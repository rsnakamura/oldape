
#python
import re
import ConfigParser
from string import whitespace
from collections import namedtuple
from types import BooleanType

# apetools Libraries
from apetools.baseclass import BaseClass
from apetools.commons.errors import ConfigurationError
from apetools.commons import expressions
from timeconverter import TimeConverter


STRIP_LIST = "'\"" + whitespace
EMPTY_STRING = ''
DAY_STRING = 'day'
MINUTE_STRING = 'm'
HOUR_STRING = 'h'
SECOND_STRING = 'second'
COMMA = ','
FORWARD_SLASH = '/'
SEMICOLON = ";"

MINUTES = 60
HOURS = 60 * MINUTES
DAYS = 24 * HOURS

INTEGER = expressions.INTEGER
NAMED = expressions.NAMED
SPACES_OPTIONAL = expressions.SPACES_OPTIONAL
DASH = '-'

START_GROUP = "start"
END_GROUP = "end"
RANGE = re.compile(NAMED.format(name=START_GROUP, pattern=INTEGER) + SPACES_OPTIONAL +
                   DASH + SPACES_OPTIONAL + NAMED.format(name=END_GROUP, pattern=INTEGER))


class ConfigurationSectionError(ConfigurationError):
    """
    An error to raise if a section is missing
    """
    pass
# end class ConfigurationSectionError


class ConfigurationOptionError(ConfigurationError):
    """
    An error to raise if an option is missing
    """
    pass
# end class ConfigurationOptionError


class BooleanValues(object):
    """
    A class to hold the valid booleans.
    """
    __slots__ = ()
    true = "y yes 1 true t on".split()
    false = "n no 0 false f off".split()
    map = dict([(t, True) for t in true] + [(f, False) for f in false])
# end class Booleans


class ConfigurationMap(BaseClass):
    """
    The ConfigurationMap is a variant of SafeConfigParser that adds some extra methods
    """
    def __init__(self, filename, *args, **kwargs):
        """
        :param:

         - `filename`: The name of the config file.
        """
        super(ConfigurationMap, self).__init__(*args, **kwargs)
        self.filename = filename
        self._parser = None
        self._sections = None
        self._time_converter = None
        return

    @property
    def time_converter(self):
        """
        :return: Converter for space-separated time stream
        """
        if self._time_converter is None:
            self._time_converter = TimeConverter()
        return self._time_converter
    
    @property
    def sections(self):
        """
        :rtype: List
        :return: sections headings
        """
        if self._sections is None:
            self._sections = self.parser.sections()
        return self._sections

    def options(self, section, default=None, optional=True):
        """
        :param:

         - `section`: the section in the config file to check
         - `optional`: if True, returns default instead of raising an error
         - `default`: value to return if section doesn't exist and is optional
        
        :return: list of options in the section
        """
        try:
            return self.parser.options(section)
        except ConfigParser.NoSectionError as error:
            self.logger.debug(error)
            if optional:
                return default
            raise ConfigurationError("Unknown Section: {0}".format(section))
    
    @property
    def parser(self):
        """
        :return: SafeConfigParser
        """
        if self._parser is None:
            self._parser = ConfigParser.SafeConfigParser()
            self._parser.readfp(open(self.filename))
        return self._parser

    def raise_error(self, error):
        """
        Logs then raises a configuration error 
        """
        self.logger.debug(error)
        raise ConfigurationOptionError(error)


    def get(self, section, option, default=None, optional=False):
        """
        Eventually this will be a type-discovering method, but for now is a pass-through to _get
        """
        return self._get(section, option, default, optional)
    
    def _get(self, section, option, default=None, optional=False):
        """
        Convenience function:strip off extra quotes and whitespace after 'get'.

        :param:

         - `section`: The [section] name
         - `option`: the option in the section
         - `default`: returns default on error
         - `optional`: If True, return default if option not found

        :raise: ConfigurationError if the section or option doesn't exist and not optional
        """
        try:
            value = self.parser.get(section, option)
            return value.strip(STRIP_LIST)
        except ConfigParser.NoSectionError as error:
            raise ConfigurationSectionError(error)
        except ConfigParser.NoOptionError as error:
            if optional:
                return default
            self.logger.debug(error)
            raise ConfigurationError(error)
        return
    
    def get_boolean(self, section, option, default="", optional=False):
        """
        True = t, true, 1, y, yes, or on
        False = f, false, 0, n, no, or off

        Case-insensitive
        
        :raise: ConfigurationError if ConfigParser raises error or can't be coerced to boolean and not optional
        :return: section:option value cast to an boolean or default
        """
        value = self.get(section, option, default, optional)

        try:
            value = value.lower()
            return BooleanValues.map[value]
        except KeyError as error:
            self.logger.debug(error)
        except AttributeError as error:
            self.logger.debug(error)
            if type(value) is BooleanType:
                return value
        self.logger("Unknown Boolean: {0}".format(value))
        raise ConfigurationError(error)
        return

    def get_booleans(self, section, option, default="", optional=False, delimiter=COMMA):
        """
        True = t, true, 1, y, yes, or on
        False = f, false, 0, n, no, or off

        Case-insensitive
        
        :raise: ConfigurationError if ConfigParser raises error or can't be coerced to boolean and not optional
        :return: section:option value cast to an boolean or default
        """
        values = self.get_list(section=section, option=option, default=default, optional=optional, delimiter=delimiter)

        try:
            return [BooleanValues.map[value.lower()] for value in values]
        except KeyError as error:
            self.logger.debug(error)
            raise ConfigurationError("Unknown Boolean in: {0}".format(values))
        return

    def get_int(self, section, option, default=None, optional=False):
        """
        :raise: ConfigurationError if ConfigParser raises error or can't be coerced to int and not optional
        :return: section:option value cast to an int or default
        """
        try:
            return self.parser.getint(section, option)
        except (ValueError, ConfigParser.Error) as error:
            if optional:
                return default
            self.logger.debug(error)
            raise ConfigurationMap(error)

    def get_ints(self, section, option, default=None, optional=False, delimiter=COMMA):
        """
        :param:

         - `section`: the config file section name
         - `option` : the section-option name
         - `default`: value to return if not found and optional
         - `optional`: if True and not found, return default
         - `delimiter`: the separator for the integer values
         
        :raise: ConfigurationError if ConfigParser raises error or can't be coerced to int and not optional
        :return: List of section:option values cast to integers or default
        """
        try:
            return self.get_list(section=section, option=option, default=default, optional=optional, delimiter=delimiter,
                                    converter=int)
            
        except ValueError as error:
            values = self.get(section=section, option=option, default=default, optional=optional)
            self.logger.debug(error)
            raise ConfigurationError("Unable to cast '{0}' to integers".format(values))
        return
    
    def get_float(self, section, option, default=None, optional=False):
        """
        :raise: ConfigurationError if ConfigParser raises error or can't be coerced to float and not optional        
        :return: section:option value cast to a float or default
        """
        try:
            return self.parser.getfloat(section, option)
        except (ValueError, ConfigParser.Error) as error:
            if optional:
                return default
            self.logger.debug(error)
            raise ConfigurationError(error)

    def get_floats(self, section, option, default=None, optional=False, delimiter=COMMA):
        """
        :param:

         - `section`: the config file section name
         - `option` : the section-option name
         - `default`: value to return if not found and optional
         - `optional`: if True and not found, return default
         - `delimiter`: the separator for the integer values
         
        :raise: ConfigurationError if ConfigParser raises error or can't be coerced to float and not optional
        :return: List of section:option values cast to floats or default
        """
        try:
            return self.get_list(section=section, option=option, default=default, optional=optional, delimiter=delimiter,
                                    converter=float)
        except ValueError as error:
            values = self.get(section=section, option=option, default=default, optional=optional)
            self.logger.debug(error)
            raise ConfigurationError("Unable to cast '{0}' to floats".format(values))
        return

    def get_string(self, section, option, default=EMPTY_STRING, optional=False):
        """
        This returns what a ConfigParser.get returns
        
        :return: value string or default
        """
        return self._get(section, option, default, optional)

    def get_strings(self, section, option, default=None, optional=False, delimiter=COMMA):
        """
        This is the same thing as get_list
        
        :return: list of strings
        """
        return self.get_list(section=section, option=option, default=default, optional=optional, delimiter=delimiter)
    
    def get_list(self, section, option, default=None, optional=False, delimiter=COMMA, converter=str):
        """
        :param:

         - `section`: The [section] in the config file.
         - `option`: the option in the section
         - `delimiter`: the value separator
         - `optional`: if True, returns default instead of raising an error
        :return: list of strings stripped of whitespace

        :raises: ConfigurationError if not optional and not found.
        """
        values = self._get(section, option, default, optional)
        self.logger.debug("get_list converting: {0}".format(values))
        try:
            return [converter(value.strip()) for value in values.split(delimiter)]
        except AttributeError as error:
            self.logger.debug(error)
            if not optional:
                raise
            else:
                return default
        return
        
    def get_lists(self, section, option, default=None, optional=False, delimiter=COMMA, converter=str,
                  list_separator=SEMICOLON):
        """
        Don't make the delimiter and separator the same or you'll end up with each item in its own list
        :param:

         - `section`: The [section] in the config file.
         - `option`: the option in the section
         - `default`: value to return if optional and no value found
         - `optional`: if True, returns default instead of raising an error
         - `delimiter`: the value separator
         - `converter`: function to apply to the values
         - `separator`: delimiter between lists

        :return: list of list of strings stripped of whitespace (converted if `converter` supplied)

        :raises: ConfigurationError if not optional and not found.
        """
        values = self._get(section, option, default, optional)
        self.logger.debug("get_list converting: {0}".format(values))
        return [[converter(subvalue.strip()) for subvalue in value.split(delimiter)] for value in values.split(list_separator)]
    
    def get_dictionary(self, section, option, default=None, optional=False, delimiter=COMMA, converter=str,
                       key_value_separator=":"):
        """
        This expects a format of `{key:value, key:value}`

        The "{}" brackets are optional.
        
        :param:

         - `section`: The [section] in the config file.
         - `option`: the option in the section
         - `default`: what to return if fails and optional
         - `optional`: if True, returns defauln instead of raising an error
         - `delimiter`: what separates the different key:value pairs
         - `converter`: a function to apply to the value
         - `key_value_separator`: Token to separate key-value pairs
         
        :return: dictionary of key:value pairings

        :raises: ConfigurationError if not optional and not found.
        """
        values = self.get_list(section, option, default, optional)
        self.logger.debug("get_dictionary converting: {0}".format(values))
        values[0] = values[0].lstrip("{")
        values[-1] = values[-1].rstrip("}")
        values = [value.split(":") for value in values]
        values = [(pair[0], converter(pair[-1])) for pair in values]
        return dict(values)

    def get_dictionaries(self, section, option, default=None, optional=False, delimiter=COMMA, converter=str,
                         key_value_separator=":", dictionary_separator=SEMICOLON):
        """
        This expects a format of `{key:value, key:value}`

        For clarity dictionaries can be enclosed in braces ({}) but only the dictionary_separator is used
        
        :param:

         - `section`: The [section] in the config file.
         - `option`: the option in the section
         - `default`: what to return if fails and optional
         - `optional`: if True, returns defauln instead of raising an error
         - `delimiter`: what separates the different key:value pairs
         - `converter`: a function to apply to the value
         - `key_value_separator`: Token to separate key-value pairs
         - `dictionary_separator`: what separates the different dictionaries
         
        :return: list of dictionaries of key:value pairings

        :raises: ConfigurationError if not optional and not found.
        """
        values = self.get_lists(section, option, default, optional, delimiter=delimiter, list_separator=dictionary_separator)
        self.logger.debug("get_dictionary converting: {0}".format(values))
        dictionaries = []
        for line in values:
            line[0] = line[0].lstrip("{")
            line[-1] = line[-1].rstrip("}")
            line = [value.split(":") for value in line]
            line = [(pair[0], converter(pair[-1])) for pair in line]
            dictionaries.append(dict(line))
        return dictionaries

    def get_namedtuple(self, section, option, default=None, delimiter=COMMA, converter=str,
                       key_value_separator=":"):
        """
        This expects a format of `{key:value, key:value}`

        For clarity named-tuples can be enclosed in braces ({}) but only the dictionary_separator is used
        
        :param:

         - `section`: The [section] in the config file.
         - `option`: the option in the section
         - `default`: what to return if fails and optional
         - `optional`: if True, returns default instead of raising an error
         - `delimiter`: what separates the different key:value pairs
         - `converter`: a function to apply to the value
         - `key_value_separator`: Token to separate key-value pairs
         - `dictionary_separator`: what separates the different dictionaries
         
        :return: namedtuple with keys as properties and values as matching values

        :raises: ConfigurationError if not optional and not found.
    
        """
        source = self.get_dictionary(section=section, option=option, default=default, delimiter=delimiter,
                                     converter=converter, key_value_separator=key_value_separator)
        tuple_constructor = namedtuple(option, source.keys())
        return tuple_constructor(**source)
                       
    def get_range(self, section, option, default=None, optional=False, delimiter=DASH):
        """
        Converts values from `start - end` to [start...end] (expects integers)
        :param:

         - `section`: The [section] in the config file.
         - `option`: the option in the section
         - `delimiter`: the value separator
         - `optional`: if True, returns default instead of raising an error

        :return: list of values

        :raises: ConfigurationError if not optional and not found.
        """
        values = self._get(section, option, default, optional)
        start_end = values.split(delimiter)
        start, end = int(start_end[0]), int(start_end[-1])
        return [i for i in range(start, end + 1)]

    def get_ranges(self, section, option, delimiter=COMMA, optional=False, start_end_delimiter=DASH):
        """
        Converts a comma-delimited set of ranges (start-finish) to a list of integers.

        :param:

         - `section`: The [section] in the config file.
         - `option`: the option in the section
         - `delimiter`: the value separator
         - `optional`: if True, returns default instead of raising an error
         - `start_end_delimiter`: the token to separate the start and end of each range
        :return: list of values

        :raises: ConfigurationError if not optional and not found.

        :return: List of integers or None if optional is True and section not found.
        """
        values = self.get_list(section, option, delimiter, optional)
        if values is None:
            return values
        values_list = []
        for value in values:
            start_end = value.split(start_end_delimiter)
            try:            
                start, end = int(start_end[0]), int(start_end[1])
            except IndexError:
                start = end = int(start_end[0])
            values_list += [i for i in range(start, end + 1)]
        return values_list

    def __getattr__(self, *args, **kwargs):
        """
        Pass-through to the SafeConfigParser
        """
        self.parser(*args, **kwargs)
        return

    def get_times(self, section, option):
        """
        Gets a list then converts the values to times.
        """
        times = self.get_list(section, option)
        return [self.time_converter(time_with_units) for time_with_units in times]

    def get_time(self, section, option, default=0, optional=False):
        """
        :param:

         - `section`: A section in the config file (e.g. TEST)
         - `option`: An option in the section in the config file.
         - `default`: A default value to return if the option isn't in the file
         - `optional`: if True and time not found, return default

        :rtype: int or float
        :return: Value in the option (in seconds) or 0 if not present.
        """
        source = self._get(section, option, default, optional)
        if source == default:
            return source
        return self.time_converter(source)
    
    def time_in_seconds(self, time_with_units):
        """
        :return: time_with_units converted to seconds
        """
        time_with_units = time_with_units.lower()
        tokens = time_with_units.split()
        if len(tokens) == 1:
            return float(tokens[0])

        total = 0
        for index, token in enumerate(tokens):
            if DAY_STRING in token:
                total += float(tokens[index - 1]) * DAYS
                continue

            if HOUR_STRING in token:
                total += float(tokens[index - 1]) * HOURS
                continue

            if MINUTE_STRING in token:
                total += float(tokens[index - 1]) * MINUTES
                continue

            elif SECOND_STRING in token:
                total += float(tokens[index - 1])
        return total
# end ConfigurationMap
