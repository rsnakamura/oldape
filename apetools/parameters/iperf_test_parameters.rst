Iperf Test Parameters
=====================

The Iperf Test Parameters are a place to add extra information that has to be passed in to the IperfCommand.

::

    class IperfTestParameters(namedtuple("IperfTestParameters", ["filename",
                                                                 "iperf_parameters"])):
        """
        IperfTestParameters add a filename to the iperf parameters.
        """
        def __str__(self):
            """
            :return: string representation of iperf_parameters
            """
            return str(self.iperf_parameters)
    # end class IperfTestParameters
    

