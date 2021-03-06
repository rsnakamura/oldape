
#python Libraries
import socket
import os
from threading import RLock

# third-party libraries
import paramiko

# apetools Libraries
from apetools.commons.readoutput import ValidatingOutput
#apetools libraries
from apetools.baseclass import BaseClass
from apetools.commons import errors

ConnectionError = errors.ConnectionError

# connections
from nonlocalconnection import NonLocalConnection
from localconnection import OutputError


SPACER = '{0} {1}'
UNKNOWN = "Unknown command: "
EOF = ''
SPACE = ' '
DOT_JOIN = "{0}.{1}"
NEWLINE = "\n"


class SSHClient(paramiko.SSHClient):
    """
    Subclasses paramiko's SSHClient to add a timeout.
    """
    def exec_command(self, command, timeout=None, bufsize=-1, combine_stderr=False):
        """
        :param:

         - `command`: A string to send to the client.
         - `timeout`: Set non-blocking timeout.
         - `bufsize`: Interpreted same way as python `file`.
         - `combine_stderr`: Sets the paramiko flag so there's only one stream

        :rtype: tuple
        :return: stdin, stdout, stderr
        """
        channel = self._transport.open_session()
        channel.settimeout(timeout)
        channel.exec_command(command)
        stdin = channel.makefile('wb', bufsize)
        stdout = channel.makefile('rb', bufsize)
        if combine_stderr:
            channel.set_combine_stderr(combine_stderr)
            stderr = stdout
        else:
            stderr = channel.makefile_stderr('rb', bufsize)
        return stdin, stdout, stderr

    def invoke_shell(self, term='vt100', width=80, height=24, timeout=None, bufsize=-1):
        """
        :param:

         - `term`: Terminal to emulate.
         - `width`: Screen width
         - `height`: Screen Height.
         - `timeout`: Set non-blocking timeout.
         - `bufsize`: Interpreted same way as python `file`.

        :rtype: tuple
        :return: stdin, stdout, stderr
        """
        channel = self._transport.open_session()
        channel.settimeout(timeout)
        channel.get_pty(term, width, height)
        channel.invoke_shell()
        stdin = channel.makefile('wb', bufsize)
        stdout = channel.makefile('rb', bufsize)
        stderr = channel.makefile_stderr('rb', bufsize)
        return stdin, stdout, stderr

    def invoke_shell_rw(self, term='vt100', width=80, height=24, timeout=None, bufsize=-1):
        """
        :param:

         - `term`: Terminal to emulate.
         - `width`: Screen width
         - `height`: Screen Height.
         - `timeout`: Set non-blocking timeout.
         - `bufsize`: Interpreted same way as python `file`.

        :rtype: tuple
        :return: i/o
        """
        channel = self._transport.open_session()
        channel.settimeout(timeout)
        channel.set_combine_stderr(True)
        channel.get_pty(term, width, height)
        channel.invoke_shell()

        shell = channel.makefile('r+b', bufsize)
        return shell
#end class SSHClient


class SimpleClient(BaseClass):
    """
    A simple wrapper around paramiko's SSHClient.

    The only intended public interface is exec_command.
    """
    def __init__(self, hostname, username, password=None, port=22, timeout=5):
        """
        :param:

         - `hostname`: ip address or resolvable hostname.
         - `username`: the login name.
         - `password`: optional if ssh-keys are set up.
         - `port`: The port for the ssh process.
         - `timeout`: Time to give the client to connect
        """
        super(SimpleClient, self).__init__()
        self._logger = None
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.timeout = timeout
        self._client = None
        return

    def exec_command(self, command, timeout=10):
        """
        A pass-through to the SSHClient's exec_command.

        :param:

         - `command`: A string to send to the client.
         - `timeout`: Set non-blocking timeout.

        :rtype: tuple
        :return: stdin, stdout, stderr

        :raise: ConnectionError for paramiko or socket exceptions
        """
        if not command.endswith(NEWLINE):
            command += NEWLINE
        try:
            return self.client.exec_command(command, timeout)

        except paramiko.SSHException as error:
            self._client = None
            self.logger.error(error)
            raise ConnectionError("There is a problem with the ssh-connection to:\n {0}".format(self))
        except paramiko.PasswordRequiredException as error:
            self.logger.error(error)
            self.logger.error("Private Keys Not Set Up, Password Required.")
            raise ConnectionError("SSH Key Error :\n {0}".format(self))
        except socket.error as error:
            self.logger.error(error)
            if 'Connection refused' in error: 
                raise ConnectionError("SSH Server Not responding: check setup:\n {0}".format(self))
            raise ConnectionError("Problem with:\n {0}".format(self))
        return
        
    @property
    def client(self):
        """
        :rtype: paramiko.SSHClient
        :return: An instance of SSHClient connected to remote host.
        :raise: ClientError if the connection fails.
        """
        if self._client is None:
            self._client = SSHClient()
            self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._client.load_system_host_keys()
            try:
                self._client.connect(hostname=self.hostname,
                                     port=self.port,
                                     username=self.username,
                                     password=self.password,
                                     timeout=self.timeout)
            except paramiko.AuthenticationException as error:
                self.logger.error(error)
                raise ConnectionError("There is a problem with the ssh-keys or password for \n{0}".format(self))
            except socket.timeout as error:
                self.logger.error(error)
                raise ConnectionError("Paramiko is unable to connect to \n{0}".format(self))
        return self._client

    def __str__(self):
        """
        :return: username, hostname, port, password in string
        """
        user = "Username: {0}".format(self.username)
        host = "Hostname: {0}".format(self.hostname)
        port = "Port: {0}".format(self.port)
        password = "Password: {0}".format(self.password)
        return NEWLINE.join([user, host, port, password])

    def close(self):
        """
        :postcondition: client's connection is closed and self._client is None                
        """
        self.client.close()
        self._client = None
        return
# class SimpleClient


class SSHConnection(NonLocalConnection):
    """
    An SSHConnection executes commands over an SSHConnection
    """
    def __init__(self, hostname, username,
                 password=None, port=22, timeout=5, 
                 *args, **kwargs):
        """
        SSHConnection Constructor
        
        :param:

         - `hostname`: The IP Address or hostname
         - `username`: The login username.
         - `password`: The login password
         - `port`: The ssh port
         - `operating_system`: OperatingSystem enumeration
         - `timeout`: The login timeout
        """
        super(SSHConnection, self).__init__(*args, **kwargs)
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.timeout = timeout
        self._logger = None
        self._client = None
        self._lock = None
        return

    @property
    def client(self):
        """
        :return: SimpleClient for the SSHConnection
        """
        if self._client is None:
            self._client = SimpleClient(hostname=self.hostname, username=self.username,
                                        password=self.password, port=self.port,
                                        timeout=self.timeout)
        return self._client
    

    def _main(self, command, arguments, timeout):
        """
        This isn't intended to be run.
        The . notation is the expected interface.
        
        runs the SimpleClient exec_command

        :param:

         - `command`: The shell command.
         - `arguments`: A string of command arguments.
         - `timeout`: readline timeout for the SSHConnection
        :return: OutputError with output and error file-like objects
        """
        self.logger.debug("command: {0}, arguments: {1}".format(command,
                                                                arguments))
        if len(self.command_prefix):
            command = SPACER.format(self.command_prefix,
                                    command)

        command = SPACER.format(command, arguments)
        self.logger.debug("calling client.exec_command with '{0}'".format(command))

        # the guys at Ryan's house are running into 'Administratively prohibited'
        # which apparently happens if too many clients try to connect to the ssh-server
        # I don't think this is where the problem is
        # but to take this out of the question I'm going to put a lock so no more
        # than one paramiko client can hit the server at once
        with self.lock:
            stdin, stdout, stderr = self.client.exec_command(command, timeout=timeout)
        
        self.logger.debug("Completed exec_command of: '{0}'".format(command))

        return OutputError(OutputFile(stdout, self.check_errors), OutputFile(stderr, self.check_errors))

    def check_errors(self, line):
        """
        Doesn't do anything - SSHClient handles ssh errors. Overwrite in sub-classes if needed
        """
        return
    
    def __str__(self):
        return "{0} ({1}): {2}@{3} ".format(self.__class__.__name__, self.operating_system, self.username, self.hostname)
# end class SSHConnection


class OutputFile(ValidatingOutput):
    """
    A class to handle the ssh output files

    This traps socket timeouts.
    """
    def __init__(self, *args, **kwargs):
        super(OutputFile, self).__init__(*args, **kwargs)
        return

    def readline(self, timeout=10):
        """
        :param:

         - `timeout`: The length of time to wait for output

        :return: line from readline, EOF or None (in event of timeout)
        """
        if not self.empty:
            try:
                line = self.lines.readline()
                if line == EOF:
                    self.end_of_file = True
                self.validate(line)
                return line
            except socket.timeout:
                self.logger.debug("socket.timeout")
                return SPACE
        return EOF
# end class OutputFile


if __name__ == "__main__":
    #c = SSHConnection('igor', 'developer')
    #o = c.wmic('path win32_networkadapter where netconnectionid="\'Wireless Network Connection\'" call enable')
    #for index, line in enumerate(o.output):
    #    print index, line
    c = SSHConnection('fakeuser', 'localhost')
    o = c.ls()
    for line in o.output:
        print line
