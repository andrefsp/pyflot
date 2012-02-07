import re
import time

import pyflot

from exception import MissingDataException
from exception import DuplicateLabelException


class XField(object):
    """
    This class will represent the `x` of an f(x) function
    """
    def __init__(self, field=None, **kwargs):
        if not field:
            raise Exception("XField must receive an field argument")

        self.field = field


class Variable(object):
    """

    """

    options = ('label', 'color', 'lines', 'bars', 'points',
              'xaxis', 'yaxis', 'clickable', 'hoverable', 'shadowSize')

    def __init__(self, field=None, *args, **kwargs):
        """

        """
        if not field:
            raise Exception("Variable must have a field")

        self.field = field

        for option in self.options:
            if option in kwargs:
                setattr(self, option, kwargs[option])



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

    data = None    # model to get data from
    x = ''     # field for the x axis
    y_axis = ()     # fields for the y axis


    def get_data(self, *args, **kwargs):
        pass

    def add_series(self, series=None):
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

        vals = dict([(y.field, list()) for y in self.y_axis])

        for sample in self.data:
            for y in self.y_axis:
                vals[y.field].append((getattr(sample, self.x.field), getattr(sample, y.field)))

        for y in self.y_axis:
            self.add_series(TimeSeries(data=vals[y.field], image=y))

