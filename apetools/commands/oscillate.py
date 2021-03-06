
#python standard library
from threading import Thread, Event
from Queue import Queue
from time import sleep
import re

# apetools modules
from apetools.baseclass import BaseClass
from apetools.commons.errors import ConnectionError, CommandError
from apetools.commons.timestamp import TimestampFormat
from apetools.tools.sleep import Sleep
from basecommand import BaseThreadedCommand

class OscillatorError(CommandError):
    """
    Exception to raise if the oscillator fails
    """
# end class OscillatorError

class Oscillate(BaseThreadedCommand):
    """
    A Class to start and stop an oscillator
    """
    def __init__(self, connection, output, arguments, retries=2, block=False):
        """
        :param:

         - `connection`: connection to oscillation master
         - `output`: file to send angle information to
         - `arguments`: string of arguments for the oscillate command
         - `retries`: number of times to retry the oscillate command
         - `block`: if True, waits for rotation start on each call
        """
        super(Oscillate, self).__init__()
        self.connection = connection
        self.output = output
        self.retries = retries
        self.block = block
        self._timestamp = None
        self.arguments = arguments
        self._rotation_start = None
        self._event = None
        self._thread = None
        self._error_queue = None
        self._sleep = None
        self.name = 'oscillate'
        return

    @property
    def sleep(self):
        """
        :return: a blocking (but verbose) sleep
        """
        if self._sleep is None:
           self._sleep = Sleep(10) 
        return self._sleep
    
    @property
    def event(self):
        """
        :return: OscillateEvent with self.rotation_start event
        """
        if self._event is None:
            self._event = OscillateEvent(self.rotation_start)
        return self._event

    @property
    def timestamp(self):
        """
        :return: timestamper
        """
        if self._timestamp is None:
            self._timestamp = TimestampFormat()
        return self._timestamp

    @property
    def error_queue(self):
        """
        :return: queue of error messages
        """
        if self._error_queue is None:
            self._error_queue = Queue()
        return self._error_queue

    @property
    def rotation_start(self):
        """
        :return: threading event
        """
        if self._rotation_start is None:
            self._rotation_start = Event()
        return self._rotation_start

    @property
    def thread(self):
        """
        :return: self.run executing in a thread
        """
        if self._thread is None:
            self._thread = Thread(target=self.run_thread, name="Oscillator")
            self._thread.daemon = True
            self._thread.start()
            self.logger.info("sleeping to wait for the table to error-out")
            self.sleep()
            if not self.error_queue.empty():
                self._thread = None
                raise OscillatorError(self.error_queue.get())

        return self._thread

    def run(self):
        """
        :postcondition: oscillate command sent to the oscillator
        """
        rotation_expression = re.compile("Rotating\s+[Ff]rom")
        try:
            with self.connection.lock:
                self.logger.info("Starting the oscillation")
                output, error = self.connection.oscillate(self.arguments)
            for line in self.generate_output(output, error):
                self.logger.debug(line)
                if line.startswith("<Oscillator>"):
                    self.output.write("{0}:{1}".format(self.timestamp.now,
                                                       line))
                    continue
                if rotation_expression.search(line):
                    self.logger.debug(("Start of rotation detected, "
                                       "event is set."))
                    self.rotation_start.set()
                    continue
                elif ('Rate table returned invalid' in line or
                      "The Turntable isn't responding" in line):
                    self.error_queue.put("Unable to oscillate: {0}".format(line))
                    raise OscillatorError(line)
                    
        except Exception as err:
            self.logger.error(err)
            self.error_queue.put(err)
        self.check_error(error)
        return

    def check_error(self, error):
        """
        Not fully implented yet.

        :param:

         - `error`: stderr file

        :raise: CommandError if detected
        """
        line = error.readline()
        if len(line):
            if "pthread_mutex_destroy" in line:
                self.error_queue.put(("Unable to grab the lock: "
                                      "Is the Oscillator already running?"))

            elif "Rate table returned invalid amount of data" in line:
                self.error_queue.put(line)
                #aise OscillatorError("Rate Table error")
            elif 'File "/usr/bin/oscillate"' in line:
                self.error_queue.put(line)
            elif "The Turntable isn't responding" in line:
                self.error_queue.put(line)
            else:
                self.logger.warning(line)
        return

    def generate_output(self, output, error):
        """
        :param:

         - `output`: stdout file
         - `error`: stderr file
        :yield: lines of stdout
        """
        for line in output:
            yield line
        self.check_error(error)
        return

    def stop(self):
        """
        :postcondition:

         - `stopped` is True
         - pkill(`oscillate`) called
         - rotate() called
        """
        command = 'oscillate;sleep 1;rotate 0 -k'
        with self.connection.lock:
            for line in self.generate_output(*self.connection.pkill(command)):
                if len(line):
                    self.logger.debug(line)
        self.stopped = True
        return

    def __call__(self, parameter=None):
        """
        :param:

         - `parameter`: not used

        :return: name
        :postcondition: thread is running, rotation_start is set
        """
        #import pudb;pudb.set_trace()
        for attempt in range(self.retries):
            if self.thread.is_alive():
                if self.block:
                    self.event.wait()
            else:
                self._thread = None
            # give the connection a chance to return an error
            self.logger.info("Sleeping to see if the turntable raises an error")
            self.sleep()
            if not self.error_queue.empty():
               self._thread = None
               if attempt == self.retries - 1:
                   message = "Unable to Oscillate: {0}".format(self.error_queue.get())
                   raise OscillatorError(message)
            if self._thread is not None:
                return self.name
        return self.name

    def __del__(self):
        """
        :postcondition: `stop` is called.
        :postcondition: connection is closed
        """
        try:
            self.stop()
            #self.connection.client.close()
        except ConnectionError:
            self.logger.debug("Connection Already closed")
        return

# end class Oscillator

class OscillateEvent(BaseClass):
    """
    An event to coordinate other commands with the start of a rotation
    """
    def __init__(self, event):
        """
        :param:

         - `event`: a python Event
        """
        super(OscillateEvent, self).__init__()
        self.event = event
        self.timeout = None
        return

    def is_set(self):
        """
        :return: True if the event is set, False otherwise.
        """
        return self.event.is_set()

    def wait(self, timeout=None):
        """
        :param:

         - `timeout`: if not None, stop blocking after timeout (seconds)

        :postcondition: event is cleared then waited for
        """
        self.event.clear()
        self.logger.info("Waiting for the start of the next rotation.")
        self.event.wait(timeout)
        return

    def __str__(self):
        return "Wait For Next Rotation Event"
# end class OscillateEvent

class OscillateStop(BaseClass):
    """
    A class to explicitly stop the Oscillator
    """
    def __init__(self, connection):
        """
        :param:

         - `connection`: a connection to the rotation master
        """
        super(OscillateStop, self).__init__()
        self.connection = connection
        return

    def check_output(self, output, error):
        for line in output:
            if len(line.strip()):
                self.logger.info(line)
        err = error.readline()
        if len(err):
            self.logger.error(err)
            return False
        return True

    def kill_and_rotate(self, sleep_time=1):
        """
        :param:

         - `sleep`: time to sleep between oscillate and rotate commands

        :postcondition: pkill oscillate and rotate 0 -k sent to connection
        :return: True if on stderr output, False otherwise
        """
        with self.connection.lock:
            output, error = self.connection.pkill("oscillate")
        if not self.check_output(output, error):
            return False
        sleep(sleep_time)
        output, error = self.connection.ps('-e')
        for line in output:
            if 'oscillate' in line:
                return False
        with self.connection.lock:
            output, error = self.connection.rotate("0 -k")
        return self.check_output(output, error)

    def __call__(self, parameter=None):
        """
        :param:

         - `parameter`: Not used

        :postcondition:
        """
        sleep_time = 5
        while not self.kill_and_rotate():
            message = "Sleeping {0} seconds and trying again.".format(sleep_time)
            self.logger.error(message)
            sleep(sleep_time)
            sleep_time += 1
        return
# end OscillateStop