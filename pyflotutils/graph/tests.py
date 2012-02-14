try:
    import json
except ImportError:
    import simplejson as json

from django.test import TestCase

import graph
from exception import MultipleXAxisException


class SampleObject(object):
    """
    """
    def __init__(self, **kwargs):
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])


class S1(graph.Series):
    """
    Series for function y = x + 3
    """
    x = graph.XField()
    y = graph.YField()
    data = [SampleObject(x=i, y=i+3) for i in range(0, 10)]

    class Meta:
        label = 'series1'
        color = 'red'


class S2(graph.Series):
    """
    Series for function y = x
    """
    x = graph.XField()
    y = graph.YField()
    data = [SampleObject(x=i, y=i) for i in range(0, 10)]

    class Meta:
        label = 'series2'



class S3(graph.Series):
    """
    Series with no initial data
    """
    x = graph.XField()
    y = graph.YField()

    class Meta:
        label = 'series3'


class SeriesTest(TestCase):
    """
    """
    def test_series_has_attrs(self):
        series = S1()

        self.assertEquals(series._x, S1.x)
        self.assertEquals(series._y, S1.y)

        self.assertTrue(isinstance(series._y, graph.YField))
        self.assertTrue(isinstance(series._x, graph.XField))

    def test_series_has_data(self):
        series = S1()

        y_data = [getattr(obj, 'y') for obj in series.data]
        x_data = [getattr(obj, 'x') for obj in series.data]

        self.assertEquals(series._x.data, x_data)
        self.assertEquals(series._y.data, y_data)

        self.assertEquals(series['data'], zip(x_data, y_data))


    def test_checks_meta_attrs(self):
        series = S1()
        self.assertEquals(series['label'], 'series1')
        self.assertEquals(series['color'], 'red')



    def test_series_receives_data_in_kwargs(self):
        series = S3(data=[SampleObject(x=i, y=(-4*i)) for i in range(0, 10)])

        y_data = [getattr(obj, 'y') for obj in series.data]
        x_data = [getattr(obj, 'x') for obj in series.data]

        self.assertEquals(series['data'], zip(x_data, y_data))




class MyGraph(graph.Graph):
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

        self.assertEquals(list(x_graph_data1), S1()._x.data)
        self.assertEquals(list(y_graph_data1), S1()._y.data)

        self.assertEquals(list(x_graph_data2), S2()._x.data)
        self.assertEquals(list(y_graph_data2), S2()._y.data)


    def test_graph_receives_series_through_kwargs(self):
        """
        """
        sample_data = [SampleObject(x=i, y=i+10) for i in range(0, 10)]
        s3 = S3(data=sample_data)
        my_graph = graph.Graph(series1=S1(),
                                series2=S2(),
                                series3=s3)

        self.assertEquals(len(my_graph.series), 3)

        self.assertTrue(any([serie == S1() for serie in my_graph.series]))
        self.assertTrue(any([serie == S2() for serie in my_graph.series]))
        self.assertTrue(any([serie == s3 for serie in my_graph.series]))

