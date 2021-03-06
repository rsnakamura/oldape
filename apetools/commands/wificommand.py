
#python libraries
import re

#apetools
from apetools.commons import errors

from basewificommand import BaseWifiCommand

MAC_UNAVAILABLE = "MAC Unavailable (use `netcfg`)"
CommandError = errors.CommandError

class WifiCommandError(CommandError):
    """
    An error to raise if the Wifi Command fails
    """
# end class WifiCommandError

class WifiCommand(BaseWifiCommand):
    """
    The Wifi Command interprets `wifi` information

    :warning: this was copied from the wl command and needs updating
    """
    def __init__(self, *args, **kwargs):
        """
        :param:

         - `connection`: A connection to the device
         - `interface`: The interface to check
         - `operating_system` : The operating system on the devices.
        """
        super(WifiCommand, self).__init__(*args, **kwargs)
        return

    @property
    def bitrate(self):
        return self.get("bitrate").readline()
    
    @property
    def interface(self):
        """
        :return: the name of the wireless interface
        """
        if self._interface is None:
            self.logger.warning("wl doesn't use the interface name")
        return self._interface

    @property
    def rssi(self):
        """
        This is dynamically generated
        
        :return: The rssi for the interface
        """
        output = self.get("rssi")
        return output.readline()
    
    @property
    def mac_address(self):
        """
        :return: MAC Address of the interface
        """
        if self._mac_address is None:
            output = self.get("mac")
            self._mac_address = output.readline()
        return self._mac_address

    @property
    def ssid(self):
        """
        :return: the SSID of the currently attched ap
        """
        output = self.get('ssid')
        return output.readline().split(":")[-1]

    @property
    def noise(self):
        """
        :return: the current noise
        """
        return self.get('noise').readline()

    @property
    def channel(self):
        """
        :return: the current channel setting
        """
        output = self.get('status')
        for line in output:
            if "Control channel:" in line:
                return line.split(":")[-1].strip()
        return

    @property
    def bssid(self):
        """
        :return: the bssid of the attached ap
        """
        return self.get('bssid').readline()
    
    def get(self, subcommand):
        """
        :param:

         - `subcommand`: `wifi` subcommand

        :return: stdout for the command
        """
        with self.connection.lock:
            output, error = self.connection.wifi(subcommand)
        err = error.readline()
        if "not found" in err:
            self.logger.error(err)
            raise CommandError("The `wifi` command wasn't found on the device")
        if len(err) > 1:
            self.logger.error(err)
        return output
        
    def _match(self, expression, name, command):
        """
        :param:

         - `expression`: The regular expression to match
         - `name`: The group name to pull the match out of the line
         - `command`: The command to send to iw
         
        :return: The named-group that matched or None
        """
        expression = re.compile(expression)
        with self.connection.lock:
            output, error = self.connection.iw(command)
        for line in output:
            match = expression.search(line)
            if match:
                return match.group(name)
        err = error.read()
        if len(err):
            self.logger.error(err)
            if "No such device" in err:
                raise CommandError("Unknown Interface: {0}".format(self.interface))
            else:
                raise CommandError(err)
        return

    def __str__(self):
        return "({iface}) RSSI: {rssi}".format(iface=self.interface,
                                               rssi=self.rssi)
# end class WifiCommand

if __name__ == "__main__":
    from apetools.connections import adbconnection
    connection = adbconnection.ADBShellConnection()
    iw = IwCommand(connection)
    print(str(iw))