from pyflot import MissingDataException, DuplicateLabelException


class MultipleXAxisException(Exception):
    """
    This Exception is mean to be raised when there is multiple XFields
    in a Graph Object
    """

