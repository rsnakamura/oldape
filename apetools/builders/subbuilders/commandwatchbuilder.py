
from basetoolbuilder import BaseToolBuilder, Parameters
from builderenums import BuilderParameterEnums

from apetools.watchers.commandwatcher import CommandWatcher


class CommandWatchBuilder(BaseToolBuilder):
    """
    The Command Watch Builder builds a command watcher
    """
    def __init__(self, *args, **kwargs):
        super(CommandWatchBuilder, self).__init__(*args, **kwargs)
        return

    @property
    def parameters(self):
        """
        :return: list of namedtuples
        """
        if self._parameters is None:
            if not any([p.name == BuilderParameterEnums.nodes for p in self.previous_parameters]):
                self.previous_parameters.append(Parameters(name=BuilderParameterEnums.nodes,
                                                           parameters=self.master.nodes.keys()))
        return self._parameters

    @property
    def product(self):
        """
        :return:
        """
        if self._product is None:
            self._product = CommandWatcher()
        return self._product
# end class CommandWatchBuilder
