
# this package
from apetools.commons import errors
ConfigurationError = errors.ConfigurationError


MAX_PINS = 24


class FaucetteError(ConfigurationError):
    """
    A FaucetteError is raised if a configuration error is detected
    """
    def __init__(self, message=""):
        self.message = message
        return

    def __str__(self):
        message =  """!!!!!!!!!!!!!!!!!    You're blowin' it!     !!!!!!!!!!!!!
        
        {m}

        Allowed PIN IDs: 0 to {x}
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!""".format(m=self.message,
                                                                            x=MAX_PINS)
        return message
