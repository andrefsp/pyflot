
import datetime
from django.test import TestCase

from . import TimeFlotGraph, XField, Variable



class TimeDataObject(object):
    """
    Create a time mock sample object
    """
    def __init__(self, **kwargs):
        self.time = datetime.datetime.now()
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])


TimeDataIterable = [TimeDataObject(var=x) for x in xrange(0, 10)]


class SimpleTest(TestCase):

    class TestFlotTimeGraph(TimeFlotGraph):
        data = TimeDataIterable
        x = XField(field='time')
        y_axis = (
            Variable(field='var', label='Var'),
        )

    def setUp(self):
        self.graph = self.TestFlotTimeGraph()

    def test_1(self):
        print self.graph.series_json
        raise

