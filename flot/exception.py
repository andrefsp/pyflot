
class MissingDataException(Exception):
    """This exception should be raised, when initializing a Series object
    no data is found either in` data` or both x and y axis points"""


class MissingAxisException(Exception):
    """This exception should be raise when a Series object doesn't have some
    axis information
    """


class MultipleAxisException(Exception):
    """This exception should be raise when repeated axis are found on the same
    Series object"""


class DuplicateLabelException(Exception):
    ""


class SeriesInvalidOptionException(Exception):
    ""

