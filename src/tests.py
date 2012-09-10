import datetime
import time
import unittest
try:
    import json
except ImportError:
    import simplejson as json

import flot


class SampleObject(object):
    ""

    def __init__(self, **kwargs):
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])


class S1(flot.Series):
    "Series for function y = x + 3"

    x = flot.XVariable()
    y = flot.YVariable()
    data = [SampleObject(x=i, y=i+3) for i in range(0, 10)]

    class Meta:
        label = 'series1'
        color = 'red'


class S2(flot.Series):
    "Series for function y = x"

    x = flot.XVariable()
    y = flot.YVariable()
    data = [SampleObject(x=i, y=i) for i in range(0, 10)]

    class Meta:
        label = 'series2'


class S3(flot.Series):
    "Series with no initial data"

    x = flot.XVariable()
    y = flot.YVariable()

    class Meta:
        label = 'series3'


class S4(flot.Series):
    "Series with X axis in time"

    var = flot.TimeXVariable()
    usr = flot.YVariable()
    data = [SampleObject(var=datetime.date(2011, 1, i), usr=i+10)\
                                                for i in range(1, 10)]


class OptionsTest(unittest.TestCase):
    "Test for the option global Option class"

    def test_options_check_for_allowed_options(self):
        # this object only allows
        options = flot.GraphOptions()
        key_val_list = [('x', 123), ('xaxis', [1,2,3])]
        for key, val in key_val_list:
            try:
                options[key] = val 
            except TypeError:
                # its fine
                pass
        options['xaxis'] = { 'format': '%d-%m-%y', 'mode': 'time' }

    def test_options_can_be_passed_through_constructor(self):
        options = flot.GraphOptions(xaxis={'mode': 'time'})
        self.assertTrue('xaxis' in options.keys())
        self.assertEquals(options['xaxis']['mode'], 'time')


class VariableTest(unittest.TestCase):
    "Variable test class"

    def test_receives_data(self):
        points = [x for x in range(0, 10)]
        my_var = flot.XVariable(points=points)
        self.assertEquals(my_var.points, points)


class TimeVariableTest(unittest.TestCase):
    "TimeVariable test class"

    def test_corrects_data(self):
        points = [datetime.date(2012, 1, i) for i in range(1, 10)]
        my_var = flot.TimeXVariable(points=points)
        time_points = [int(time.mktime(d.timetuple())*1000) for d in points]
        self.assertEquals(my_var.points, time_points)


class SeriesTest(unittest.TestCase):
    "Series test class"

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

    def test_options_van_be_passed_to_seties(self):
        series = S1(options=flot.SeriesOptions(bars={'show': True}))
        self.assertTrue('show' in series['bars'])
        self.assertTrue(series['bars']['show'])


class MyGraph(flot.Graph):
    "Graph Object"
    series1 = S1()
    series2 = S2()

    class Meta:
        options = flot.GraphOptions()


class GraphTest(unittest.TestCase):
    "Graph test class"

    def test_graph_builds_data(self):
        my_graph = MyGraph()
        graph_data_obj = json.loads(my_graph.json_data)
        x_graph_data1, y_graph_data1 = zip(*graph_data_obj[0]['data'])
        x_graph_data2, y_graph_data2 = zip(*graph_data_obj[1]['data'])
        self.assertEquals(list(x_graph_data1), S1()._x.points)
        self.assertEquals(list(y_graph_data1), S1()._y.points)
        self.assertEquals(list(x_graph_data2), S2()._x.points)
        self.assertEquals(list(y_graph_data2), S2()._y.points)

    def test_graph_receives_series_through_kwargs(self):
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

    def test_graph_set_axis_mode(self):
        my_graph = flot.Graph(series1=S4())
        self.assertEquals(my_graph._options['xaxis']['mode'], 'time')
        #self.assertEquals(my_graph._options['yaxis']['mode'], 'null')

    def test_graph_accepts_options(self):
        my_graph = flot.Graph(series1=S4(), options=flot.GraphOptions(xaxis={
                                                'mode': 'time',
                                                'format': '%d-%m-%y' 
                                                }))
        self.assertEquals(my_graph._options['xaxis']['mode'], 'time')
        self.assertEquals(my_graph._options['xaxis']['format'], '%d-%m-%y')


