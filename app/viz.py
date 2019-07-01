# -*- coding: utf-8 -*-

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models.tools import TapTool
from bokeh.models.tools import HoverTool
from bokeh.models.tools import ResetTool
from bokeh.models.tools import SaveTool
from bokeh.models.tools import BoxZoomTool
from bokeh.models import DatetimeTickFormatter
import numpy as np
from datetime import datetime

from .utils import eval_code

TOOLS = [TapTool(), BoxZoomTool(),HoverTool(), ResetTool(), SaveTool(),]

FIG_WIDTH, FIG_HEIGHT = 500, 300


def create_data_plot(f):
    """Create plot of x [I] vs y [B/G].

    f: Function object
    """
    try:
        p = figure(tools=TOOLS, plot_height=FIG_HEIGHT, plot_width=FIG_WIDTH)
        x = f.data_x
        y = f.data_y
        xx = np.linspace(x.min(), x.max(), 100)
        yy = [eval_code(f, x=i)[-1] for i in xx]
        p.circle(x, y, size=6,
                 alpha=0.8,
                 color='magenta')
        p.line(xx, yy, color='blue', line_width=1.5, alpha=0.6, line_dash='solid')
        return components(p)
    except:
        return '<div></div>', '<div></div>'


def create_trend_plot(f):
    """Create plot for hit trend.

    f: Function object
    """
    try:
        x = f.hit_ts
        to_ts = np.vectorize(lambda x: (x - datetime(1970,1,1)).total_seconds())
        from_ts = np.vectorize(lambda x: datetime.utcfromtimestamp(x))

        hist, x_bins = np.histogram(to_ts(x))
        x_bins = 0.5*(x_bins[0:-1] + x_bins[1:])
        xx = from_ts(x_bins)
        yy = hist

        p = figure(tools=TOOLS, plot_height=FIG_HEIGHT, plot_width=FIG_WIDTH,
                   x_axis_type='datetime')
        p.xaxis.formatter = DatetimeTickFormatter(
                                minutes=["%H:%M %d/%b/%Y"],
                            )
        p.xaxis.major_label_orientation = np.pi/4
        p.vbar(x=xx, top=yy, width=3600, alpha=0.8, color='magenta')
        return components(p)
    except:
        return '<div></div>', '<div></div>'
