import flot
import math
import datetime
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        xy10 = flot.Series(x=flot.XVariable(points=range(1, 10)),
                           y=flot.YVariable(points=range(1, 10)),
                           options=flot.SeriesOptions(bars={'show': True},
                                                      label='y = 10*x'))

        xy20 = flot.Series(x=flot.XVariable(points=[i for i in range(1, 10)]),
                           y=flot.YVariable(points=[i*2 for i in range(1, 10)]),
                           options=flot.SeriesOptions(bars={'show': True},
                                                    label='y = 20*x',
                                                    color='green'))

        x_time_points = [datetime.date(2011, 1, i) for i in range(1, 20)]
        y_points = [float(1)/i for i in range(1, 20)]
        time1 = flot.Series(x=flot.TimeXVariable(points=x_time_points),
                            y=flot.YVariable(points=y_points),
                            options=flot.SeriesOptions(points={'show': True},
                                                        lines={'show': True},
                                                        label='y = 1/x',
                                                        color='blue'))

        graph_option = flot.GraphOptions(xaxis={'format': '%d/%m/%Y'})

        xpoints = map(math.radians ,range(1, 360))
        ypoints = map(math.sin, xpoints)
        sin_series = flot.Series(data=zip(xpoints, ypoints),
                            options=flot.SeriesOptions(label='sin(x)',
                                                       color='red'))

        last_series = flot.Series(xpoints=range(0, 10), ypoints=range(0, 10),
                                    options=flot.SeriesOptions(label='y = x'))

        context = {
                    'graph1': flot.Graph(series1=xy10, series2=xy20),
                    'graph2': flot.Graph(series1=time1, options=graph_option),
                    'sin_graph': flot.Graph(sin_series=sin_series),
                    'last_series': flot.Graph(last_series=last_series),
                    'all_series_graph': flot.Graph([xy10, xy20, last_series])
                }
        return context
