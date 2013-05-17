from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

register = template.Library()

class GraphRenderer(template.Node):
    """
    This template tag is mean to render the graph object on the template
    """
    def __init__(self, dom_id, graph, rest):
        self.graph = template.Variable(graph)
        self.dom_id = dom_id
        self.rest = rest

    def render(self, context):
        graph = self.graph.resolve(context)
        ctx = {
            'dom_id': self.dom_id,
            'rest': self.rest,
            'graph_data': graph.json_data,
            'graph_options': graph.options
        }
        return """
        <div id="%(dom_id)s" %(rest)s></div>
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
    tag_name = tokens.pop(0)
    dom_id = tokens.pop(0)
    graph = tokens.pop(0)
    rest = ''.join([" %s" % token for token in tokens])
    return GraphRenderer(dom_id, graph, rest)
