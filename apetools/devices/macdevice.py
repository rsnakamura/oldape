
from basedevice import BaseDevice
from apetools.commands.airportcommand import AirportCommand


class MacDevice(BaseDevice):
    """
    A class to bundle commands to control a mac os device
    """
    def __init__(self, *args, **kwargs):
        """
        :param:

         - `connection`: An device connection
        """
        super(MacDevice, self).__init__(*args, **kwargs)
        self._airport = None
        return

    @property
    def airport(self):
        """
        :return: AirportCommand built with self.connection
        """
        if self._airport is None:
            self._airport = AirportCommand(connection=self.connection,
                                           interface=self.interface)
        return self._airport

    @property
    def channel(self):
        """
        :return: the channel for the current wifi connection
        """
        return self.airport.channel
    
    @property
    def rssi(self):
        """
        :return: the current RSSI
        """
        return self.airport.rssi

    @property
    def bitrate(self):
        """
        :return: the current bitrate
        """
        return self.airport.bitrate
    
    @property
    def noise(self):
        """
        :return: the current noise
        """
        return self.airport.noise

    @property
    def ssid(self):
        """
        :return: the ssid of the attached AP
        """
        return self.airport.ssid

    @property
    def bssid(self):
        """
        :return: the MAC address of the attached AP
        """
        return self.airport.bssid
    
    @property
    def mac_address(self):
        """
        :return: device mac address
        """
        if self._mac_address is None:
            self._mac_address = self.airport.mac_address
        return self._mac_address

    @property
    def wifi_control(self):
        """
        :return: Svc command (enable disable radio)
        """
        if self._wifi_control is None:
            self._wifi_control = Svc(connection=self.connection)
        return self._wifi_control

    @property
    def connection(self):
        """
        :return: connection passed in 
        """
        return self._connection

    def wake_screen(self):
        """
        Wake the screen (not implemented)
        """
        raise NotImplementedError("Wake Screen not ready yet")
        return

    def display(self, message):
        """
        Display a message on the screen (not implemented)
        """
        raise NotImplementedError("Display <message> not done yet")
        return

    def disable_wifi(self):
        """
        Sends 'networksetup -setairportpower airport off' command
        
        :postcondition: WiFi radio disabled
        """
        self.connection.networksetup("-setairportpower airport off")
        return

    def enable_wifi(self):
        """
        Sends 'networksetup -setairport airport on' command
        
        :postcondition: WiFi radio enabled
        """
        self.connection.networksetup('-setairportpower airport on')
        return

    def get_wifi_info(self):
        """
        gets the 'airpor status' command output
        :rtype: StringType
        :return: The Wifi Info
        """        
        return self.airport.status

    def log(self, message):
        """
        :postcondition: message sent to the connection
        """
        self.connection.logger(message)
        return

    @property
    def address(self):
        """
        :return: ip address of interface
        """
        return self.airport.ip_address                                 
# end class MacDevice
