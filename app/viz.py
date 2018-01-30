# -*- coding: utf-8 -*-

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models.tools import TapTool
from bokeh.models.tools import HoverTool 
from bokeh.models.tools import ResetTool
from bokeh.models.tools import SaveTool
from bokeh.models.tools import BoxZoomTool
import numpy as np

from .utils import eval_code


TOOLS = [TapTool(), BoxZoomTool(),HoverTool(), ResetTool(), SaveTool(),]

def create_plot(f):
    # f: Function object
    try:
        p = figure(tools=TOOLS, plot_height=300, width=600)
        x = f.get_x()
        y = f.get_y()
        xx = np.linspace(x.min(), x.max(), 100)
        yy = [eval_code(f, x=i)[-1] for i in xx]
        p.circle(x, y, size=6,
                 alpha=0.8,
                 color='magenta')
        p.line(xx, yy, color='blue', alpha=0.6, line_dash='solid')
        return components(p)
    except:
        return '<div></div>', '<div></div>'
