Errors
======

A module to hold infrastructure errors.

Since the infrastructure is the highest level of exception catchers these errors aren't placed in the commons, as no one else is expected to catch them.

Although they are actually exceptions, they are called errors to avoid conflicts with python's built-in exceptions.

.. uml::

   Exception <|-- OperationError

.. module:: apetools.proletarians.errors
.. autosummary::
   :toctree: api

   OperationError

