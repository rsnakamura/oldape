
# python libraries
from collections import namedtuple
from string import lower

# apetools modules
from basetoolbuilder import BaseToolBuilder, Parameters
from apetools.lexicographers.config_options import ConfigOptions

from apetools.affectors.synaxxx.synaxxx import Synaxxx
from apetools.commands.poweron import PowerOn

from apetools.commons.errors import ConfigurationError


class PowerOnConfigurationError(ConfigurationError):
    """
    An error to raise if the user's configuration is wrong
    """
# end class PowerOnConfigurationError


class PowerOnBuilderEnum(object):
    """
    A holder of Synaxxx constants
    """
    __slots__ = ()
    id_switch = "id_switch"
    timeout = 'timeout'
    sleep = "sleep"
# end class PowerOnBuilderEnums


class PowerOnParameters(namedtuple("PowerOnParameters",
                                   "identifier switch".split())):
    __slots__ = ()

    def __str__(self):
        return "identifier: {0} switch: {1}".format(self.identifier,
                                                    self.switch)
# end class PowerOnParameters


class PowerOnBuilder(BaseToolBuilder):
    """
    A networked power-switch builder
    """
    def __init__(self, *args, **kwargs):
        super(PowerOnBuilder, self).__init__(*args, **kwargs)
        self._synaxxxes = None
        self._config_options = None
        self._clients = None
        return

    @property
    def synaxxxes(self):
        """
        :return: dict of <hostname>:<synaxxx>
        """
        if self._synaxxxes is None:
            self._synaxxxes = {}
            for identifier, param in self.config_options.iteritems():
                if identifier not in self._synaxxxes:
                    self._synaxxxes[identifier] = self.clients[param.hostname]
        return self._synaxxxes

    @property
    def clients(self):
        """
        :return: a dict of <hostname>: telnet-client
        """
        if self._clients is None:
            self._clients = {}
            for switch in self.config_options.itervalues():
                if switch.hostname not in self._clients:
                    if hasattr(switch, PowerOnBuilderEnum.sleep):
                        sleep = float(switch.sleep)
                    else:
                        sleep = 0

                    if hasattr(switch, PowerOnBuilderEnum.timeout):
                        timeout = float(switch.timeout)
                    else:
                        timeout = 1
                    self._clients[switch.hostname] = Synaxxx(switch.hostname,
                                                             sleep=sleep,
                                                             timeout=timeout)
        return self._clients

    @property
    def config_options(self):
        """
        :return: dictionary of <id>: <hostname, switch number>
        """
        if self._config_options is None:
            self._config_options = {}
            section = ConfigOptions.poweron_section
            identifiers = self.config_map.options(section)
            try:
                config_tuples = [self.config_map.get_namedtuple(section,
                                                                identifier,
                                                                converter=lower) 
                                                                for identifier in identifiers]
            except TypeError as error:
                self.logger.error(error)
                message = "Missing POWERON section in the config-file."
                raise PowerOnConfigurationError(message)
            self._config_options = dict(zip(identifiers, config_tuples))
            if not len(self._config_options):
                message = "Missing POWERON options (<ID>=hostname:<hostname>,switch:<switch ID>) in the config file"
                raise PowerOnConfigurationError(message)
        return self._config_options

    @property
    def product(self):
        """
        :return: PowerOn object
        """
        if self._product is None:
            self._product = PowerOn(self.synaxxxes)
        return self._product

    @property
    def parameters(self):
        """
        :return: list of named tuples
        """
        if self._parameters is None:
            parameters = []
            for identifier, param in self.config_options.iteritems():
                switch = param.switch

                parameters.append(PowerOnParameters(identifier=identifier,
                                                    switch=switch))
            name = PowerOnBuilderEnum.id_switch
            self.previous_parameters.append(Parameters(name=name,
                                                       parameters=parameters))
            self._parameters = self.previous_parameters
        return self._parameters
# end class PowerOnBuilder
