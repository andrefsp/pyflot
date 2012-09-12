"""
`PyFlot` is a Python interface for the known `Flot` Javascript chart library
"""

__version__ = "0.1"
get_version = lambda : __version__

import time
try:
    import simplejson as json
except ImportError:
    import json

import exception

class BaseOptions(dict):
    "Base implementation for options"

    allowed_options = {}

    def __setitem__(self, key, value):
        """
        __setitem__ should only allow keys within allowed option keys
        and they have to batch the type
        """
        if not key.startswith('__'):
            if key not in self.allowed_options.keys():
                raise TypeError("%s is not a allowed option. Allowed "
                        "options are: %s" % (key, self.allowed_options.keys()))
            if not isinstance(value, self.allowed_options[key]):
                raise TypeError("Option %s got an unexpected object type" % key)
        super(BaseOptions, self).__setitem__(key, value)

    def __init__(self, *args, **kwargs):
        super(BaseOptions, self).__init__()
        for option, value in kwargs.items():
            if value:
                self[option] = value


class GraphOptions(BaseOptions):
    "Option object for graph"

    allowed_options = {
                        'xaxis': dict,
                        'yaxis': dict,
                        'legend': dict,
                        'grid': dict,
    }


class SeriesOptions(BaseOptions):
    """
        Options for Series object. This should be a completition of the
    normal json_data object
    """

    allowed_options  = {
            'label': basestring,
            'color': basestring,
            'xaxis': list,
            'yaxis': list,
            'lines': dict,
            'bars': dict,
            'points': dict,
            'clickable': bool,
            'hoverable': bool,
            'shadowSize': int,
            'highlightColor': basestring,
    }


class Variable(object):
    "Genric Variable Object"

    def contribute_to_class(self, obj, attr_name, data=None):
        if getattr(obj, self._var_name, False):
            raise exception.MultipleAxisException(
                                        "%s already set" % self._var_name)
        setattr(obj, self._var_name, self)
        if data:
            self._set_points(attr_name, data)


class Axis(object):
    "Generic Axis object"

    def __repr__(self):
        return self._var_name

    def __str__(self):
        return self._var_name


class XAxis(Axis):
    "X Axis Object"
    _var_name = '_x'


class YAxis(Axis):
    "Y Axis Object"
    _var_name = '_y'


class LinearVariable(Variable):
    "Linear Variable Object. No adjustment its done to the points"
    def __init__(self, points=None, **kwargs):
        if points is not None:
            self.points = points

    def _set_points(self, attr_name, data):
        self.points = []
        for sample in data:
            try:
                self.points.append(getattr(sample, attr_name))
            except AttributeError:
                s = {}
                s['_x'], s['_y'] = sample
                self.points.append(s[self._var_name])


class TimeVariable(Variable):
    "Time Variable Object. Points content its adjusted"
    def __init__(self, points=None, **kwargs):
        if points is not None:
            self.points = [int(time.mktime(point.timetuple()) * 1000)\
                                                    for point in points]

    def _set_points(self, attr_name, data):
        an = attr_name
        self.points = [int(time.mktime(getattr(s, an).timetuple()) * 1000)\
                                                    for s in data]
        self.points = []
        for sample in data:
            try:
                self.points.append(
                    int(time.mktime(getattr(sample, an).timetuple()) * 1000)
                )
            except AttributeError:
                s = {}
                s['_x'], s['_y'] = sample
                self.points.append(
                    int(time.mktime(s[self._var_name].timetuple()) * 1000)
                )


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

    _options = SeriesOptions()

    def _set_data(self):
        """
        This method will be called to set Series data
        """
        if getattr(self, 'data', False) and not getattr(self, '_x', False) and not getattr(self, '_y', False):
            _x = XVariable()
            _y = YVariable()
            _x.contribute_to_class(self, 'X', self.data)
            _y.contribute_to_class(self, 'Y', self.data)
            self['data'] = zip(self._x.points, self._y.points)
        else: 
            for axis in ('_x', '_y'):
                axis_obj = getattr(self, axis, False)
                if not axis_obj:
                    raise exception.MissingAxisException("%s missing" % axis)
                if not getattr(axis_obj, 'points', False):
                    raise exception.MissingDataException()

            self['data'] = zip(self._x.points, self._y.points)

    def __init__(self, data=None, xpoints=None, ypoints=None, options=None, *args, **kwargs):
        """
        Series should be able to get contructed and completed through
        class definition or through kwargs
        """
        #FIXME
        #   There should be a sanitizing method to take care of data, xpoints
        # and ypoints args. 
        self._options = SeriesOptions()
        super(Series, self).__init__()

        if 'data' not in dir(self) and data is not None:
            # if not data is defined in Class def try to get is by args
            self.data = data
        if data is None and xpoints is not None and ypoints is not None:
            # xpoints and ypoints were passed directly to Series object
            self.data = zip(xpoints, ypoints)

        # through class definition
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, Variable):
                attr.contribute_to_class(self, attr_name, self.data)

        # through kwargs
        for name, attr in kwargs.iteritems():
            if isinstance(attr, Variable):
                attr.contribute_to_class(self, name)
        
        # set series data
        self._set_data()

        # set series options
        for option in dir(self.Meta):
            self._options[option] = getattr(self.Meta, option)
        self.update(self._options)
        # options passed to the construction will overide Meta options
        if options is not None and isinstance(options, SeriesOptions):
            self.update(options)

    @property
    def json_series(self):
        "serializes a Series object"
        return json.dumps(self)

    class Meta:
        pass


class Graph(object):
    "Contains the data object and also the plot options"

    _series = []
    _options = GraphOptions()

    def __init__(self, series=None, options=None, **kwargs):
        "This contructor will be able to receive"
        self._series = []
        # set series
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, Series):
                self._series.append(attr)
        for arg in kwargs.values():
            if isinstance(arg, Series):
                self._series.append(arg)
        
        if series and all([isinstance(s, Series) for s in series]):
            self._series.extend(series)

        # set options through Meta
        for option in dir(self.Meta):
            self._options[option] = getattr(self.Meta, option)
        # check for options through argument
        if options and isinstance(options, GraphOptions):
            self._options.update(options)
        self._set_options()

    def _get_axis_mode(self, axis):
        "will get the axis mode for the current series"
        if all([isinstance(getattr(s, axis), TimeVariable) for s in self._series]):
            return 'time'
        return None

    def _set_options(self):
        "sets the graph ploting options"
        # this is aweful
        # FIXME: Axis options should be passed completly by a GraphOption
        if 'xaxis' in self._options.keys():
            self._options['xaxis'].update(
                        {'mode' : self._get_axis_mode(XAxis._var_name)})
        if 'yaxis' in self._options.keys():
            self._options['yaxis'].update(
                        {'mode' : self._get_axis_mode(YAxis._var_name)})

    @property
    def json_data(self):
        "returns its json data serialized"
        return json.dumps(self._series)

    @property
    def options(self):
        "returns its json option serialized"
        return json.dumps(self._options)

    class Meta:
        # meta should contain graph options, eg. xaxis, yaxis, legend
        pass

