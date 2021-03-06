
class ToolBuilderEnum(object):
    __slots__ = ()
    ners = "ners"
    apconnect = "apconnect"
    timetorecovery = "timetorecovery"
    dumpdevicestatebuilder = "dumpdevicestatebuilder"
    iperf = "iperf"
    rotate = 'rotate'
    poweron = 'poweron'
    oscillate = 'oscillate'
    oscillatestop = 'oscillatestop'
    sleep = 'sleep'
    naxxx = 'naxxx'
    busyboxwget = 'busiboxwget'
# end class ToolBuilderEnum


class ToolBuilder(object):
    """
    An aggregator of tool builders
    """
    def __init__(self):
        self._ners = None
        self._apconnect = None
        self._timetorecovery = None
        self._dumpdevicestate = None
        self._iperf = None
        self._rotate = None
        self._oscillate = None
        self._oscillatestop = None
        self._commandwatch = None
        self._poweron = None
        self._poweroff = None
        self._sleep = None        
        self._watchlogs = None
        self._naxxx = None
        self._busyboxwget = None
        return

    @property
    def busyboxwget(self):
        from busyboxwgetbuilder import BusyboxWgetBuilder
        return BusyboxWgetBuilder
    
    @property
    def sleep(self):
        """
        :return: class to build sleep
        """
        from sleepbuilder import SleepBuilder 
        return SleepBuilder
        
    @property
    def watchlogs(self):
        """
        :return: TheWatcher builder
        """
        from watcherbuilder import WatcherBuilder
        return WatcherBuilder

    @property
    def oscillatestop(self):
        from oscillatebuilder import OscillateStopBuilder
        return OscillateStopBuilder

    @property
    def oscillate(self):
        """
        """
        from oscillatebuilder import OscillateBuilder
        return OscillateBuilder

    @property
    def commandwatch(self):
        from commandwatchbuilder import CommandWatchBuilder
        return CommandWatchBuilder

    @property
    def rotate(self):
        from rotatebuilder import RotateBuilder
        return RotateBuilder

    @property
    def poweron(self):
        """
        :return: A builder for the Synaxxx power on
        """
        from poweronbuilder import PowerOnBuilder
        return PowerOnBuilder

    @property
    def poweroff(self):
        """
        """
        from poweroffbuilder import PowerOffBuilder
        return PowerOffBuilder
    
    @property
    def ners(self):
        from nersbuilder import NersBuilder
        return NersBuilder

    @property
    def apconnect(self):
        from apconnectbuilder import APConnectBuilder
        return APConnectBuilder

    @property
    def timetorecovery(self):
        from timetorecoverybuilder import TimeToRecoveryBuilder
        return TimeToRecoveryBuilder

    @property
    def dumpdevicestate(self):
        from dumpdevicestatebuilder import DumpDeviceStateBuilder
        return DumpDeviceStateBuilder

    @property
    def iperf(self):
        from iperfsessionbuilder import IperfSessionBuilder
        return IperfSessionBuilder

    @property
    def naxxx(self):
        from naxxxbuilder import NaxxxBuilder
        return NaxxxBuilder
# end class ToolBuilder
