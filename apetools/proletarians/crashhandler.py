
# python
import traceback
from StringIO import StringIO

# apetools
from apetools.baseclass import BaseClass
from apetools.commons import storageoutput
from apetools.log_setter import LOGNAME


class CrashHandler(BaseClass):
    """
    The CrashHandler is called if the entire program crashes and collects crash information.
    """
    def __init__(self, arguments, *args, **kwargs):
        """
        :param:

         - `arguments`: The command line arguments given.
        """
        super(CrashHandler, self).__init__(*args, **kwargs)
        self.arguments = arguments
        return

    def run(self, error):
        """
        This is called when the program crashes.

        :param:

         - `error`: The error returned by the exception
        """
        self.logger.error("The program has crashed. I weep for you.")
        self.logger.error(error)
        output = storageoutput.StorageOutput("crash_report_{t}")
        output.move(LOGNAME)
        f = output.open("crashreport.log")
        separator = "*" * 20
        message = " Crash Report "
        header =  separator + message + separator
        footer = separator + separator + "*" * len(message)
        f.write(header + "\n")
        
        traceback.print_exc(file=f)
        f.write(footer + "\n")
        return
# end CrashHandler
