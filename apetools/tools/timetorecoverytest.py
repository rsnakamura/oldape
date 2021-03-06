
# python libraries
from collections import namedtuple

#timetorecovery libraries
from apetools.baseclass import BaseClass


TimeToRecoveryTestParameters = namedtuple("TimeToRecoveryTestParameters",
                                          ['output',
                                          'device',
                                           'time_to_recovery'])


NEWLINE_STRING = "{0}\n"


class TimeToRecoveryTest(BaseClass):
    """
    A time to recovery Test times how long it takes to recover.
    """
    def __init__(self, parameters, *args, **kwargs):
        """
        :param:

         - `parameters`: A TimeToRecoveryTestParameters object
        """
        super(TimeToRecoveryTest, self).__init__(*args, **kwargs)
        self.parameters = parameters
        self._device = None
        self._output = None
        self._time_to_recovery = None
        return

    @property
    def device(self):
        if self._device is None:
            self._device = self.parameters.device
        return self._device

    @property
    def output(self):
        if self._output is None:
            self._output = self.parameters.output
        return self._output

    @property
    def time_to_recovery(self):
        """
        :return: The time-to-recovery measurer passed in as a parameter
        """
        if self._time_to_recovery is None:
            self._time_to_recovery = self.parameters.time_to_recovery
        return self._time_to_recovery
    
    def run(self, parameters):
        """
        Runs a single time to recovery test.
        """
        self.logger.info("Enabling Wifi")
        self.device.enable_wifi()
        self.logger.info("Waiting for the device to recover")
        elapsed_time = self.time_to_recovery.run(parameters)
        self.save_data(elapsed_time, parameters.criteria, parameters.repetition)
        return elapsed_time

    def save_data(self, elapsed, criteria, repetition):
        """
        :param:

         - `elapsed`: Value returned from time-to-recovery
         - `criteria`: upper-bound to passing the test.
         - `repetition`: The current repetition
        """
        if elapsed > criteria or elapsed is None:
            self.log_message("Failed TTR Test: Repetition: {r} Actual: time={a} Expected: time<{e}".format(r=repetition,
                                                                                                           a=elapsed,
                                                                                                           e=criteria))
        else:
            self.log_message("Time-To-Recover: {0}".format(elapsed))
        self.output.write(NEWLINE_STRING.format(elapsed))
        return

    def log_message(self, message):
        """
        :param:

         - `message`: Message to send to logger log and device log
        """
        self.device.log(message)
        self.logger.info(message)
        return
# end TimeToRecoveryTest  
