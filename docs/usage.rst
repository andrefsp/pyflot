=====
Usage
=====

There are several ways to create and plot graphs with *PyFlot*.


Examples
--------

Basic Examples

::
    
    import flot
    
    class MySeries(flot.Series):
        data = [(1,2),(2,5),(3,7),(4,9),]
    
    class MyGraph(flot.Graph):
        my_series = MySeries()
    
    my_graph = MyGraph()
    print my_graph.json_data
    print my_graph.options
    



Its also possible to create ``Series`` objects by instatiating it inline

::
    
    import flot
    
    series = flot.Series(data=[(1,2),(2,5),(3,7),(4,9)])
    
    class MyGraph(flot.Graph):
        series = series
    
    my_graph = MyGraph()
    print my_graph.json_data
    print my_graph.options
    


You can also create ``Graph`` objects inline

::
    
    import flot
    
    series = flot.Series(data=[(1,2),(2,5),(3,7),(4,9)])
     
    my_graph = flot.Graph([series,]) 
    print my_graph.json_data
    print my_graph.options


A ``Graph`` object is may contain several ``Series`` objects, this way is possible on a single graph to plot more than one series. The next exmples shows how to

Inline example:
::
    
    import flot
    
    series_a = flot.Series(data=[(1,2),(2,5),(3,7),(4,9)])
    series_b = flot.Series(data=[(4,5),(6,8),(1,4),(2,8)])
    my_graph = flot.Graph([series_a,series_b]) 
    print my_graph.json_data
    print my_graph.options


Class declaration example:
::
    
    import flot
    
    class FirstSeries(flot.Series):
        data = [(1,2),(2,3),(3,4)]
    
    class SecondSeries(flot.Series):
        data = [(10,20),(20,30),(30,40)]
    
    
    class MyGraph(flot.Graph):
        first_series = FirstSeries()
        second_series = SecondSeries()
    
     
    my_graph = MyGraph()    
    print my_graph.json_data
    print my_graph.options



