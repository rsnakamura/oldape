
# python
import sys
import re
import time

# this package
from apetools.parsers import oatbran
from apetools.baseclass import BaseClass
from apetools.commons.timestamp import TimestampFormat


class TsharkWatcherEnum(object):
    """
    A class to hold variable names 
    """
    __slots__ = ()
    frames = "frames"
    bytes = 'bytes'
    
# end class TsharkWatcherEnum


COMMAND_STRING = "-i {interface} -nqz io,stat,1 -a duration:{duration}"


class TsharkWatcher(BaseClass):
    """
    A class to watch bytes and frames using tshark
    """
    def __init__(self, connection, output=None, interface="wlan0"):
        """
        :param:

         - `output`: file to send output to 
         -`connection`: connection to the device to run tshark
         - `interface`: network interface to monitor
        """
        super(TsharkWatcher, self).__init__()
        self._output = output
        self.connection = connection
        self._expression = None
        self.frames = None
        self._timestamp = None
        self.stopped = False
        self.interface = interface
        return

    @property
    def timestamp(self):
        """
        :return: timestamper
        """
        if self._timestamp is None:
            self._timestamp = TimestampFormat()
        return self._timestamp

    @property
    def output(self):
        """
        :return: file object to write to
        """
        if self._output is None:
            self._output = sys.stdout
        return self._output

    @property
    def expression(self):
        """
        :return: a regular expression to match tshark output
        """
        if self._expression is None:
            timestamp = oatbran.REAL + '-'+ oatbran.REAL
            frames = oatbran.NAMED(n=TsharkWatcherEnum.frames, e=oatbran.INTEGER)
            byte = oatbran.NAMED(n=TsharkWatcherEnum.bytes, e=oatbran.INTEGER)
            self._expression = re.compile(timestamp + oatbran.SPACES
                                          + frames+ oatbran.SPACES
                                          + byte)
        return self._expression

    def call_once(self):
        """

        """
        timestamp = self.timestamp.now
        byte_count = 0
        frames = 0
        output, error = self.connection.tshark(COMMAND_STRING.format(interface=self.interface,
                                                                     duration=1))
        for line in output:
            match = self.expression.search(line)
            if match:
                match = match.groupdict()
                frames += int(match[TsharkWatcherEnum.frames])
                byte_count += int(match[TsharkWatcherEnum.bytes])                
        return timestamp, frames, byte_count

    def stop(self):
        """
        :postcondition: self.stopped is True
        """
        self.stopped = True
        return
    
    def __call__(self, duration=10):
        """
        :postcondition: tshark data sent to self.output
        """
        self.output.write("timestamp,frames,bytes\n")
        self.logger.info("Watching the tshark packets for {0} seconds.".format(duration))
        ctime = time.time()
        command = COMMAND_STRING.format(interface=self.interface,
                                        duration=duration)
        self.logger.debug(command)
        output, error = self.connection.tshark(command)
        for line in output:
            match = self.expression.search(line)
            if match:
                match = match.groupdict()
                time_stamp = self.timestamp.convert(ctime)
                frames = match[TsharkWatcherEnum.frames]
                byte_count = match[TsharkWatcherEnum.bytes]

                self.output.write("{0},{1},{2}\n".format(time_stamp,
                                                         frames,
                                                     byte_count))

                ctime += 1

        return
# end class TsharkWatcher


if __name__ == "__main__":
    from apetools.connections.sshconnection import SSHConnection
    c = SSHConnection("portegeether", "portegeadmin")
    watch = TsharkWatcher(c)
    watch()
