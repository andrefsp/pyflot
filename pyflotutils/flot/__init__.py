import time
try:
    import json
except ImportError:
    import simplejson as json
from exception import MultipleAxisException


class Variable(object):
    "Genric Variable Object"

    def contribute_to_class(self, obj, attr_name, data=None):
        if getattr(obj, self._var_name, False):
            raise MultipleAxisException
        setattr(obj, self._var_name, self)
        if data:
            self._set_points(attr_name, data)


class XAxis(object):
    "X Axis Object"
    _var_name = '_x'


class YAxis(object):
    "Y Axis Object"
    _var_name = '_y'


class LinearVariable(Variable):
    "Linear Variable Object. No adjustment its done to the points"
    def __init__(self, points=None, **kwargs):
        if points is not None:
            self.points = points
   
    def _set_points(self, attr_name, data):   
        self.points = [getattr(sample, attr_name) for sample in data]


class TimeVariable(Variable):
    "Time Variable Object. Points content its adjusted" 
    def __init__(self, points=None, *kwargs):
        if points is not None:
            self.points = [int(time.mktime(point.timetuple()) * 1000)\
                                                    for point in points]

    def _set_points(self, attr_name, data):
        an = attr_name
        self.points = [int(time.mktime(getattr(s, an).timetuple()) * 1000)\
                            for s in data]


class XVariable(XAxis, LinearVariable):
    "Linear Variable on X Axis"


class YVariable(YAxis, LinearVariable):
    "Linear Variable on Y Axis"


class TimeXVariable(XAxis, TimeVariable):
    "Time Variable on X Axis"


class TimeYVariable(YAxis, TimeVariable):
    "Time Variable on Y Axis"


class Series(dict):
    "This class represents the actual flot series"

    _options = ('label',    # meta 
                'color',    # meta
                'lines',    # unknown  ****
                'bars',     # unknown  ****
                'points',   # unknown  ****
                'xaxis',    # meta
                'yaxis',    # meta
                'clickable',    # meta
                'hoverable',    # meta
                'shadowSize')   # meta


    def __init__(self, data=None, *args, **kwargs):
        """
        """
        if 'data' not in dir(self) and data is not None:
            # if not data is defined in Class def try to get is by args
            self.data = data
        # through class definition
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, Variable):
                attr.contribute_to_class(self, attr_name, self.data)
        # through kwargs
        for name, attr in kwargs.iteritems():
            if isinstance(attr, Variable):
                attr.contribute_to_class(self, name)
        self['data'] = zip(self._x.points, self._y.points)
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
        ""
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

    class Meta:
        pass

