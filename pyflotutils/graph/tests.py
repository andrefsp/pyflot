
import datetime

try:
    import json
except ImportError:
    import simplejson as json

from django.test import TestCase

from . import TimeFlotGraph, XField, YField
from exception import MultipleXAxisException


class TimeDataObject(object):
    """
    Create a time mock sample object
    """
    def __init__(self, **kwargs):
        self.time = datetime.datetime.now()
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])



class SimpleTest(TestCase):

    class TestFlotTimeGraph(TimeFlotGraph):
        "Must be everything fine with this one"
        data = [TimeDataObject(var=x, lib=x+1) for x in xrange(0, 5)]
        time = XField()
        var = YField(label='Var')
        lib = YField(label='Lib')


    class TestMultipleXTimeGraph(TimeFlotGraph):
        "Must Fail as it has two X Field objects"
        data = [TimeDataObject(var=x) for x in xrange(0, 10)]
        time = XField()
        var = XField()


    def test_assert_no_multiple_XFields(self):
        ""
        self.assertRaises(MultipleXAxisException,
                            self.TestMultipleXTimeGraph, None)


    def test_assert_multiple_variables(self):
        ""
        graph = self.TestFlotTimeGraph()
        self.assertEquals(len(graph._y), 2)

    def test_x_field_set__x(self):
        ""
        my_object = type('myobject', (), {})()

        XField().contribute_to_class(my_object)
        self.assertIsNotNone(getattr(my_object, XField.fieldname, None))


    def test_varible_field_append(self):
        ""
        my_object = type('myobject', (), {})()
        var1 = YField(label='var1')
        var2 = YField(label='var2')
        var1.contribute_to_class(my_object)
        var2.contribute_to_class(my_object)

        self.assertEquals(getattr(my_object, YField.fieldname, None),
                                                 [var1, var2])


    def test_construct_series(self):
        ""
        graph = self.TestFlotTimeGraph()
        print graph.series_json



