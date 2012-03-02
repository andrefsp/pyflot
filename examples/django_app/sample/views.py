from django.views.generic import TemplateView

import flot

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs): 
        xy10 = flot.Series(x=flot.XVariable(points=range(1, 10)),
                           y=flot.YVariable(points=range(1, 10))) # x=y : 1<E<10

        xy20 = flot.Series(x=flot.XVariable(points=[i for i in range(1, 10)]),
                           y=flot.YVariable(points=[i*2 for i in range(1, 10)])) # x=y : 1<E<10

        context = {  
                    'graph1' : flot.Graph(series1=xy10, series2=xy20)
                }
        return context
