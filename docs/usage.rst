=====
Usage
=====

There are several ways to create and plot graphs with pyflot. 


Examples
--------

Basic Example

::
    
    import flot
    
    class MySeries(flot.Series):
        data = [
            (1,2),
            (2,5),
            (3,7),
            (4,9),
        ]
    
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
    


You can also create graphs inline

::
    
    import flot
    
    series = flot.Series(data=[(1,2),(2,5),(3,7),(4,9)])
     
    my_graph = flot.Graph([series,]) 
    print my_graph.json_data
    print my_graph.options


As agraph is collection of series it is possible to:

::
    
    import flot
    
    series_a = flot.Series(data=[(1,2),(2,5),(3,7),(4,9)])
    series_b = flot.Series(data=[(4,5),(6,8),(1,4),(2,8)])
    my_graph = flot.Graph([series_a,series_b]) 
    print my_graph.json_data
    print my_graph.options



