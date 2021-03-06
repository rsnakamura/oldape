
# python libraries
import re

# tot lib
from apetools.baseclass import BaseClass
from apetools.commons import expressions
from apetools.commons import errors


ERROR_MESSAGE = "Unable to find address for {i}: {e}"


class GetIp(BaseClass):
    """
    A GetIp gets Ip addresses
    """
    def __init__(self, interface, connection, expression):
        """
        :param:

         - `interface`: The network interface name with the address
         - `connection`: A connection to the device with the interface
         - `expression`: The regular expression that matches the ip address.
        """
        super(GetIp, self).__init__()
        self.interface = interface
        self.connection = connection
        self._expression = None
        self.expression = expression
        return

    @property
    def expression(self):
        """
        :return: the compiled expression to match the IP address
        """
        return self._expression

    @expression.setter
    def expression(self, expr):
        """
        :param:

         - `expr`: A regular expression to match the ip address.
        """
        self._expression = re.compile(expr)
        return

    def run(self):
        """
        :return: The ip-address of the interface
        :raise: CommandError if no interface is found
        """
        output, error = self.connection.ifconfig(self.interface)
        for line in output:
            self.logger.debug(line)
            match = self.expression.search(line)
            if match:
                return match.group(expressions.ADDRESS_NAME)
        raise errors.CommandError(ERROR_MESSAGE.format(i=self.interface,
                                                       e=error.read()))
        return
# end class GetIp
