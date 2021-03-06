
# python Libraries
from collections import namedtuple

# apetools Libraries
from apetools.baseclass import BaseClass
from errors import OperatorError
from countdown import CountDown


ELAPSED_TIME = 'Elapsed Time: {t}'


class CrashRecord(namedtuple("CrashRecord",
                             "id start_time crash_time error")):
    """
    A CrashRecord holds the crash information for later.
    """
    __slots__ = ()

    def __str__(self):
        message = ("Crash Record -- ID: {i}"
                   " Start Time: {s} Crash Time: {c} Error: {e}")
        return message.format(i=self.id,
                              s=self.start_time,
                              e=self.error,
                              c=self.crash_time)


class Hortator(BaseClass):
    """
    A builder builds objects.
    """
    def __init__(self, operations, *args, **kwargs):
        """
        :param:

         - `operations`: An iterator of operators
         - `storage`: a file mover for the log
        """
        super(Hortator, self).__init__(*args, **kwargs)
        self.operations = operations
        self.last_operator = None
        self._countdown = None
        return

    @property
    def countdown(self):
        """
        :return: a countdown-timer
        """
        if self._countdown is None:
            self._countdown = CountDown(self.operations.count)
        return self._countdown

    def __call__(self):
        """
        Runs the operators
        """
        self.countdown.start()

        crash_times = []

        for operation_count, operation in enumerate(self.operations):
            operation_start = self.countdown.now
            try:
                operation()
            except OperatorError as error:
                crash_time = self.countdown.now
                self.logger.error(error)
                crash_times.append(CrashRecord(id=operation_count,
                                               start_time=operation_start,
                                               error=error,
                                               crash_time=crash_time))
            except KeyboardInterrupt:
                warning = "Oh, I am slain. (by a Keyboard-Interrupt)"
                self.logger.warning(warning)
                break
            self.countdown.add(operation_start)
            remaining = self.countdown.remaining(operation_count)
            if remaining:
                message = "{0} out of {1} tests completed"
                self.logger.info(message.format(operation_count,
                                                self.operations.count))
                message = "Estimated Time Remaining: {0}"
                self.logger.info(message.format(remaining))

        for crash in crash_times:
            print str(crash)
        self.logger.info(ELAPSED_TIME.format(t=self.countdown.elapsed))
        return
# end class Hortator
