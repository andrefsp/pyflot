================
Object Reference
================

The main objects on PyFlot

Series
------

**Series**\(data=None, xpoints=None, ypoints=None, options=None,\*\*kwargs)

::
    
    class Series(dict):
        data = []
        _options = SeriesOptions() 
    

- data
    **data** argument ca be used to directly pass the data values to the Series.
   
::
     
    import flot
    flot.Series(data=zip(range(0,5), range(0,5)))
    

- xpoints, ypoints
   **xpoints** and **ypoints** can be used to pass directly the points on the x and y axis. Keep in mind that that they both need to be the same size.

::
    
    import flot
    flot.Series(xpoints=range(0, 5), ypoints=range(5,10))
    

- options
    **options** its what should be used to series costumization. Things like label or color can be configured using just by passning a ``SeriesOptions`` object on this argument.

::
    
    import flot
    flot.Series(xpoints=range(0, 5), ypoints=range(0,5),
                options=flot.SeriesOptions(label='y=x', color='red'))
    

If the series is being created by class definition, the options are set by the series *Meta* class attribute.

::
    
    import flot
    class Series(flot.Series):
        data = zip(range(0, 5),range(0, 5))

        class Meta:
            label = 'y=x'
            color = 'blue'

    
Graph
-----

This is a graph object
The graph object its meant to group one or more series objects so that it can be displayed on the page.

Assuming we have series such as:
:: 

    import flot
    series_a = flot.Series(data=[(1, 1), (2, 2) , (3, 3), (4, 4)])
    series_b = flot.Series(data=[(1, 2), (2, 3) , (3, 5), (4, 7)])
  

The series can be grouped on a Graph object by:

::
    flot.Graph(series1=series_a, series2=series_b)

or

::
    flot.Graph([series_a, series_b])



- options
    **options** its what should be used to graph display costumization. ``GraphOptions`` object.


