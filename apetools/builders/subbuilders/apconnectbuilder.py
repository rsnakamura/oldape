
from apetools.affectors.apconnect import APConnect
from apetools.lexicographers.config_options import ConfigOptions

from basetoolbuilder import BaseToolBuilder, Parameters
from builderenums import BuilderParameterEnums


class APConnectBuilder(BaseToolBuilder):
    """
    A class to build AP Connectors
    """
    def __init__(self, *args, **kwargs):
        super(APConnectBuilder, self).__init__(*args, **kwargs)
        self._ssids = None
        return

    @property
    def ssids(self):
        """
        :return: list of ssids from the config file
        """
        if self._ssids is None:
            self._ssids = self.config_map.get_list(ConfigOptions.apconnect_section,
                                                   ConfigOptions.ssids_option)
        return self._ssids

    @property
    def product(self):
        """
        :return: an APConnect
        """
        if self._product is None:
            self._product = APConnect(self.master.nodes)
        return self._product

    @property
    def parameters(self):
        """
        :return: namedtuple with `name` and `parameters` attribute
        """
        if self._parameters is None:

            if not any([p.name == BuilderParameterEnums.nodes for p in self.previous_parameters]):
                self.previous_parameters.append(Parameters(name=BuilderParameterEnums.nodes,
                                                           parameters=self.master.nodes.keys()))

            if not any([p.name == BuilderParameterEnums.ssids for p in self.previous_parameters]):
                self.previous_parameters.append(Parameters(name=BuilderParameterEnums.ssids,
                                                           parameters=self.ssids))

            self._parameters = self.previous_parameters
        return self._parameters
# end class APConnectBuilder
