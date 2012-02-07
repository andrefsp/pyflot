import re
import time

import pyflot
import inspect

from exception import MissingDataException
from exception import DuplicateLabelException
from exception import MultipleXAxisException

class Field(object):
    """
    Generic Field class for graphs
    """

    def __init__(self, **kwargs):

        for option in self._options:
            if option in kwargs:
                setattr(self, option, kwargs.pop(option))


class XField(Field):
    """
    X Axis Field YField
    """
    _options = ()
    fieldname = '_x'

    def contribute_to_class(self, obj):
        if getattr(obj, self.fieldname, False):
            raise MultipleXAxisException
        setattr(obj, self.fieldname, self)

class YField(Field):
    """
    YField as a Image of an X Axis YField
    """
    _options = ('label', 'color', 'lines', 'bars', 'points',
             'xaxis', 'yaxis', 'clickable', 'hoverable', 'shadowSize')
    fieldname = '_y'

    def contribute_to_class(self, obj):
        if getattr(obj, self.fieldname, False):
            previous = getattr(obj, self.fieldname)
            previous.append(self)
            setattr(obj, self.fieldname, previous)
        else:
            setattr(obj, self.fieldname, [self])


class Series(dict):
    """
        This class represents the actual flot series
    """
    options = ('color', 'lines',
               'bars', 'points',
               'xaxis', 'yaxis',
               'clickable', 'hoverable', 'shadowSize')

    def __init__(self, data=None, image=None, *args, **kwargs):
        """
        """
        super(Series, self).__init__(*args, **kwargs)
        if not data:
            raise MissingDataException

        self['data'] = data
        self['label'] = image.label

        for option in self.options:
            if getattr(image, option, False):
                self[option] = getattr(image, option, False)


class TimeSeries(Series):

    def __init__(self, data=None, image=None, *args, **kwargs):
        """
            This will fix the data to display
        """
        super(TimeSeries, self).__init__(data=data, image=image, *args, **kwargs)
        self['data'] = [(int(time.mktime(ts.timetuple()) * 1000), val) \
                        for ts, val in data]  # fix data attribute for time


class TimeFlotGraph(pyflot.Flot):
    """

    """

    _options = {'mode' : 'time'}

    def get_data(self, *args, **kwargs):
        pass

    def add_series(self, series=None):
        """

        """
        if not series:
            raise Exception("add series receives a serie as argument")
        if series['label'] and \
            series['label'] in [x.get('label', None) for x in self._series]:
            raise DuplicateLabelException
        self._series.append(series)


    def __init__(self, *args, **kwargs):
        """

        """
        super(TimeFlotGraph, self).__init__()

        if not self.data:
            self.data = self.get_data(*args, **kwargs)

        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, Field):
                setattr(attr, 'field', attr_name)
                attr.contribute_to_class(self)


        #vals = dict([(y.field, []) for y in self._y])

        #for sample in self.data:
        #    for y in self._y:
        #        vals[y.field].append((getattr(sample, self._x.field), getattr(sample, y.field)))

        #for y in self._y:
        #    self.add_series(TimeSeries(data=vals[y.field], image=y))


