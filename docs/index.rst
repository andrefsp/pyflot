.. PyFlot documentation master file, created by
   sphinx-quickstart on Wed Sep 12 23:39:16 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PyFlot's documentation!
==================================

PyFlot provides an interface from Python to flot_.

.. _flot: http://www.flotcharts.org


::
     
    import flot
    class Fx(flot.Series):
        data = [(1, 2), (2, 3), (3, 4), (4, 5)]
     
    class MyGraph(flot.Graph):
        fx = Fx()
     
    my_graph = MyGraph()

::
    
    <html>
        <head>
            <script type="text/javascript" src='static/js/jquery.js'></script>
            <script type="text/javascript" src='static/js/jquery.flot.js'></script>
        </head>
        <body>
            <div id="gr" style="width:600px;height:300px;"></div>
        <script type='text/javascript'>
            $.plot($("#gr"), {{ my_graph.json_data|safe }}, {{ my_graph.options|safe }});
        </script>
        </body>
    </html>
    


Contents:

.. toctree::
   :maxdepth: 1
  
   introduction 
   installation 
   usage
   object-reference
   integrating-with-django


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


