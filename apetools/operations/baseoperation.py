
# this package
from apetools.baseclass import BaseClass


TOKEN_JOINER = "_"


class DummyOperation(BaseClass):
    """
    A dummy for an Test 
    """
    def __init__(self, *args, **kwargs):
        super(DummyOperation, self).__init__(*args, **kwargs)
        return

    def __call__(self, parameters=None, filename_prefix=None):
        """
        Logs the parameters
        """
        self.logger.debug(str(parameters))
        self.logger.debug(filename_prefix)        
        return

    def __getattr__(self, name):
        """
        Logs the attribute called

        :param:

         - `name`: name of attribute being called
        """
        self.logger.info("{0} called".format(name))
        return
# end class DummyOperation


class BaseOperation(BaseClass):
    """
    A Base operations holds the common elements operations
    """
    def __init__(self, products):
        """
        :param:

         - `products`: list of tools to call
        """
        super(BaseOperation, self).__init__()
        self._logger = None
        self.products = products
        return

    def __call__(self, parameters, filename_prefix=None):
        """
        :param:

         - `parameters` :namedtuple with settings to run the operation
         - `filename_prefix`: optional prefix to pass to the products
        :return: string of returned output from products
        """
        return_tokens = []
        for product in self.products:
            if filename_prefix is not None:
                returned = product(parameters, filename_prefix)
            else:
                returned = product(parameters)
            if returned:
                return_tokens.append(returned)
        return TOKEN_JOINER.join((str(token) for token in return_tokens))
#end class BaseOperation
