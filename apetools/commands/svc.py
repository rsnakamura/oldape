
from abc import ABCMeta, abstractmethod

from apetools.baseclass import BaseClass
from apetools.connections import adbconnection
from apetools.commons.errors import CommandError

class ToggleWifiBase(BaseClass):
    """
    A callable class to enable or disable wifi
    """
    __metaclass__ = ABCMeta
    
    def __init__(self, connection=None, command=None):
        super(ToggleWifiBase, self).__init__()
        self._logger = None
        self.connection = connection
        self._command = command
        return

    @property
    def command(self):
        """
        :return: a command with a `enable_wifi` method
        """
        if self._command is None:
            self._command = Svc(connection=self.connection)
        return self._command

    @abstractmethod
    def __call__(self, parameters=None):
        """
        Calls the command's <enable|disable>_wifi method

        :param:

         - `parameters`: not used
        """
        return
# end class ToggleWifiBase

class EnableWifi(ToggleWifiBase):
    """
    A callable class to enable wifi
    """
    def __call__(self, parameters=None):
        """
        Calls the command's `enable_wifi` method

        :param:

         - `parameters`: not used
        """
        self.command.enable_wifi()
        return
# end class EnableWifi

class DisableWifi(ToggleWifiBase):
    """
    A callable class to disable wifi
    """
    def __call__(self, parameters=None):
        """
        Calls the command's `disable_wifi` method

        :param:

         - `parameters`: not used
        """
        self.command.disable_wifi()
        return
# end class DisableWifi

class Svc(BaseClass):
    """
    The Android's SVC command (wifi only).
    """
    def __init__(self, connection=None, enable_wifi_command="wifi enable",
                 disable_wifi_command="wifi disable"):
        """
        :param:

         - `connection`: a connection to the device (creates `ADBShellConnection` if not given)
         - `enable_wifi_command`: command to send to svc to enable radio
         - `disable_wifi_command`: command to send to svc to disable radio
        """
        super(Svc, self).__init__()
        self._connection = connection
        self.enable_wifi_command = enable_wifi_command
        self.disable_wifi_command = disable_wifi_command
        return

    @property
    def connection(self):
        """
        :return: connection to the device
        """
        if self._connection is None:
            self._connection = adbconnection.ADBShellConnection()
        return self._connection

    def call_svc(self, command):
        """
        :param:

         - `command`: the command to send to 'svc'
        """
        with self.connection.lock:
            output, error = self.connection.svc(command)
        self.validate(output, command)
        return
        
    def enable_wifi(self):
        """
        Enable the WiFi radio
        """
        self.call_svc(self.enable_wifi_command)
        return

    def disable_wifi(self):
        """
        Disable the wifi radio
        """
        self.call_svc(self.disable_wifi_command)
        return

    def validate(self, output, subcommand):
        """
        :raise: CommandError if there is an error in the output
        """
        for line in output:
            self.logger.debug(line)
            if "Killed" in line:
                raise CommandError("'svc' must be run as root")
            if "not found" in line:
                raise CommandError("'svc' wasn't found on the path")
            if "Available commands" in line:
                raise CommandError("'svc' subcommand missing or incorrect (given: `{0}`".format(subcommand))
        return
# end class Svc