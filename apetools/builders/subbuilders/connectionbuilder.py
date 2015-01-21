
#python standard library
from collections import namedtuple
from abc import ABCMeta, abstractproperty

#apetools
from apetools.connections import adbconnection, nonlocalconnection
from apetools.baseclass import BaseClass
from apetools.connections import sshconnection
from apetools.commons import errors


#SSHParameters = namedtuple("SSHParameters", "hostname username password".split())
class SSHParameters(object):
    """
    To make the parameters optional this is changed to a class
    """
    def __init__(self, hostname, username, password=None):
        self.hostname = hostname
        self.username = username
        self.password = password
    


class ConnectionBuilderBase(BaseClass):
    __metaclass__ = ABCMeta
    def __init__(self, parameters):
        self.parameters = parameters
        self._connection = None
        return

    @abstractproperty
    def connection(self):
        """
        The built connection.
        """
        return        


class DummyConnectionBuilder(ConnectionBuilderBase):
    """
    Builds a Dummy Connection
    """
    def __init__(self, *args, **kwargs):
        super(DummyConnectionBuilder, self).__init__(*args, **kwargs)
        return

    @property
    def connection(self):
        """
        The DummyConnection

        :return: DummyConnection object
        """
        if self._connection is None:
            self._connection = nonlocalconnection.DummyConnection()
        return self._connection


class AdbShellConnectionBuilder(BaseClass):
    """
    Use this to get an adb shell connection
    """
    def __init__(self, parameters=None):
        """
        AdbShellConnectionBuilder Constructor
        
        :param:

         - `parameters`: Not used, just here to keep the interface uniform
        """
        super(AdbShellConnectionBuilder, self).__init__()
        self._connection = None
        return

    @property
    def connection(self):
        """
        The ADB Shell Connection
        
        :rtype: ADBShellConnection
        :return: A built ADB shell connection
        """
        if self._connection is None:
            self.logger.debug("Creating the adb shell connection")
            self._connection = adbconnection.ADBShellConnection()
        return self._connection
# end class AdbShellConnectionBuilder


class SSHConnectionBuilder(BaseClass):
    """
    Use this to get an ssh connection
    """
    def __init__(self, parameters):
        """
        :param:

         - `parameters`: An object with `hostname`, `username`, and `password` attributes
        """
        super(SSHConnectionBuilder, self).__init__()
        self._logger = None
        self.parameters = parameters
        self._hostname = None
        self._username = None
        self._password = None
        self._connection = None
        self._operating_system = None
        self._path = None
        self._library_path = None
        return

    @property
    def operating_system(self):
        """
        :return: parameters.operating_system
        """
        if self._operating_system is None:
            try:
                self._operating_system = self.parameters.operating_system
            except AttributeError as error:
                self.logger.debug(error)
                self.logger.warning("Operating System not found in: {0}".format(self.parameters))
        return self._operating_system

    @property
    def library_path(self):
        """
        :return: LD_LIBRARY_PATH value(s) or None
        """
        if self._library_path is None:
            try:
                self._library_path = ":".join(self.parameters.library_path.split())
            except AttributeError as error:
                self.logger.debug(error)
        return self._library_path

    @property
    def path(self):
        """
        :return: additions to the PATH
        """
        if self._path is None:
            try:
                self._path = ":".join(self.parameters.path.split())
            except AttributeError as error:
                self.logger.debug(error)
        return self._path
    @property
    def hostname(self):
        """
        :rtype: StringType
        :return: The hostname (I.P.) to connect to
        :raise: ConfigurationError if not set
        """
        if self._hostname is None:
            try:
                self._hostname = self.parameters.hostname
            except AttributeError as error:
                self.logger.debug(error)
                try:
                    self._hostname = self.parameters.address
                except AttributeError as error:
                    self.logger.debug(error)
                    raise errors.ConfigurationError("`hostname` is a required parameter for the SSHConnection")
        return self._hostname

    @property
    def username(self):
        """
        :rtype: StringType
        :return: user login name
        :raise: ConfigurationError if not found
        """
        if self._username is None:
            try:
                self._username = self.parameters.username
            except AttributeError as error:
                self.logger.debug(error)
                try:
                    self._username = self.parameters.login
                except AttributeError as error:
                    self.logger.debug(error)
                    raise errors.ConfigurationError("`username` is a required parameter for the SSHConnection")                
        return self._username

    @property
    def password(self):
        """
        :return: the password for the connection (sets to None if not given in the parameters)
        """
        if self._password is None:
            try:
                self._password = self.parameters.password
            except AttributeError as error:
                self.logger.debug(error)
                self._password = None
        return self._password
    
    @property
    def connection(self):
        """
        :return: an SSHConnection
        """
        if self._connection is None:
            self.logger.debug("Creating the ssh connection.")
            self._connection = sshconnection.SSHConnection(hostname=self.hostname,
                                                           username=self.username,
                                                           password=self.password,
                                                           path=self.path,
                                                           library_path=self.library_path,
                                                           operating_system=self.operating_system)
        return self._connection
# end class SshConnectionBuilder


class AdbShellSshConnectionBuilder(SSHConnectionBuilder):
    """
    A class to build an adb-shell connection over ssh
    """
    def __init__(self, *args, **kwargs):
        """
        :param:

         - `parameters`: An object with `hostname`, `username`, and `password` attributes
        """
        super(AdbShellSshConnectionBuilder, self).__init__(*args, **kwargs)
        self._serial_number = None
        return

    @property
    def serial_number(self):
        """
        A serial number for the USB connection
        """
        if self._serial_number is None:
            if hasattr(self.parameters, 'serial_number'):
                self._serial_number = self.parameters.serial_number
        return self._serial_number
    
    @property
    def connection(self):
        """
        :return: ADBShellSSHConnection instance
        """
        if self._connection is None:
            self.logger.debug("Creating the ADBShellConnection")
            self._connection = adbconnection.ADBShellSSHConnection(hostname=self.hostname,
                                                                   username=self.username,
                                                                   password=self.password,
                                                                   path=self.path,
                                                                   library_path=self.library_path,
                                                                   operating_system=self.operating_system,
                                                                   serial_number=self.serial_number)
        return self._connection
# end class AdbShellSshConnectionBuilder


class ConnectionBuilderTypes(object):
    __slots__ = ()
    ssh = 'ssh'
    adbshellssh = "adbshellssh"
    adbshell = "adbshell"
    dummy = 'dummy'
# end class BuilderTypes


connection_builders = {ConnectionBuilderTypes.ssh: SSHConnectionBuilder,
                       ConnectionBuilderTypes.adbshellssh: AdbShellSshConnectionBuilder,
                       ConnectionBuilderTypes.adbshell: AdbShellConnectionBuilder,
                       ConnectionBuilderTypes.dummy: DummyConnectionBuilder}


#python standard library
import unittest

#third-party
from mock import MagicMock
from nose.tools import raises


class BadChild(ConnectionBuilderBase):
    def __init__(self, *args, **kwargs):
        super(BadChild, self).__init__(*args, **kwargs)
        return

class GoodChild(ConnectionBuilderBase):
    def __init__(self, *args, **kwargs):
        super(GoodChild, self).__init__(*args, **kwargs)
        return

    def connection(self):
        return
    
class TestConnectionBuilderBase(unittest.TestCase):
    def test_parameters(self):
        """
        Does ConnectionBuilderBase take a `parameters` argument on construction?
        """
        parameters = MagicMock()
        builder = GoodChild(parameters=parameters)
        self.assertEqual(parameters, builder.parameters)
        return

    @raises(TypeError)
    def test_no_connection(self):
        """
        Does a child that hasn't implemented the connection raise an error?
        """
        BadChild(None)
        return


class TestDummyConnectionBuilder(unittest.TestCase):
    def test_connection(self):
        """
        Is the connection a Dummy Connection?
        """
        builder = DummyConnectionBuilder(None)
        self.assertIsInstance(builder.connection, nonlocalconnection.DummyConnection)        
        return


class TestConnectionBuilders(unittest.TestCase):
    def test_valid_keys(self):
        """
        Are all the keys in the ConnectionBuilderTypes?
        """
        for connection_type in connection_builders:
            self.assertTrue(hasattr(ConnectionBuilderTypes, connection_type))
        return
