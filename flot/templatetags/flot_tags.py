from random import choice
from django import template

register = template.Library()

class GraphRenderer(template.Node):
    """
    This template tag is mean to render the graph object on the template
    """
    def __init__(self, graph, attr_string, dom_id):
        self.graph = template.Variable(graph)
        self.attr_string = attr_string
        self.dom_id = dom_id

    def render(self, context):
        graph = self.graph.resolve(context)
        ctx = {
            'dom_id': self.dom_id,
            'attr_string': self.attr_string,
            'graph_data': graph.json_data,
            'graph_options': graph.options
        }
        return """
        <div %(attr_string)s></div>
        <script type='text/javascript'>
            $.plot($("#%(dom_id)s"), %(graph_data)s, %(graph_options)s);
        </script>
        """ % ctx

@register.tag
def plot(parser, token):
    """
    Tag to plot graphs into the template
    """

    tokens = token.split_contents()
    tokens.pop(0)
    graph = tokens.pop(0)

    attrs = dict([token.split("=") for token in tokens])

    if 'id' not in attrs.keys():
        attrs['id'] = ''.join([chr(choice(range(65, 90))) for i in range(0, 5)])
    else:
        attrs['id'] = attrs['id'][1:len(attrs['id'])-1]

    attr_string = ''.join([" %s=%s" % (k, v) for k, v in attrs.iteritems()])
    return GraphRenderer(graph, attr_string, attrs['id'])
