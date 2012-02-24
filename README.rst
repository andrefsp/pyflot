======
pyflot
======

Introduction
============

The idea behing pyflot utils its to provide an easy and quick way to create graphs in python and to print them out in a web page.  

It uses the known `flot <http://code.google.com/p/flot/>`__ javaScript/jQuery plotting library as interface.


Usage
=====

I will do a couple of examples on how it works and how you can use it in your app.  
But first a quick briefing through the avalable flot objects.

- **XVariable** : A linear variable which will be tight to the X axis

- **YVariable** : A linear variable which will be tight to the Y axis

- **Series** : A series object its composed by one **XVariable**, one **YVariable** and one **data** object list which its where it gets the data from, we will go to that in a minute.

- **Graph** : The real thing! This is what we want to print out. A **Graph** object its composed by one or more **Series** objects. 

Examples
--------

1. This first example shows how to print a graph json data.

    ::
 
        import flot
        
        class MyObject(object):
            "A sample object model"
            def __init__(self, var=None, usr=None):
                self.var = var
                self.usr = usr  
        
        # let's create a list of objects  
        my_list = [MyObject(var=i, usr=i+1) for i in range(0, 5)]
        
        # create a Series object
        class MySeries(flot.Series):
            var = flot.XVariable()
            usr = flot.YVariable()
            data = my_list
        
            class Meta:
                label = 'my series'
                color = 'red'
        
        # now its time to create our 
        class MyGraph(flot.Graph):
            my_series = MySeries()
        
        # instantiate your graph
        my_graph = MyGraph()
        # the data should come out in 
        print my_graph.json_data 

The way it works its quite simple. *MyObject* has two attributes(``var``, ``usr``), and *my_list* its a list object containing 10 different *MyObject* instances.
When you create *MySeries* you literaly specify a ``var`` and ``usr`` attributes as *XVariable* and *YVariable*. So as this point, the new series will be created knowing that ``MyObject.var`` reffers to the X axis variable and ``MyObject.usr`` reffers to Y axis variable. From here the Series object its able o create the points for its X and Y axis and also to create its own data. 
 
Check MySeries()['data'], you must have something like:

[[0,1],[1,2],[2,3],[3,4],[4,5]]
 
