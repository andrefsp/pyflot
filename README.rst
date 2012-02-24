=========
pyflot
=========

Introduction
------------

The idea behing pyflot utils its to provide an easy and quick way to create graphs in python and to print them out in a web page.  

It uses the known [linkref]: http://code.google.com/p/flot/ "flot" javaScript/jQuery plotting library as interface.


Usage
-----------

I will do a couple of examples on how it works and how you can use it in your app.
But first a quick briefing through the different objects.

- flot.__XVariable__ : A linear variable which will be tight to the X axis
- flot.__YVariable__ : A linear variable which will be tight to the Y axis

- flot.__Series__ : A series object its composed by one __XVariable__, one __YVariable__ and one __data__ object list which its where it gets the data from, we will go to that in 
a minute.

- flot.__Graph__ : The real thing! This is what we want to print out. A __Graph__ object its composed by __'N' Series__ objects. 


1. This first example shows how to print a graph json data.
 
    import flot

    class MyObject(object):
        "A sample object model"
        def __init__(self, **kwargs):
            for key, val in kwargs.iteritems():
                setattr(self, key, val)

    # let's create a list of objects
    my_list = [MyObject(var=i, usr=i+1) for i in range(0, 10)]

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
    


