try:
    import json
except ImportError:
    import simplejson as json

from unittest import TestCase

import flot
from flot.exception import MultipleAxisException


class SampleObject(object):
    """
    """
    def __init__(self, **kwargs):
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])


class S1(flot.Series):
    """
    Series for function y = x + 3
    """
    x = flot.XVariable()
    y = flot.YVariable()
    data = [SampleObject(x=i, y=i+3) for i in range(0, 10)]

    class Meta:
        label = 'series1'
        color = 'red'


class S2(flot.Series):
    """
    Series for function y = x
    """
    x = flot.XVariable()
    y = flot.YVariable()
    data = [SampleObject(x=i, y=i) for i in range(0, 10)]

    class Meta:
        label = 'series2'


class S3(flot.Series):
    """
    Series with no initial data
    """
    x = flot.XVariable()
    y = flot.YVariable()

    class Meta:
        label = 'series3'


class VariableTest(TestCase):
    """

    """
    def test_receives_data(self):
        points = [x for x in range(0, 10)]
        my_field = flot.XVariable(points=points)
        self.assertEquals(my_field.points, points)


class SeriesTest(TestCase):
    """
    """
    def test_series_has_attrs(self):
        series = S1()

        self.assertEquals(series._x, S1.x)
        self.assertEquals(series._y, S1.y)

        self.assertTrue(isinstance(series._y, flot.YVariable))
        self.assertTrue(isinstance(series._x, flot.XVariable))


    def test_series_has_data(self):
        series = S1()

        y_points = [getattr(obj, 'y') for obj in series.data]
        x_points = [getattr(obj, 'x') for obj in series.data]

        self.assertEquals(series._x.points, x_points)
        self.assertEquals(series._y.points, y_points)

        self.assertEquals(series['data'], zip(x_points, y_points))


    def test_checks_meta_attrs(self):
        series = S1()
        self.assertEquals(series['label'], 'series1')
        self.assertEquals(series['color'], 'red')


    def test_series_receives_data_in_kwargs(self):
        series = S3(data=[SampleObject(x=i, y=(-4*i)) for i in range(0, 10)])

        y_data = [getattr(obj, 'y') for obj in series.data]
        x_data = [getattr(obj, 'x') for obj in series.data]

        self.assertEquals(series['data'], zip(x_data, y_data))


    def test_series_accept_field_objects_in_kwargs(self):
        x_points = [x for x in range(0, 10)]
        y_points = [y for y in range(10, 20)]

        x_field = flot.XVariable(points=x_points)
        y_field = flot.YVariable(points=y_points)

        series = flot.Series(xa=x_field, ya=y_field)

        self.assertEquals(series['data'], zip(x_points, y_points))
        self.assertEquals(series._x, x_field)
        self.assertEquals(series._y, y_field)


class MyGraph(flot.Graph):
    """
        Graph Object
    """
    series1 = S1()
    series2 = S2()


class GraphTest(TestCase):
    """
    """
    def test_graph_builds_data(self):
        """
        """
        my_graph = MyGraph()
        graph_data_obj = json.loads(my_graph.json_data)

        x_graph_data1, y_graph_data1 = zip(*graph_data_obj[0]['data'])
        x_graph_data2, y_graph_data2 = zip(*graph_data_obj[1]['data'])

        self.assertEquals(list(x_graph_data1), S1()._x.points)
        self.assertEquals(list(y_graph_data1), S1()._y.points)

        self.assertEquals(list(x_graph_data2), S2()._x.points)
        self.assertEquals(list(y_graph_data2), S2()._y.points)


    def test_graph_receives_series_through_kwargs(self):
        """
        """
        sample_data = [SampleObject(x=i, y=i+10) for i in range(0, 10)]
        s3 = S3(data=sample_data)
        my_graph = flot.Graph(series1=S1(),
                                series2=S2(),
                                series3=s3)

        self.assertEquals(len(my_graph._series), 3)

        self.assertTrue(any([serie == S1() for serie in my_graph._series]))
        self.assertTrue(any([serie == S2() for serie in my_graph._series]))
        self.assertTrue(any([serie == s3 for serie in my_graph._series]))


    def test_graph_accept_multiple_type_series(self):
        x_points = [i for i in range(30, 40)]
        y_points = [i for i in range(40, 50)]
        x_field = flot.XVariable(points=x_points)
        y_field = flot.YVariable(points=y_points)

        series1 = flot.Series(x=x_field, y=y_field)

        my_graph = MyGraph(s1=series1)

        self.assertTrue(any([serie == series1 for serie in my_graph._series]))
        self.assertTrue(any([serie == S1() for serie in my_graph._series]))
        self.assertTrue(any([serie == S2() for serie in my_graph._series]))
