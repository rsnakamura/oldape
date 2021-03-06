
#python
import time
from types import IntType

#apetools
from apetools.baseclass import BaseClass

#affectors
from elexol import elexol24
from errors import FaucetteError


# Total number of AC ports device can control
MAX_PINS = 24
# Total number of AC devices per port (A, B, C)
PINS_PER_PORT = 8
# Time, in seconds, to delay between turning a device on/off
TOGGLE_DELAY = 0.05
# Maximum number of devices that are allowed to be on at a time.
MAX_ON = 6
# ID if first pin
FIRST_PIN = 0

ON = "on"
OFF = "off"


class NetworkedPowerSupply (BaseClass):
    """
    This class provides access to the Network Power Supply (NPS). 
    It prevents electrically unsafe use.

    The most important commands to use are:

       * `TurnOn()`
       * `TurnOff()`
       * `TurnOffList()`
       * `TurnOnList()`

    * `TurnOn/Off()`: specify which AC port to turn on/off via integer identifier
    * `TurnOff/OnList()`: accepts a list of devices to turn on or off. 
    * `TurnOnList()`: keyword 'clear' indicates whether to disable devices already on.

    Error checking is done to ensure that devices turn on/off as expected.
    """
    def __init__ (self, IP, clear=True, retry=5, ports="ABC"):
        """
        Initializes an elexol24 object to talk to the NPS device.
     
        :param:
         - `IP`    : String IP address of the Elexol device.
         - `clear` : Bool indicating whether or not NPS will disable all plugs at start
         - `retry` : Number of times to retry if communication with Elexol fails.
         - `ports`: The elexol's serial port ID's (needs to be iterable)
        """
        super(NetworkedPowerSupply, self).__init__()
        self.IP = IP
        self.clear = clear
        self.retry = retry
        self.ports = ports

        self._elexol = None
        self._port_status = None
        
        # index iterators
        self._attempts = None
        self._pins = None
        self._pins_per_port = None

        # method dictionaries
        self._check_switch_is = None
        self._turn_switch = None
        return

    @property
    def turn_switch(self):
        """
        :return: dict of ON:elexol.setpin24, OFF:elexol.clearpin24
        """
        if self._turn_switch is None:
            self._turn_switch = {}
            self._turn_switch[ON] = self.elexol.setpin24
            self._turn_switch[OFF] = self.elexol.clearpin24
        return self._turn_switch

    @property
    def check_switch_is(self):
        """
        :return: dict of ON:self.switch_is_on, OFF:port_is_off
        """
        if self._check_switch_is is None:
            self._check_switch_is = {}
            self._check_switch_is[ON] = self.switch_is_on
            self._check_switch_is[OFF] = self.switch_is_off
        return self._check_switch_is

    @property
    def attempts(self):
        """
        :return: List of allowed attempts (up to self.num_retry times)     
        """
        if self._attempts is None:
            self._attempts = [attempt for attempt in range(self.retry)]
        return self._attempts

    @property
    def pins(self):
        """
        :return: List of all pin identifiers
        """
        if self._pins is None:
            self._pins = [pin for pin in range(MAX_PINS)]
        return self._pins

    @property
    def pins_per_port(self):
        """
        :return: List of pins for a single port (0-7)
        """
        if self._pins_per_port is None:
            self._pins_per_port = [pin for pin in range(PINS_PER_PORT)]
        return self._pins_per_port
    
    @property
    def elexol(self):
        """
        :return: elexol24 object
        """
        if self._elexol is None:
            self._elexol = elexol24(self.IP,
                                    self.clear,
                                    self.retry)
        return self._elexol
    
    @property
    def port_status(self):
        """
        :return: Dict of port:pin-status-list
        """
        if self._port_status is None:
            self._port_status = {}
            for port in self.ports:
                self._port_status[port] = [False for pin in self.pins_per_port]
        return self._port_status
    
    def set_port_status(self):
        """
        sets current ON/OFF status for all pins from elexol.
        
        Example retrieval of status::

            status = np.port_status[port][pin]
            
            for example,
            
            np = nps.nps()
            np.set_port_status()
            if np.port_status['B'][4]:
                print 'Port B4 is on!'
 
        See `convert_to_port_pin()` to convert pin (i.e. 23) to  port,pin (i.e., 'C', 7)

        :postcondition: `self.port_status` dict contains port,pin statuses
        """
        for port in self.ports:
            raw_int = self.elexol.getport(port)
            for pin in self.pins_per_port:
                self.port_status[port][pin] = bool(raw_int & (1 << pin))
        return

    def switch_is_on(self, switch):
        """
        :param:

         - `switch`: The switch ID (e.g. 16 for port C, pin 0)
        
        :return: True if pin is on

        :raise: FaucetteError if switch ID is invalid.
        """
        if type(switch) is not IntType:
            raise FaucetteError("Switch must be integer, not {0}".format(type(switch)))
        if switch >= MAX_PINS or switch < FIRST_PIN:
            raise FaucetteError("Switch # {0} does not exist!".format(switch))

        self.set_port_status()
        
        port, pin = self.ports[switch/PINS_PER_PORT], switch % PINS_PER_PORT
        return self.port_status[port][pin]

    def switch_is_off(self, switch):
        """
        :param:

         - `switch`: The switch ID
        :return: True if pin is off
        """
        return not self.switch_is_on(switch)

        
    def switches_on(self):
        """
        Queries Elexol to determine how many switches are currently on.

        :rtype: int
        :return: Number of switches currently ON.
        """
        count = 0
        self.set_port_status()        
                
        for port in self.ports:
            count += len([pin for pin in self.pins_per_port if self.port_status[port][pin]])
        return count
    
    def turn_on_switches(self, switches, turn_others_off=False):
        """
        Turn on all switches whose numbers are included in a provided list.

        :param:

         - `switches`: List containing integer switch numbers                
         - `turn_others_off`  : *True* turn *Off* all others.*False* leave *On*.

        :postcondition:

        - If `clear`, all switches not in `switches` are off.
        - All switches in `outlets` are on.
        """
        if turn_others_off:
            self.all_off_except(switches)
        for switch in switches:
            self.turn_on(switch)
        return
    
    def turn_off_switches(self, off_list):
        """
        Turn off all devices whose numbers are included in a provided list.

        :param:

        - `off_list` : List that contains the integer switch numbers

        :postcondition: All switches in `off_list` are off.
        """
        for switch in off_list:
            self.turn_off(switch)
        return

    def toggle_switch(self, switch, on_or_off):
        """
        Turns switch on or off based on `on_or_off` value.

        :param:

         - `switch`: Switch number to turn on.
         - `on_or_off`: ON turns switch on, OFF turns switch off
         
        :raise: FaucetteError if invalid switch, failed change, too many switches on.
        """
        self.logger.debug("Turning switch {0} {1}".format(switch, on_or_off))
        if on_or_off == ON and self.switches_on() >= MAX_ON:
            raise FaucetteError(('Maximum number of ON switches exceeded'
                                 ' ({0})--switch {1} was not turned on').format(MAX_ON, switch))

        for attempt in self.attempts:
            if self.check_switch_is[on_or_off](switch):
                return
            self.turn_switch[on_or_off](switch)
            time.sleep(TOGGLE_DELAY)
        raise FaucetteError("Could not turn {o} pin #{s}".format(s=switch,
                                                                 o=on_or_off))
        return
    
    def turn_on(self, switch):
        """
        Turn *on* switch 

        :param:
         - `switch` : Switch number to turn on

        :postcondition: switch is on.
        :raise: FaucetteError if switch out of bounds, too many on, or unable to turn on.
        """
        self.toggle_switch(switch, ON)
    
    def turn_off(self, switch):
        """
        Turn *off* switch listed by number

        :param:
        
         - `switch` : switch number to turn off

        :postcondition: switch identified by `number` is off.

        :raise: FaucetteError if switch out of bounds or unable to turn off.
        """
        self.toggle_switch(switch, OFF)
        return
    
    def all_off_except(self, exceptions=[]):
        """
        Turns off all devices on the Elexol NPS not listed in `exception` list

        :param: 
        - `exceptions` : list of device numbers (int) to leave on. (Default=all off))

        :postcondition: All devices not in `exception` are turned off.
        """
        self.logger.debug("Turning off all pins except {0}".format(exceptions))
        for pin in self.pins:
            if pin not in exceptions: 
                self.turn_off(pin)
        return

    def __str__(self):
        return "NetworkedPowerSupply: IP={0} clear={1} retry={2} ports={3}".format(self.IP,
                                                                                   self.clear,
                                                                                   self.retry,
                                                                                   self.ports)
# end class NetworkedPowerSupply
