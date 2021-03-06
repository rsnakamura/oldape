
# python standard library
import time

# apetools
from apetools.log_setter import LOG_TIMESTAMP


class TimestampFormatEnums(object):
    """
    A class to hold the format names
    """
    __slots__ = ()
    iperf = "iperf"
    log = 'log'
# end class TimestampFormatEnums

formats = {TimestampFormatEnums.iperf:"%Y%m%d%H%M%S",
           TimestampFormatEnums.log:LOG_TIMESTAMP}


class TimestampFormat(object):
    """
    A class to hold timestampformats
    """
    def __init__(self, format_type=TimestampFormatEnums.log):
        """
        :param:
        
         - `format_type`: the type of format to use (see TimestampFormatEnum)
        """
        self.format_type = format_type
        self._format = None
        self._now = None
        return

    @property
    def format(self):
        """
        :return: the strftime format
        """
        return formats[self.format_type]


    @property
    def now(self):
        """
        :return: timestamp for now
        """
        return time.strftime(self.format)

    def convert(self, time_in_seconds):
        """
        :param:

         - `time_in_seconds`: seconds since the epoch (as float)

        :return: the given time converted to a formatted string
        """
        return time.strftime(self.format, time.localtime(time_in_seconds))
    
    def __call__(self):
        """
        A pass-through to self.now
        """
        return self.now
# end class TimestampFormat
