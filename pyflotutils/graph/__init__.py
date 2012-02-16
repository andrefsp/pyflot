import time

try:
    import json
except ImportError:
    import simplejson as json

import pyflot
import inspect

from exception import MissingDataException
from exception import DuplicateLabelException
from exception import MultipleXAxisException
from exception import SeriesInvalidOptionException

class Field(object):
    """
    Generic Field class for graphs
    """

    _args = ('data',)
    
    def __init__(self, **kwargs):
        if len(kwargs) > 0:
            for arg in kwargs.keys():
                if arg in self._args:
                    setattr(self, arg, kwargs.pop(arg))
   
    def _set_data(self, attr_name, data):   
        self.data = [getattr(sample, attr_name) for sample in data]
        

    def contribute_to_class(self, obj, attr_name, data=None):
        if getattr(obj, self.fieldname, False):
            raise MultipleXAxisException
        setattr(obj, self.fieldname, self)
        if data:
            self._set_data(attr_name, data)

   

class XField(Field):
    """
    X Axis Field YField
    """

    fieldname = '_x'


class YField(Field):
    """
    YField as a Image of an X Axis YField
    """

    fieldname = '_y'


class Series(dict):
    """
        This class represents the actual flot series
    """

    _options = ('label', 
                'color', 
                'lines', 
                'bars', 
                'points',
                'xaxis', 
                'yaxis', 
                'clickable', 
                'hoverable', 
                'shadowSize')


    def __init__(self, *args, **kwargs):
        """
        """
        if 'data' not in dir(self):
            try:
                self.data = kwargs.pop('data')
            except KeyError:
                #raise MissingDataException
                pass

        # through function definition
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, Field):
                attr.contribute_to_class(self, attr_name, self.data)

        # through kwargs
        for name, attr in kwargs.iteritems():
            if isinstance(attr, Field):
                attr.contribute_to_class(self, name)

        self['data'] = zip(self._x.data, self._y.data)

        # set series options
        for option in dir(self.Meta):
            if option in self._options:
                self[option] = getattr(self.Meta, option)

        super(Series, self).__init__()

 
    @property
    def json_series(self):
        "serializes a Series object"
        return json.dumps(self)

    class Meta:
        pass


class Graph(object):
    """
    Contains the data object and also the plot options       
    """

    _series = []
    _options = {}

    def __init__(self, **kwargs):
        """

        """
        self._series = []
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, Series):
                self._series.append(attr)

        for arg in kwargs.values():
            if isinstance(arg, Series):
                self._series.append(arg)

    @property
    def json_data(self):
        "returns its json data serialized"
        return json.dumps([series for series in self._series])

    @property
    def options(self):    
        ""
        return json.dumps(self._options)


