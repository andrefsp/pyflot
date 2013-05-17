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
