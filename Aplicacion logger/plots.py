# plots.py

from bokeh.layouts import layout
from bokeh.models import (Range1d, ColumnDataSource, RangeTool,
                          LinearColorMapper, BasicTicker,
                          ColorBar, HoverTool, BoxSelectTool, Span, Paragraph,
                          DataRange1d)
from bokeh.models.widgets.tables import (NumberFormatter, DateFormatter,
                                         TableColumn, DataTable)
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.models.tickers import DatetimeTicker, FixedTicker
from bokeh.palettes import brewer, mpl, d3, Colorblind
from bokeh.plotting import figure
from bokeh.transform import jitter
from itertools import zip_longest
from logging import getLogger, NullHandler
from numpy import linspace, histogram, zeros, pi, polyfit, poly1d, isnan, array
from pandas import notnull, DataFrame, Series
from pandas.api.types import is_numeric_dtype, is_datetime64_any_dtype
from typing import Dict, Iterable, Tuple, Union, Sequence, List

# Add do-nothing handler to the module logger.
# This will prevent logged events being output in
# the absence of logging configuration by the user of the library.
getLogger(__name__).addHandler(NullHandler())

# color palettes
discrete_brewer = (brewer['Set2'][8] +
                   brewer['Set1'][9] +
                   brewer['Set3'][12] +
                   brewer['Dark2'][8])

discrete_d3 = (d3['Category20'][20][::2] +
               d3['Category20'][20][1::2])

discrete_dark = (d3['Category10'][10] +
                 brewer['Dark2'][8] +
                 Colorblind[8])

rainbow = [
    '#0034f8',
    '#0037f6',
    '#003af3',
    '#003df0',
    '#003fed',
    '#0041ea',
    '#0044e7',
    '#0046e4',
    '#0048e1',
    '#004ade',
    '#004cdb',
    '#004fd8',
    '#0051d5',
    '#0053d2',
    '#0054d0',
    '#0056cd',
    '#0058ca',
    '#005ac7',
    '#005cc4',
    '#005ec1',
    '#0060be',
    '#0061bb',
    '#0063b8',
    '#0065b6',
    '#0066b3',
    '#0068b0',
    '#006aad',
    '#006baa',
    '#006da7',
    '#006ea5',
    '#006fa2',
    '#00719f',
    '#00729d',
    '#00739a',
    '#007598',
    '#007695',
    '#077793',
    '#0d7890',
    '#13798e',
    '#187a8b',
    '#1c7b89',
    '#1f7c87',
    '#237d84',
    '#267e82',
    '#287f7f',
    '#2b807d',
    '#2d817b',
    '#2f8278',
    '#318376',
    '#328473',
    '#348571',
    '#35866f',
    '#36876c',
    '#37886a',
    '#388967',
    '#398a65',
    '#3a8b62',
    '#3b8c60',
    '#3c8e5d',
    '#3c8f5b',
    '#3d9058',
    '#3d9155',
    '#3e9253',
    '#3e9350',
    '#3e944d',
    '#3e954a',
    '#3e9647',
    '#3f9745',
    '#3f9842',
    '#3e993e',
    '#3e9a3b',
    '#3e9b38',
    '#3e9c35',
    '#3e9d32',
    '#3e9e2e',
    '#3e9f2b',
    '#3fa027',
    '#3fa124',
    '#40a221',
    '#41a31d',
    '#42a41a',
    '#44a517',
    '#45a615',
    '#47a713',
    '#4aa711',
    '#4ca80f',
    '#4fa90e',
    '#51a90d',
    '#54aa0d',
    '#57ab0d',
    '#5aab0d',
    '#5dac0d',
    '#5fad0d',
    '#62ad0e',
    '#65ae0e',
    '#67ae0e',
    '#6aaf0f',
    '#6db00f',
    '#6fb00f',
    '#72b110',
    '#74b110',
    '#77b211',
    '#79b211',
    '#7cb311',
    '#7eb412',
    '#80b412',
    '#83b512',
    '#85b513',
    '#88b613',
    '#8ab613',
    '#8cb714',
    '#8fb814',
    '#91b815',
    '#93b915',
    '#95b915',
    '#98ba16',
    '#9aba16',
    '#9cbb16',
    '#9fbb17',
    '#a1bc17',
    '#a3bc18',
    '#a5bd18',
    '#a7be18',
    '#aabe19',
    '#acbf19',
    '#aebf19',
    '#b0c01a',
    '#b2c01a',
    '#b5c11b',
    '#b7c11b',
    '#b9c21b',
    '#bbc21c',
    '#bdc31c',
    '#c0c31c',
    '#c2c41d',
    '#c4c41d',
    '#c6c51d',
    '#c8c51e',
    '#cac61e',
    '#cdc61f',
    '#cfc71f',
    '#d1c71f',
    '#d3c820',
    '#d5c820',
    '#d7c920',
    '#d9c921',
    '#dcca21',
    '#deca22',
    '#e0ca22',
    '#e2cb22',
    '#e4cb23',
    '#e6cc23',
    '#e8cc23',
    '#eacc24',
    '#eccd24',
    '#eecd24',
    '#f0cd24',
    '#f2cd24',
    '#f3cd24',
    '#f5cc24',
    '#f6cc24',
    '#f8cb24',
    '#f9ca24',
    '#f9c923',
    '#fac823',
    '#fbc722',
    '#fbc622',
    '#fcc521',
    '#fcc421',
    '#fcc220',
    '#fdc120',
    '#fdc01f',
    '#fdbe1f',
    '#fdbd1e',
    '#febb1d',
    '#feba1d',
    '#feb91c',
    '#feb71b',
    '#feb61b',
    '#feb51a',
    '#ffb31a',
    '#ffb219',
    '#ffb018',
    '#ffaf18',
    '#ffae17',
    '#ffac16',
    '#ffab16',
    '#ffa915',
    '#ffa815',
    '#ffa714',
    '#ffa513',
    '#ffa413',
    '#ffa212',
    '#ffa111',
    '#ff9f10',
    '#ff9e10',
    '#ff9c0f',
    '#ff9b0e',
    '#ff9a0e',
    '#ff980d',
    '#ff970c',
    '#ff950b',
    '#ff940b',
    '#ff920a',
    '#ff9109',
    '#ff8f08',
    '#ff8e08',
    '#ff8c07',
    '#ff8b06',
    '#ff8905',
    '#ff8805',
    '#ff8604',
    '#ff8404',
    '#ff8303',
    '#ff8102',
    '#ff8002',
    '#ff7e01',
    '#ff7c01',
    '#ff7b00',
    '#ff7900',
    '#ff7800',
    '#ff7600',
    '#ff7400',
    '#ff7200',
    '#ff7100',
    '#ff6f00',
    '#ff6d00',
    '#ff6c00',
    '#ff6a00',
    '#ff6800',
    '#ff6600',
    '#ff6400',
    '#ff6200',
    '#ff6100',
    '#ff5f00',
    '#ff5d00',
    '#ff5b00',
    '#ff5900',
    '#ff5700',
    '#ff5500',
    '#ff5300',
    '#ff5000',
    '#ff4e00',
    '#ff4c00',
    '#ff4a00',
    '#ff4700',
    '#ff4500',
    '#ff4200',
    '#ff4000',
    '#ff3d00',
    '#ff3a00',
    '#ff3700',
    '#ff3400',
    '#ff3100',
    '#ff2d00',
    '#ff2a00']

brewer_sets_123 = (brewer['Set1'][9] + brewer['Set2'][8] + brewer['Set3'][10][
                                                           2:][::-1]) * 10
brewer_sets_12 = (brewer['Set1'][9] + brewer['Set2'][8]) * 10
brewer_sets_23 = (brewer['Set2'][8] + brewer['Set3'][12]) * 10
palette_dark = (brewer['Dark2'][8] + brewer['Set2'][8] + Colorblind[8] +
                d3['Category10'][10])
red_to_green = (brewer['YlOrBr'][9] +
                brewer['YlGn'][9][::-1])



def heatmap(obj: DataFrame,
            xvar: str,
            yvar: str,
            value: str,
            width: int = None,
            height: int = None,
            hoover_format: Iterable[Tuple[str, str]] = None,
            color_low: Union[int, float] = None,
            color_high: Union[int, float] = None,
            title: str = None,
            colorbar: bool = True,
            xrange: Sequence = None,
            yrange: Sequence = None,
            palette: Union[str, List] = None,
            reverse: bool = False) -> figure:
    """Plot heatmap.

    :param obj: input data.
    :param xvar: column from input data to on x axis.
    :param yvar: column from input data to plot on y axis.
    :param value: column from input data (of format int or float) to format the colors.
    :param width: width of plot.
    :param height: height of plot.
    :param hoover_format: variables to include in the hoover tool. Default None.
                    v.g. [('label1', '@column_name1'), ('label2', '@column_name2')]
    :param color_low: value in data to match with the end of the color map.
    :param color_high: value in data to match with the start of the color map.
    :param title: title of plot. Default None.
    :param colorbar: plot color bar to the right of the plot.
    :param xrange: list of x axis tickers.
    :param yrange: list of y axis tickers.
    :param palette: name of color palette or list of HEX color codes.
    Default None. If None the palette brewer 'orange-yellow-green' is used.
    Accepts any brewer palette name that contains at least a 9 colours.
    :param reverse: reverse color mapping.
    :return: bokeh figure.
    :author: Tecnalia Research and Innovation (Miguel Esteras and Sandra Riaño).
    """
    obj.fillna(0, inplace=True)
    # set low and high threshold for color map
    color_low = color_low or obj[value].min()
    color_high = color_high or obj[value].max()
    # continuous colormap from list of colours
    c = (brewer[palette][9]
         if isinstance(palette, str)
         else (palette or mpl['Viridis'][256]))
    c = c[::-1] if reverse else c
    mapper = LinearColorMapper(palette=c, low=color_low, high=color_high)

    # define axis range
    obj[xvar] = obj[xvar].astype(str)
    obj[yvar] = obj[yvar].astype(str)
    xrange = xrange or obj[xvar].unique()
    yrange = yrange or obj[yvar].unique()

    width = width or int(20 * len(xrange)) + 400
    height = height or int(20 * len(yrange)) + 400

    title = title or f'Heatmap | {xvar} - {yvar}'

    p = figure(title=title, x_range=xrange, y_range=yrange,
               plot_width=width, plot_height=height, tools='box_zoom,reset',
               toolbar_location=None, tooltips=hoover_format)
    # figure theme
    p.title.text_font_size = "12pt"
    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_text_font_size = "10pt"
    p.axis.major_label_standoff = 0
    p.xaxis.major_label_orientation = 1
    p.xaxis.axis_label = xvar
    p.yaxis.axis_label = yvar
    p.min_border_left = 50
    p.min_border_right = 50
    p.min_border_top = 50
    p.min_border_bottom = 50

    # plot data
    p.rect(x=xvar, y=yvar, width=1, height=1, source=obj,
           fill_color={'field': value, 'transform': mapper}, line_color=None)
    # plot color bar
    if colorbar:
        color_bar = ColorBar(color_mapper=mapper,
                             major_label_text_font_size="10pt",
                             ticker=BasicTicker(desired_num_ticks=10),
                             title=f'{value}',
                             label_standoff=10, border_line_color=None,
                             location=(0, 0))
        p.add_layout(color_bar, 'right')
    return p


def histograms(obj: Union[DataFrame, Series],
               bins: int = 10,
               width: int = None,
               height: int = None,
               groupby: Union[str, Series] = None,
               title: str = None,
               color: Union[str, Iterable[str]] = None,
               hoover: bool = True,
               **kwargs) -> figure:
    """Create a histogram figure for each column in obj that are of type bool, int or float.

    :param obj: input data.
    :param groupby: name of column to group columns in independent correlation matrices.
    :param width: width of plot in pixels.
    :param height: height of plot in pixels.
    :param title: title of plot.
    :param color: color or palette of colors to use in the plot.
    :param bins: number of bins in histograms.
    :param hoover: include a hoover tool. Default True.
    :return: bokeh figure
    :author: Tecnalia Research and Innovation (Miguel Esteras and Sandra Riaño)
    """
    logger = getLogger(__name__)
    groups = obj[groupby] if groupby else None
    source = obj.drop(groupby, axis=1) if groupby else obj.copy()
    source = source.select_dtypes(include=['bool', 'float'])
    if source.shape[1] > 1:
        list_of_plots = [histograms(source[col], title=col,
                                    width=width or 300,
                                    height=height or 200,
                                    hoover=hoover,
                                    groupby=groups,
                                    color=color, bins=bins)
                         for col in source]
        n = kwargs.pop('n_columns', None) or min([3, source.shape[1]])
        return plots_to_grid(plots=list_of_plots, n_columns=n)

    title = title or obj.name or ''

    # x range
    xmin, xmax = float(min(source)), float(source.max())
    xpad = abs(abs(xmin) - abs(xmax)) * 0.05
    xrange = (xmin - xpad, xmax + (xpad * 2))

    p = figure(title=title, tools='box_zoom,reset',
               background_fill_color="white",
               plot_height=height or 600, plot_width=width or 800,
               toolbar_location='above', x_range=xrange)
    data = [(title, obj)] if groupby is None else [(str(key), df) for key, df
                                                   in source.groupby(groups)]
    color = color or brewer_sets_123
    for c, (name, sample) in zip(color, data):
        hist, edges = histogram(sample.dropna().values, bins=bins)
        source = ColumnDataSource(
            data=dict(values=hist, left=edges[:-1], right=edges[1:]))
        gly = p.quad(top='values', bottom=0, left='left', right='right',
                     fill_color=c, line_color="white", source=source,
                     legend_label=str(name))
        if hoover:
            p.add_tools(HoverTool(renderers=[gly],
                                  tooltips=[('Freq(x)', '@values')],
                                  toggleable=False))
    p.y_range.start = 0
    p.xaxis.axis_label = 'x'
    p.yaxis.axis_label = 'Freq(x)'
    p.grid.grid_line_color = '#eeeeee'
    # borders
    p.min_border_left = 40
    p.min_border_right = 40
    p.min_border_top = 40
    p.min_border_bottom = 40
    # legend
    p.legend.click_policy = 'hide'
    p.legend.location = 'top_right'
    p.legend.label_text_font_size = '6pt'
    p.legend.background_fill_color = "#ffffff"
    p.legend.background_fill_alpha = 1
    p.legend.label_text_line_height = 1
    p.legend.spacing = 0

    return p


def correlation(obj: DataFrame, method: str = 'spearman',
                plot_unique: bool = True,
                width: int = None, height: int = None, title: str = None,
                groupby: str = None,
                color_palette: Iterable[str] = None, add_text: bool = True,
                hoover: bool = True, **kwargs) -> figure:
    """Plot correlation matrix between columns in pandas data frame.

    :param obj: input data
    :param method: correlation method. Default 'spearman'. Accepted values are 'spearman',
            ‘pearson’, ‘kendall’.
    :param groupby: name of column to group columns in independent correlation matrices.
    :param plot_unique: plot unique correlation pairs only (triangular shape).
    :param width: width of plot in pixels.
    :param height: height of plot in pixels.
    :param title: title of plot.
    :param color_palette: color palette for plot.
    :param add_text: print the correlation coefficient inside each square.
    :param hoover: add hoover tool to plot.
    :return: bokeh figure
    :author: Tecnalia Research and Innovation (Miguel Esteras and Sandra Riaño)
    """
    logger = getLogger(__name__)
    if groupby:
        list_of_plots = [
            correlation(df, method=method, plot_unique=plot_unique,
                        title=str(key),
                        width=width or 200, height=height or 200,
                        hoover=hoover,
                        add_text=False, color_palette=color_palette)
            for key, df
            in obj.groupby(groupby)]
        n_columns = kwargs.pop('n_columns', None) or 3
        return plots_to_grid(list_of_plots, n_columns)

    corr = (obj
            .reindex(sorted(obj.columns), axis=1)
            .select_dtypes(include=['int', 'float'])
            .corr(method=method))
    n = corr.shape[1]
    source = (corr
              .stack()
              .reset_index()
              .rename({'level_0': 'x', 'level_1': 'y', 0: 'stat'}, axis=1))

    if plot_unique:
        # remove duplicate pairs of features
        source = source.groupby(
            source['x'].apply(hash) + source['y'].apply(hash)).first()

    # format rho value to string
    source.insert(0, 'stat_str', source.stat.map('{:+.2f}'.format))
    color_palette = color_palette or brewer['RdYlBu'][11]
    mapper = LinearColorMapper(palette=color_palette,
                               low=source['stat'].min(),
                               high=source['stat'].max())
    # create figure and hoover tool
    xrange = sorted(set(source['x'].values))
    yrange = xrange[::-1]

    p = figure(title=title, plot_width=width or n * 40,
               plot_height=height or n * 40,
               x_range=xrange, y_range=yrange, toolbar_location=None)
    # plot data
    gly = p.rect('x', 'y', .9, .9, source=source, fill_alpha=0.5,
                 fill_color={'field': 'stat', 'transform': mapper})
    if add_text:
        p.text('x', 'y', text='stat_str', source=source, text_align="center",
               text_baseline="middle", text_font_size='8pt')
    if hoover:
        p.add_tools(HoverTool(renderers=[gly], toggleable=False,
                              tooltips=[("x", "@x"), ("y", "@y"),
                                        ("stat", "@stat_str")]))
    # format plot
    p.outline_line_color = None
    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_standoff = 0
    p.xaxis.major_label_orientation = 0.8
    p.yaxis.major_label_orientation = 0.8
    return p


def time_lines(obj: Union[DataFrame, Series],
               yvar: Union[str, Iterable[str]] = None,
               xvar: str = None,
               xrange: Iterable = None,
               yrange: Iterable = None,
               groupby: str = None,
               highlight: Union[str, Iterable[str]] = None,
               line_width: float = 1,
               color: str = None,
               color_palette: List[str] = None,
               height: int = 400, width: int = 1600,
               legend_location: str = 'top_right',
               title: str = None, toolbar: str = 'xpan,box_zoom,reset',
               hoover: bool = True,
               hoover_tips: Iterable[Tuple[str, str]] = None) -> figure:
    """Creates a time series line plot.

    :param obj: input data.
    :param yvar: columns names in data to plot in the y axis.
    :param xvar: column or index name to plot in the x axis. Default None. If None the index
                will plot on the x axis.
    :param xrange: x range in the format (min, max) or bokeh.figure.x_range. Default None.
                If None the x axis shows the first 1/10 of the x variable data.
    :param yrange: y range in the format (min, max). If None the default y axis range is shown.
    :param groupby: name of column to used to group the data. If None data is not grouped.
    :param highlight: columns names of variables in the y axis to be ploted with a thicker line.
    :param line_width: width of lines.
    :param color: color of line.
    :param color_palette: palette of color as list of HEX codes to use in case of more than one
            group of data or variable per plot. Default None. In None, a comination of brewer
            palettes is used.
    :param height: height of plot in pixels. Default 400.
    :param width: width of plot in pixels. Default 1600.
    :param legend_location: legend location.
    :param title: title of plot. Default None. If None the title is a list of the names of the
                variables plotted in the y axis.
    :param toolbar: tools to include in the tool bar.
    :param hoover: include a hoover tool. Default True.
    :param hoover_tips: variables to include in the hoover tool. Default None. If None the
                hoover tool shows the y axis value. v.g. [('label', '@column_name')]
    :return: bokeh figure.
    :author: Tecnalia Research and Innovation (Miguel Esteras and Sandra Riaño)
    """

    logger = getLogger(__name__)
    # transform strings to list of strings
    yvar = (([yvar] if isinstance(yvar, str) else yvar) if yvar
            else (list(obj.columns) if isinstance(obj, DataFrame)
                  else ([obj.name or 0])))
    highlight = list(highlight) if highlight else []
    # define x variable
    obj.index.name = obj.index.name or 'index'
    xvar = xvar or obj.index.name
    df = obj.reset_index()
    # define x range
    if xrange is None:
        xr = sorted(set(df[xvar]))
        xrange = (xr[0], xr[int(len(xr) / 5)])
    # plot only the time component of datetime variables in the y axis
    ydtype = 'auto'
    for dtvar in [y for y in yvar if is_datetime64_any_dtype(df[y])]:
        df[dtvar] = df[dtvar].dt.time
        ydtype = 'datetime'
    # define title
    t = title or "; ".join([str(x) for x in yvar])
    # create figure
    p = figure(plot_height=height, plot_width=width, tools=toolbar,
               toolbar_location='above', y_axis_type=ydtype,
               x_axis_type="datetime", background_fill_color="#f8f9f9",
               x_range=xrange, title=t)
    # plot data
    color_palette = color_palette or palette_dark
    for col, c in zip(yvar, color_palette):
        if groupby:
            groups = df[groupby].unique()
            for g, cc in zip(groups, color_palette):
                source = df[df[groupby] == g].rename(columns={col: 'y'})
                if source['y'].empty or source['y'].isnull().all():
                    continue
                w = 4 if g in highlight else line_width
                gly = p.line(x=xvar, y='y', line_color=color or cc,
                             line_width=w, source=source, legend_label=str(g))
                if hoover:
                    tips = hoover_tips or [('value', '@y')]
                    p.add_tools(HoverTool(renderers=[gly], tooltips=tips,
                                          toggleable=False))
        else:
            source = df.rename(columns={col: 'y'})
            if source['y'].empty or source['y'].isnull().all():
                continue
            w = 4 if col in highlight else line_width
            gly = p.line(x=xvar, y='y', line_color=color or c,
                         line_width=w, source=source, legend_label=str(col))
            if hoover:
                tips = hoover_tips or [('value', '@y')]
                p.add_tools(HoverTool(renderers=[gly], tooltips=tips,
                                      toggleable=False))
    # title format
    p.title.text_font_size = '10pt' if title else '0pt'
    # x axis format
    p.xaxis.ticker = DatetimeTicker(desired_num_ticks=int(width / 100))
    p.xaxis.formatter = DatetimeTickFormatter(days=["%d-%b-%y"])

    # y axis format
    if yrange:
        p.y_range = yrange if isinstance(yrange, DataRange1d) else Range1d(
            *yrange)

    # legend format
    p.legend.click_policy = 'hide'
    p.legend.location = legend_location
    p.legend.label_text_font_size = '8pt'
    p.legend.background_fill_color = "#ffffff"
    p.legend.background_fill_alpha = 1
    p.legend.label_text_line_height = 1
    p.legend.spacing = 1
    # borders
    p.min_border_bottom = 50
    p.min_border_left = 50
    return p


def time_lines_and_dots(obj: Union[Series, DataFrame],
                        yvar: Union[List[str], str] = None,
                        xvar: str = None,
                        xrange: Tuple[float, float] = None,
                        yrange: Tuple[float, float] = None,
                        groupby: str = None,
                        line_color: str = None,
                        line_color_palette: List[str] = None,
                        line_width: float = 1,
                        dots_color: str = None,
                        dots_color_palette: List[str] = None,
                        dots: Union[Series, DataFrame] = None,
                        dots_groupby: str = None,
                        dots_xvar: Union[List[str], str] = None,
                        dots_yvar: Union[List[str], str] = None,
                        dots_size: float = 10,
                        height: float = 400, width: float = 1600,
                        title: str = None,
                        hoover: bool = True, hoover_tips=None,
                        toolbar: str = 'xpan,box_zoom,reset',
                        legend_location: str = 'top_right') -> figure:
    """Plot a combination of time series line and scatter graph.

    :param obj: input table for line plot.
    :param yvar: column name or list of column names from the input table to plot on the y axis.
    :param xvar: column name from table to plot on the x axis. Default None. If None, the index
            of the input table will be plotted on the x axis.
    :param xrange: range of x axis in format (min, max).
    :param yrange: range of y axis in format (min, max).
    :param groupby: name of column in input table to use to group samples in plot.
    :param line_color_palette: palette of color as list of HEX codes to use in case of more than
            one group of data or variables per plot. Default None. In None, a combination of brewer
            palettes is used.
    :param line_width: width of lines.
    :param dots_color_palette: palette of color as list of HEX codes to use in case of more than
            one group of data or variables per plot. Default None. In None, a combination of brewer
            palettes is used.
    :param dots: input table for scatter plot.
    :param dots_yvar: column name or list of column names from input scatter table to plot on the y axis.
    :param dots_size: size of dots.
    :param dots_groupby: name of column in input scatter table to use to group samples in plot.
    :param dots_xvar: column name from dots table to plot on the x axis. Default None. If None,
            the index of the input dots table will be plotted on the x axis.
    :param height: height of figure in pixels.
    :param width: width of figure in pixels.
    :param title: title of figure.
    :param hoover: include a hoover tool. Default True.
    :param hoover_tips: variables to include in the hoover tool. Default None. If None the
                hoover tool shows the y axis value. v.g. [('label', '@column_name')]
    :param toolbar: tools to include in the tool bar.
    :param legend_location: legend location in figure. Default 'center_right'.
    :return: bokeh figure.
    :author: Tecnalia Research and Innovation (Miguel Esteras and Sandra Riaño)
    """
    logger = getLogger(__name__)
    # transform strings to list of strings
    yvar = (([yvar] if isinstance(yvar, str) else yvar) if yvar
            else (list(obj.columns) if isinstance(obj, DataFrame)
                  else ([obj.name or 0])))
    # define datetime x variable
    obj.index.name = obj.index.name or 'index'
    xvar = xvar or obj.index.name
    df = obj.reset_index()

    if xrange is None:
        xr = sorted(set(df[xvar]))
        xrange = (xr[0], xr[int(len(xr) / 10)])

    # plot only the time component of datetime variables in the y axis
    ydtype = 'auto'
    for dtvar in [y for y in yvar if is_datetime64_any_dtype(df[y])]:
        df[dtvar] = df[dtvar].dt.time
        ydtype = 'datetime'

    t = title or "; ".join([str(x) for x in yvar])
    p = figure(plot_height=height, plot_width=width, tools=toolbar,
               toolbar_location='above', x_axis_type="datetime",
               y_axis_type=ydtype,
               background_fill_color="#f8f9f9", x_range=xrange, title=t)
    # plot data
    line_color_palette = line_color_palette or palette_dark
    for col, c in zip(yvar, line_color_palette):
        if groupby:
            groups = df[groupby].unique()
            for g, cc in zip(groups, line_color_palette):
                source = df[df[groupby] == g].rename(columns={col: 'y'})
                if source['y'].empty or source['y'].isnull().all():
                    continue
                else:
                    gly = p.line(x=xvar, y='y', line_color=line_color or cc,
                                 line_width=line_width,
                                 source=source, legend_label=str(g))
                if hoover:
                    tips = hoover_tips or [('value', '@y')]
                    p.add_tools(HoverTool(renderers=[gly], tooltips=tips,
                                          toggleable=False))
        else:
            source = df.rename(columns={col: 'y'})
            if source['y'].empty or source['y'].isnull().all():
                continue
            else:
                gly = p.line(x=xvar, y='y', line_color=line_color or c,
                             line_width=line_width,
                             source=source, legend_label=str(col))
            if hoover:
                tips = hoover_tips or [('value', '@y')]
                p.add_tools(HoverTool(renderers=[gly], tooltips=tips,
                                      toggleable=False))

    if dots is not None:
        dots.index.name = dots.index.name or 'UnnamedIndex'
        dots_xvar = dots_xvar or dots.index.name
        dots_yvar = [dots_yvar] if isinstance(dots_yvar, str) else (
            dots_yvar if dots_yvar is not None else [dots.name])
        df = dots.reset_index()
        dots_color_palette = dots_color_palette or palette_dark
        for col, c in zip(dots_yvar, dots_color_palette):
            df.rename(columns={col: 'y'}, inplace=True)
            if dots_groupby:
                for g, cc in zip(df[dots_groupby].unique(),
                                 dots_color_palette):
                    source = df[df[dots_groupby] == g]
                    if source['y'].empty or source['y'].isnull().all():
                        continue
                    else:
                        gly = p.circle(dots_xvar, 'y', size=dots_size,
                                       fill_color=dots_color or cc,
                                       fill_alpha=0.8, line_color='white',
                                       source=source,
                                       legend_label=str(g))
                        if hoover:
                            tips = hoover_tips or [('value', '@y')]
                            p.add_tools(
                                HoverTool(renderers=[gly], tooltips=tips,
                                          toggleable=False))
            else:
                if df['y'].empty or df['y'].isnull().all():
                    continue
                gly = p.circle(dots_xvar, 'y', size=dots_size, fill_alpha=0.8,
                               line_color='white',
                               fill_color=dots_color or c, source=df,
                               legend_label=str(col))
                if hoover:
                    tips = hoover_tips or [('value', '@y')]
                    p.add_tools(HoverTool(renderers=[gly], tooltips=tips,
                                          toggleable=False))
    else:
        logger.warning('Dots data is missing.')
    # title format
    p.title.text_font_size = '10pt' if title else '0pt'
    # x axis format
    p.xaxis.ticker = DatetimeTicker(desired_num_ticks=int(width / 100))
    p.xaxis.formatter = DatetimeTickFormatter(days=["%d-%b-%y"])
    # y axis format
    if yrange:
        p.y_range = yrange if isinstance(yrange, DataRange1d) else Range1d(
            *yrange)
    # legend format
    p.legend.click_policy = 'hide'
    p.legend.location = legend_location
    p.legend.label_text_font_size = '8pt'
    p.legend.background_fill_color = "#ffffff"
    p.legend.background_fill_alpha = 1
    p.legend.label_text_line_height = 1
    p.legend.spacing = 1
    # borders
    p.min_border_bottom = 50
    p.min_border_left = 50
    return p


def time_bars(obj: Union[DataFrame, Series], yvar: Union[str, List[str]],
              xvar: str = None,
              xrange: Tuple = None,
              yrange: Tuple = None, groupby: str = None, color: str = None,
              color_palette: List[str] = None,
              height: int = 400, width: int = 1600, bar_width=1,
              title: str = None,
              toolbar: str = 'xpan,box_zoom,reset',
              legend_location: str = 'top_right',
              hoover: bool = True,
              hoover_tips: Iterable[Tuple[str, str]] = None) -> figure:
    """Plot a time series bar plot.

    :param obj: input data.
    :param yvar: columns names in data to plot in the y axis.
    :param xvar: column or index name to plot in the x axis. Default None. If None the index
                will plot on the x axis.
    :param xrange: x range in the format (min, max) or bokeh.figure.x_range. Default None.
                If None the x axis shows the first 1/10 of the x variable data.
    :param yrange: y range in the format (min, max). If None the default y axis range is shown.
    :param groupby: name of column to used to group the data. If None data is not grouped.
    :param color: color of bars, only effective when groupby is None. Default None. If None,
            the brewer['Set3'] palette is used.
    :param color_palette: palette of color as list of HEX codes to use in case of more than
            one group of data or variables per plot. Default None. In None, a combination of brewer
            palettes is used.
    :param bar_width: width of bars. Default 1.
    :param height: height of plot in pixels. Default 400.
    :param width: width of plot in pixels. Default 1600.
    :param title: title of plot. Default None. If None the title is a list of the names of the
                variables plotted in the y axis.
    :param toolbar: tools to include in the tool bar.
    :param legend_location: legend location.
    :param hoover: include a hoover tool. Default True.
    :param hoover_tips: variables to include in the hoover tool. Default None. If None the
                hoover tool shows the y axis value. v.g. [('label', '@column_name')]
    :return: bokeh figure.
    :author: Tecnalia Research and Innovation (Miguel Esteras and Sandra Riaño)
    """
    logger = getLogger(__name__)
    # transform strings to list of strings
    yvar = (([yvar] if isinstance(yvar, str) else yvar) if yvar
            else (list(obj.columns) if isinstance(obj, DataFrame)
                  else ([obj.name or 0])))
    # define datetime x variable
    obj.index.name = obj.index.name or 'index'
    xvar = xvar or obj.index.name
    df = obj.reset_index()

    if xrange is None:
        xr = sorted(set(df[xvar]))
        xrange = (xr[0], xr[int(len(xr) / 10)])

    # plot only the time component of datetime variables in the y axis
    ydtype = 'auto'
    for dtvar in [y for y in yvar if is_datetime64_any_dtype(df[y])]:
        df[dtvar] = df[dtvar].dt.time
        ydtype = 'datetime'

    t = title or "; ".join([str(x) for x in yvar])
    p = figure(plot_height=height, plot_width=width, tools=toolbar,
               toolbar_location='above',
               x_axis_type="datetime", y_axis_type=ydtype,
               background_fill_color="#f8f9f9",
               x_range=xrange, title=t)
    # plot data
    color_palette = color_palette or brewer_sets_23
    for col, c in zip(yvar, color_palette):
        if groupby:
            groups = df[groupby].unique()
            for g, cc in zip(groups, brewer['Set3'][12] * 10):
                source = df[df[groupby] == g].rename(columns={col: 'y'})
                if source['y'].empty or source['y'].isnull().all():
                    continue
                gly = p.vbar(x=xvar, top='y', width=bar_width, source=source,
                             legend_label=str(g),
                             fill_color=color or cc, line_color=color or cc)
                if hoover:
                    tips = hoover_tips or [('value', '@y')]
                    p.add_tools(HoverTool(renderers=[gly], tooltips=tips,
                                          toggleable=False))
        else:
            source = df.rename(columns={col: 'y'})
            if source['y'].empty or source['y'].isnull().all():
                continue
            gly = p.vbar(x=xvar, top=col, width=bar_width, source=source,
                         legend_label=str(col),
                         fill_color=color or c, line_color=color or c)
            if hoover:
                tips = hoover_tips or [('value', '@y')]
                p.add_tools(HoverTool(renderers=[gly], tooltips=tips,
                                      toggleable=False))
    # title format
    p.title.text_font_size = '10pt'
    # x axis format
    p.xaxis.ticker = DatetimeTicker(desired_num_ticks=int(width / 100))
    p.xaxis.formatter = DatetimeTickFormatter(days=["%d-%b-%y"])
    # y axis format
    if yrange:
        p.y_range = yrange if isinstance(yrange, DataRange1d) else Range1d(
            *yrange)
    # legend format
    p.legend.click_policy = 'hide'
    p.legend.location = legend_location
    p.legend.label_text_font_size = '8pt'
    p.legend.background_fill_color = "#ffffff"
    p.legend.background_fill_alpha = 1
    p.legend.label_text_line_height = 1
    p.legend.spacing = 1
    # borders
    p.min_border_bottom = 50
    p.min_border_left = 50
    return p


def time_scatter(obj: Union[DataFrame, Series],
                 yvar: Union[str, Iterable[str]] = None,
                 xvar: str = None, xrange: Iterable = None,
                 yrange: Iterable = None,
                 groupby: str = None, color: str = None,
                 color_palette: List[str] = None,
                 height: int = 400, width: int = 1600,
                 legend_location: str = 'top_right',
                 size: Union[int, float] = 12, alpha: float = .8,
                 title: str = None, toolbar: str = 'xpan,box_zoom,reset',
                 hoover: bool = True,
                 hoover_tips: Iterable[Tuple[str, str]] = None) -> figure:
    """Creates a time series scatter plot.

    :param obj: input data.
    :param yvar: columns names in data to plot in the y axis.
    :param xvar: column or index name to plot in the x axis. Default None. If None the index
                will plot on the x axis.
    :param xrange: x range in the format (min, max) or bokeh.figure.x_range. Default None.
                If None the x axis shows the first 1/10 of the x variable data.
    :param yrange: y range in the format (min, max). If None the default y axis range is shown.
    :param groupby: name of column to used to group the data. If None data is not grouped.
    :param color: color of dots, only effective when groupby is None. Default None. If None,
                the brewer['Set3'] palette is used.
    :param color_palette: palette of color as list of HEX codes to use in case of more than one
            group of data or variable per plot. Default None. In None, a combination of
            brewer 'Set' palettes is used.
    :param height: height of plot in pixels. Default 400.
    :param width: width of plot in pixels. Default 1600.
    :param legend_location: legend location.
    :param size: size of dots. Default 12.
    :param alpha: transparency factor of dots (0->transparent, 1->non-transparent). Default 0.8
    :param title: title of plot. Default None. If None the title is a list of the names of the
                variables plotted in the y axis.
    :param toolbar: tools to include in the tool bar.
    :param hoover: include a hoover tool. Default True.
    :param hoover_tips: variables to include in the hoover tool. Default None. If None the
                hoover tool shows the y axis value. v.g. [('label', '@column_name')]
    :return: bokeh figure.
    :author: Tecnalia Research and Innovation (Miguel Esteras and Sandra Riaño)
    """

    logger = getLogger(__name__)
    # transform strings to list of strings
    yvar = (([yvar] if isinstance(yvar, str) else yvar) if yvar
            else (list(obj.columns) if isinstance(obj, DataFrame)
                  else ([obj.name or 0])))
    # define datetime x variable
    obj.index.name = obj.index.name or 'index'
    xvar = xvar or obj.index.name
    df = obj.reset_index()
    # define x range
    if xrange is None:
        xr = sorted(set(df[xvar]))
        xrange = (xr[0], xr[int(len(xr) / 10)])

    # plot only the time component of datetime variables in the y axis
    ydtype = 'auto'
    for dtvar in [y for y in yvar if is_datetime64_any_dtype(df[y])]:
        df[dtvar] = df[dtvar].dt.time
        ydtype = 'datetime'

    t = title or "; ".join([str(x) for x in yvar])
    p = figure(plot_height=height, plot_width=width, tools=toolbar,
               toolbar_location='above', y_axis_type=ydtype,
               x_axis_type="datetime",
               background_fill_color="#f8f9f9", x_range=xrange, title=t)
    # plot data
    color_palette = color_palette or brewer_sets_23
    for col, c in zip(yvar, color_palette):
        if groupby:
            groups = df[groupby].unique()
            for g, cc in zip(groups, color_palette):
                source = df[df[groupby] == g].rename(columns={col: 'y'})
                if source['y'].empty or source['y'].isnull().all():
                    continue
                gly = p.circle(x=xvar, y='y', source=source,
                               size=size, fill_color=color or cc,
                               fill_alpha=alpha, line_alpha=0,
                               legend_label=str(g))
                if hoover:
                    tips = hoover_tips or [('value', '@y')]
                    p.add_tools(HoverTool(renderers=[gly], tooltips=tips,
                                          toggleable=False))
        else:
            source = df.rename(columns={col: 'y'})
            if source['y'].empty or source['y'].isnull().all():
                continue
            gly = p.circle(x=xvar, y='y', source=source,
                           size=size, fill_color=color or c, fill_alpha=alpha,
                           line_alpha=0,
                           legend_label=str(col))
            if hoover:
                tips = hoover_tips or [('value', '@y')]
                p.add_tools(HoverTool(renderers=[gly], tooltips=tips,
                                      toggleable=False))
    # title format
    p.title.text_font_size = '10pt'
    # x axis format
    p.xaxis.ticker = DatetimeTicker(desired_num_ticks=int(width / 100))
    p.xaxis.formatter = DatetimeTickFormatter(days=["%d-%b-%y"])
    # y axis format
    if yrange:
        p.y_range = yrange if isinstance(yrange, DataRange1d) else Range1d(
            *yrange)
    # legend format
    p.legend.click_policy = 'hide'
    p.legend.location = legend_location
    p.legend.label_text_font_size = '8pt'
    p.legend.background_fill_color = "#ffffff"
    p.legend.background_fill_alpha = 1
    p.legend.label_text_line_height = 1
    p.legend.spacing = 1
    # borders
    p.min_border_bottom = 50
    p.min_border_left = 50
    return p


def time_range_tool(obj: Union[DataFrame, Series], xrange: Iterable,
                    yvar: str = None, xvar: str = None,
                    yrange: Iterable = None,
                    height=120, width=1600) -> figure:
    """Plots a range selection tool for time series plots with xpan tools.

    :param obj: input data.
    :param yvar: columns name in data to plot in the y axis.
    :param xrange: x range in the format (min, max) or a bokeh.figure.x_range.
    :param xvar: column or index name to plot in the x axis. Default None. If None the index
                will plot on the x axis.
    :param yrange: y range in the format (min, max). If None the default y axis range is shown.
    :param height: height of plot in pixels. Default 120.
    :param width: width of plot in pixels. Default 1600.
    :return: bokeh figure.
    :raises TypeError: if yvar column is not data type numeric.
    :author: Tecnalia Research and Innovation (Miguel Esteras and Sandra Riaño)
    """

    logger = getLogger(__name__)
    # define datetime x variable
    obj.index.name = obj.index.name or 'index'
    xvar = xvar or obj.index.name
    df = obj.sort_index().reset_index()
    # set default value
    yvar = yvar if yvar is not None else obj.name
    # check y axis variable dtype
    if not (is_numeric_dtype(df[yvar]) or is_datetime64_any_dtype(df[yvar])):
        raise TypeError(f'Y axis variable column must be numeric or datetime.')
    # plot only the time component of datetime variables in the y axis
    ydtype = None
    if is_datetime64_any_dtype(df[yvar]):
        df[yvar] = df[yvar].dt.time
        ydtype = 'datetime'

    p = figure(
        title=f"Drag the box to change the temporal range. Variable displayed: {yvar}",
        plot_height=height, plot_width=width, x_axis_type="datetime",
        y_axis_type=ydtype,
        toolbar_location=None, background_fill_color="#f5f5f5")
    # plot data
    p.vbar(x=xvar, top=yvar, width=1, source=df, fill_color="#aaafb3",
           line_color="#aaafb3")
    # x axis format
    p.xaxis.ticker = DatetimeTicker(desired_num_ticks=int(width / 100))
    p.xaxis.formatter = DatetimeTickFormatter(days=["%d-%b-%y"])
    # y axis format
    if yrange:
        p.y_range = yrange if isinstance(yrange, DataRange1d) else Range1d(
            *yrange)
    p.ygrid.grid_line_color = None
    p.title.text_font_size = "10pt"
    # add selection of range tool
    tool = RangeTool(x_range=xrange)
    tool.overlay.fill_color = "#708090"
    tool.overlay.fill_alpha = 0.5
    p.add_tools(tool)
    p.toolbar.active_multi = tool
    return p


def scatter(obj: DataFrame, xvar: str, yvar: str, xrange: Tuple = None,
            yrange: Tuple = None,
            size: Union[int, float, str] = 1, size_type: str = 'radius',
            colorvar: str = None, color_asc: bool = False,
            color_min: float = None, color_max: float = None,
            marker_color: str = None, color_palette: List[str] = None,
            color_alpha: float = 0.6, groupby: str = None,
            legend_location: str = 'top_right',
            height: int = 700, width: int = 700,
            x_jitter: float = 0, y_jitter: float = 0,
            hist_axes: bool = False, nbins: int = 10,
            get_regression: bool = False,
            deg: int = 1, add_regression: Dict = None, hoover: bool = True,
            title: str = '',
            hoover_tips: Iterable[Tuple] = None,
            toolbar: str = "pan,box_zoom,reset",
            xaxis_labels_map: Dict = None,
            yaxis_labels_map: Dict = None) -> Union[figure, None]:
    """Scatter plot + Histograms on x and y axis + regression line/curve.

    :param obj: input table.
    :param xvar: name of column in table to plot on the x axis.
    :param yvar: name of column in table to plot on the y axis.
    :param size: size of radius of markers in units, or name of the column on table to use
                as marker size. Default 1 unit.
    :param size_type: measure size in 'radius' or 'size'.
    :param colorvar: name of column in table to map the color of the markers to. Column must be
                dtype numerical.
    :param color_asc: indicate if maximum colors are red (True) or blue(False).
    :param color_max: indicate maximum value to colour as red (if asc), instead of variable maximum
    :param marker_color: color of marker.
    :param color_palette: palette of color as list of HEX codes to use in case of more than one
            group of data or variable per plot. Default None. In None, a combination of
            brewer 'Set' palettes is used.
    :param color_alpha: transparency of fill color of marker (0-transparent, 1-opaque). Default 0.6.
    :param groupby: name of column in table to group data in plot. Groups are differentiated
                by marker color. Default None.
    :param legend_location: legend location in figure. Default 'center_right'.
    :param xrange: x range in the format (min, max) or bokeh.figure.x_range. Default None.
    :param yrange: y range in the format (min, max) or bokeh.figure.y_range. Default None.
    :param height: height of plot in pixels. Default 700.
    :param width: width of plot in pixels. Default 700.
    :param x_jitter: add jitter to categorical groups in x axis. Default 0, or no jitter.
    :param hist_axes: plot histograms at the x and y axes. Default False.
    :param nbins: number of bins to divided the histograms into. Default 10.
    :param get_regression: compute and plot a regression estimator for each group in the data.
                Default, False.
    :param deg: degrees of freedom of the regression estimator. Default 1.
    :param add_regression: regression fit function of the type returned by the numpy.poly1d.
            Default None.
    :param hoover: display hoover tool tips. Default True.
    :param hoover_tips: variables to include in the hoover tool v.g. [('label', '@column_name')].
                Default None. If None the hoover tool shows the y axis value.
    :param toolbar: bokeh figure tools to include. Default 'pan,box_zoom,reset'.
    :param title: title of plot.
    :param xaxis_labels_map: dict used to override major x axis labels. Default None.
    :param yaxis_labels_map: dict used to override major y axis labels. Default None.
    :return: bokeh figure.
    :author: Tecnalia Research and Innovation (Miguel Esteras and Sandra Riaño)
    """

    logger = getLogger(__name__)
    # define axis range
    if not xrange:
        if is_numeric_dtype(obj[xvar]):
            xdiff = (1 + obj[xvar].max() - obj[xvar].min()) * 1.1
            xrange = [obj[xvar].max() - xdiff, obj[xvar].min() + xdiff]
        else:
            xrange = obj[xvar].unique()
    if not yrange:
        if is_numeric_dtype(obj[yvar]):
            ydiff = (1 + obj[yvar].max() - obj[yvar].min()) * 1.1
            yrange = [obj[yvar].max() - ydiff, obj[yvar].min() + ydiff]
        else:
            yrange = obj[yvar].unique()

    # create scatter plot
    p = figure(plot_height=height, plot_width=width, min_border=50,
               min_border_left=50,
               tools=toolbar, toolbar_location="above", title=title,
               x_range=xrange,
               y_range=yrange, background_fill_color="#ffffff")
    p.select(BoxSelectTool).select_every_mousemove = False

    color_palette = color_palette or brewer_sets_123
    scatter_params = {size_type: size}
    if groupby:
        for g, cc in zip(obj[groupby].unique(), color_palette):
            source = obj[obj[groupby] == g]
            source.insert(0, 'x', source[xvar])
            source.insert(0, 'y', source[yvar])
            if source.y.isnull().all() or source.x.isnull().all():
                continue

            gly = p.circle(x=jitter('x', x_jitter, range=p.x_range),
                           y=jitter('y', y_jitter, range=p.y_range),
                           color=marker_color or cc, size=size,
                           fill_alpha=color_alpha, line_alpha=color_alpha,
                           source=source,
                           legend_label=str(g))
            if hoover:
                tips = hoover_tips or [('x', '@x'), ('y', '@y')]
                p.add_tools(HoverTool(renderers=[gly], tooltips=tips,
                                      toggleable=False))

    else:
        source = obj.copy()
        source.insert(0, 'x', source[xvar])
        source.insert(0, 'y', source[yvar])
        if source.y.isnull().all() or source.x.isnull().all():
            logger.error('All NaN values in axis.')
            return
        if colorvar is None:
            cc = color_palette[0] or brewer['Set2'][8][1]
        else:
            source.insert(0, 'c', source[colorvar])
            clip_max = color_max or source['c'].quantile(.99)
            clip_min = color_min or source['c'].quantile(.01)
            source[colorvar] = source[colorvar].clip(clip_min, clip_max)
            pal = rainbow if not color_asc else rainbow[::-1]
            mapper = LinearColorMapper(palette=pal)
            cc = {'field': colorvar, 'transform': mapper}
            color_bar = ColorBar(color_mapper=mapper,
                                 major_label_text_font_size="10pt",
                                 ticker=BasicTicker(desired_num_ticks=10),
                                 label_standoff=10, border_line_color=None,
                                 location=(0, 0), width=10)
            p.add_layout(color_bar, 'right')
            p.title.text = p.title.text + f' | Color Bar: {colorvar}'
        gly = p.circle(jitter('x', x_jitter), 'y', color=cc,
                       fill_alpha=color_alpha, line_alpha=color_alpha,
                       source=source, size=size)
        if hoover:
            tips = hoover_tips or [('x', '@x'), ('y', '@y'), ('c', '@c')]
            p.add_tools(
                HoverTool(renderers=[gly], tooltips=tips, toggleable=False))

    # plot a regression function
    if get_regression:
        source = obj[(notnull(obj[xvar])) & (notnull(obj[yvar]))]
        if groupby:
            for g, cc in zip(source[groupby].unique(), color_palette):
                x = source[source[groupby] == g][xvar].values
                y = source[source[groupby] == g][yvar].values
                try:
                    fit = polyfit(x, y, deg)
                    fit_fn = poly1d(fit)
                    # fit_fn is a function which takes in x
                    # and returns an estimate for y
                    xx = linspace(min(x), max(x), 1000)
                    p.line(x=xx, y=fit_fn(xx), line_color=cc, line_width=2,
                           legend_label=str(g))
                except Exception as e:
                    logger.error(f'Regression failed.\n{e}')
        else:
            cc = 'black'
            x = source[xvar].values
            y = source[yvar].values
            try:
                fit = polyfit(x, y, deg)
                fit_fn = poly1d(fit)
                # fit_fn is a function which takes in x
                # and returns an estimate for y
                xx = linspace(min(x), max(x), 1000)
                p.line(x=xx, y=fit_fn(xx), line_color=cc, line_width=2)
            except Exception as e:
                logger.error(f'Regression failed.\n{e}')

    if add_regression:
        for (key, model), c in zip(add_regression.items(), brewer_sets_12):
            xx = linspace(p.x_range.start, p.x_range.end, 1000)
            p.line(x=xx, y=model.predict(array([[a] for a in xx])),
                   line_color=c, line_width=1, legend_label=str(key))

    # legend format
    if groupby or add_regression:
        p.legend.click_policy = 'hide'
        p.legend.location = legend_location
        p.legend.label_text_font_size = '8pt'
        p.legend.background_fill_color = "#ffffff"
        p.legend.background_fill_alpha = 1
        p.legend.label_text_line_height = 1
        p.legend.spacing = 1

    p.min_border_left = 50
    p.min_border_top = 50

    if not hist_axes:
        # axis format
        p.xaxis.axis_label = xvar
        p.yaxis.axis_label = yvar
        p.xaxis.major_label_overrides = xaxis_labels_map or {}
        p.yaxis.major_label_overrides = yaxis_labels_map or {}

        p.xaxis.axis_label_standoff = 20
        p.yaxis.axis_label_standoff = 20
        return p

    # add histograms to axis
    p.axis.visible = False
    # create the horizontal histogram
    xhist, xedges = histogram(obj[xvar].values[~isnan(obj[xvar].values)],
                              bins=nbins)
    xzeros = zeros(len(xedges) - 1)
    xmax = max(xhist) * 1.1

    xh = figure(toolbar_location=None, plot_width=p.plot_width,
                plot_height=200,
                x_range=p.x_range, y_range=(-xmax / 4, xmax), min_border=10,
                min_border_left=50,
                y_axis_location="right", background_fill_color="#fafafa")
    xh.xgrid.grid_line_color = None
    xh.yaxis.major_label_orientation = pi / 4
    xh.xaxis.axis_label = xvar
    xh.xaxis.major_label_overrides = xaxis_labels_map or {}
    xh.xaxis.axis_label_standoff = 20
    line_param = dict(color="#3A5785", line_color=None)
    if groupby:
        for g, cc in zip(obj[groupby].unique(), brewer_sets_123):
            xx = obj[obj[groupby] == g][xvar].values
            xxhist, xxedges = histogram(xx[~isnan(xx)], bins=nbins)
            xh.quad(bottom=0, left=xxedges[:-1], right=xxedges[1:], top=xxhist,
                    color=cc,
                    fill_alpha=0.3)
    else:
        cc = brewer['Set2'][8][1]
        xh.quad(bottom=0, left=xedges[:-1], right=xedges[1:], top=xhist,
                color=cc,
                line_color="white")
    xh.quad(bottom=0, left=xedges[:-1], right=xedges[1:], top=xzeros,
            alpha=0.5, **line_param)
    xh.quad(bottom=0, left=xedges[:-1], right=xedges[1:], top=xzeros,
            alpha=0.1, **line_param)

    # create the vertical histogram
    yhist, yedges = histogram(obj[yvar].values[~isnan(obj[yvar].values)],
                              bins=nbins)
    yzeros = zeros(len(yedges) - 1)
    ymax = max(yhist) * 1.1

    yh = figure(toolbar_location=None, plot_width=200,
                plot_height=p.plot_height,
                x_range=(-ymax / 4, ymax), y_range=p.y_range, min_border=10,
                y_axis_location="right", background_fill_color="#fafafa")
    yh.ygrid.grid_line_color = None
    yh.xaxis.major_label_orientation = pi / 4
    yh.yaxis.major_label_overrides = yaxis_labels_map or {}
    yh.yaxis.axis_label = yvar
    yh.yaxis.axis_label_standoff = 20

    if groupby:
        for g, cc in zip(obj[groupby].unique(), brewer_sets_123):
            yy = obj[obj[groupby] == g][yvar].values
            yyhist, yyedges = histogram(yy[~isnan(yy)], bins=nbins)
            yh.quad(left=0, bottom=yyedges[:-1], top=yyedges[1:], right=yyhist,
                    color=cc,
                    fill_alpha=0.3)
    else:
        cc = brewer['Set2'][8][1]
        yh.quad(left=0, bottom=yedges[:-1], top=yedges[1:], right=yhist,
                color=cc,
                line_color="white")
    yh.quad(left=0, bottom=yedges[:-1], top=yedges[1:], right=yzeros,
            alpha=0.5, **line_param)
    yh.quad(left=0, bottom=yedges[:-1], top=yedges[1:], right=yzeros,
            alpha=0.1, **line_param)

    return layout([[p, yh], [xh]])


def lines(obj: Union[DataFrame, Series],
          yvar: Union[str, Iterable[str]] = None, xvar: str = None,
          xrange: Tuple = None, yrange: Tuple = None, groupby: str = None,
          highlight: Union[str, Iterable[str]] = None, line_width: float = 1,
          hline: List[float] = None, vline: List[float] = None,
          color: str = None,
          color_palette: List[str] = None,
          legend_location: str = 'top_right', height: int = 400,
          width: int = 1600,
          title: str = None, toolbar: str = "pan,box_zoom,reset",
          background: str = None,
          hoover: bool = True,
          hoover_tips: Iterable[Tuple[str, str]] = None) -> figure:
    """Plot a line graph.

    :param obj: input data.
    :param yvar: columns names in data to plot in the y axis.
    :param xvar: column or index name to plot in the x axis. Default None. If None the index
                will plot on the x axis.
    :param xrange: x range in the format (min, max) or bokeh.figure.x_range. Default None.
                If None the x axis shows the first 1/10 of the x variable data.
    :param yrange: y range in the format (min, max). If None the default y axis range is shown.
    :param groupby: name of column to used to group the data. If None data is not grouped.
    :param highlight: columns names of variables in the y axis to be plotted with a thicker line.
    :param line_width: width of lines.
    :param hline: positions in the y axis where to draw a span line.
    :param vline: positions in the x axis where to draw a span line.
    :param color: color of lines, only effective when groupby is None. Default None. If None,
            the brewer['Set1'] and brewer['Set2'] palette is used.
    :param color_palette: palette of color as list of HEX codes to use in case of more than
            one group of data or variables per plot. Default None. In None, a combination of brewer
            palettes is used.
    :param legend_location: legend location in figure. Default 'center_right'.
    :param height: height of plot in pixels. Default 400.
    :param width: width of plot in pixels. Default 1600.
    :param title: title of plot. Default None. If None the title is a list of the names of the
                variables plotted in the y axis.
    :param toolbar: tools to include in the tool bar.
    :param background: color of background. Default None. If None the background color is gray.
    :param hoover: include a hoover tool. Default True.
    :param hoover_tips: variables to include in the hoover tool. Default None. If None the
                hoover tool shows the y axis value. v.g. [('label', '@column_name')]
    :return: bokeh figure.
    :author: Tecnalia Research and Innovation (Miguel Esteras and Sandra Riaño)
    """

    logger = getLogger(__name__)
    # transform strings to list of strings
    yvar = (([yvar] if isinstance(yvar, str) else yvar) if yvar
            else (list(obj.columns) if isinstance(obj, DataFrame)
                  else ([obj.name or 0])))

    highlight = list(highlight) if highlight else []
    # define datetime x variable
    obj.index.name = obj.index.name or 'index'
    xvar = xvar or obj.index.name
    df = obj.reset_index()
    # define axis range
    xdiff = (obj[xvar].max() - obj[xvar].min()) * 1.1
    xrange = xrange or [obj[xvar].max() - xdiff, obj[xvar].min() + xdiff]
    # define title
    t = title or "; ".join([str(x) for x in yvar])
    # create figure
    p = figure(plot_height=height, plot_width=width, tools=toolbar,
               toolbar_location="above",
               background_fill_color="#f8f9f9", x_range=xrange, title=t)
    # plot data
    color_palette = color_palette or brewer_sets_123
    for col, c in zip(yvar, color_palette):
        if groupby:
            groups = df[groupby].unique()
            for g, cc in zip(groups, color_palette):
                source = df[df[groupby] == g].rename(columns={col: 'y'})
                if source['y'].empty or source['y'].isnull().all():
                    continue
                w = 4 if g in highlight else line_width
                gly = p.line(x=xvar, y='y', line_color=color or cc,
                             line_width=w, source=source,
                             legend_label=str(g))
                if hoover:
                    tips = hoover_tips or [('value', '@y')]
                    p.add_tools(HoverTool(renderers=[gly], tooltips=tips,
                                          toggleable=False))
        else:
            source = df.rename(columns={col: 'y'})
            if source['y'].empty or source['y'].isnull().all():
                continue
            w = 4 if col in highlight else line_width
            gly = p.line(x=xvar, y='y', line_color=color or c, line_width=w,
                         source=source,
                         legend_label=str(col))
            if hoover:
                tips = hoover_tips or [('value', '@y')]
                p.add_tools(HoverTool(renderers=[gly], tooltips=tips,
                                      toggleable=False))

    # reference lines
    if hline:
        for line in hline:
            new_line = Span(location=line, dimension='width',
                            line_color='black', line_width=3,
                            line_dash='dashed')
            p.renderers.extend([new_line])
    if vline:
        for line in vline:
            new_line = Span(location=line, dimension='height',
                            line_color='gray', line_width=3,
                            line_dash='dashed')
            p.renderers.extend([new_line])

    # y axis format
    if yrange:
        p.y_range = yrange if isinstance(yrange, DataRange1d) else Range1d(
            *yrange)

    # title format
    p.title.text_font_size = '10pt' if title else '0pt'

    # axis format
    p.xaxis.axis_label = xvar

    # legend format
    p.legend.click_policy = 'hide'
    p.legend.location = legend_location
    p.legend.label_text_font_size = '8pt'
    p.legend.background_fill_color = background or "#ffffff"
    p.legend.background_fill_alpha = 1
    p.legend.label_text_line_height = 1
    p.legend.spacing = 1
    # borders
    p.min_border_top = 100
    p.min_border_left = 100
    return p


def plot_blanks(df: DataFrame, title: str, width: int = 400, height: int = 800,
                palette: str = "Blues8",
                datetime_index: bool = True) -> figure:
    """Plot data frame values as pixel intensity, using index as y axis values.

    :param df: input data.
    :param title: title of plot.
    :param width: plot width in pixels.
    :param height: plot height in pixels.
    :param palette: name of bokeh color palette.
    :param datetime_index: index of input data is of type datetime.
    :return: bokeh figure.
    :author: Tecnalia Research and Innovation (Miguel Esteras and Sandra Riaño)
    """
    logger = getLogger(__name__)
    p = figure(plot_width=width, plot_height=height, toolbar_location=None)
    p.x_range.range_padding = 0
    p.y_range.range_padding = 0
    p.xaxis.major_label_text_font_size = "8pt"
    p.yaxis.major_label_text_font_size = "8pt"
    # title
    p.title.text = title
    p.title.align = "left"
    p.title.text_color = "#374f80"
    p.title.text_font_size = "18px"
    # borders
    p.min_border_left = 10
    p.min_border_right = 20
    p.min_border_top = 50
    p.min_border_bottom = 150
    # format x axis
    p.xaxis.ticker = FixedTicker(ticks=[x + .5 for x in range(df.shape[1])])
    p.xaxis.major_label_overrides = {x + .5: y for x, y
                                     in zip(range(df.shape[1]),
                                            df.columns.values)}
    p.xaxis.major_label_orientation = 1.2
    # format y axis
    ylabels = sorted(set(df.index.values))
    if datetime_index:
        ylabels = [x.strftime("%d-%B-%Y") for x in ylabels]
    p.yaxis.ticker = FixedTicker(
        ticks=[int(y) for y in linspace(0, len(ylabels) - 1, 20)])
    p.yaxis.major_label_overrides = {int(y): ylabels[::-1][int(y)] for y
                                     in linspace(0, len(ylabels) - 1,
                                                 int(height / 50))}
    # plot data
    p.image(image=[df.values], x=0, y=0, dw=df.shape[1], dh=df.shape[0],
            palette=palette)

    return p


def plot_table(obj: Union[DataFrame, Series], column_names: List[str] = None,
               datetime_index: bool = True,
               height: int = 600, width: int = 1600, decimals: int = 2,
               title: str = None) -> figure:
    """plot column data table.

    :param obj: input data.
    :param column_names: names of columns in obj to include in table. Default None.
        If None, all columns in obj will be included.
    :param height: table height in pixels.
    :param width: table width in pixels.
    :param datetime_index: format the index column as datetime.
    :param decimals: decimal places to show on numeric columns.
    :param title: title of table. Default None.
    :return: bokeh figure.
    :author: Tecnalia Research and Innovation (Miguel Esteras and Sandra Riaño)
    """
    logger = getLogger(__name__)

    obj.index.name = obj.index.name or 'UnnamedIndex'
    if isinstance(obj, Series):
        column_names = column_names or [obj.name]
    elif isinstance(obj, DataFrame):
        column_names = column_names or list(obj.columns)
    source = obj.sort_index().reset_index()
    index_format = DateFormatter(
        format='%d-%m-%Y %H:%M:%S') if datetime_index else None
    columns = [TableColumn(field=obj.index.name, title=obj.index.name,
                           formatter=index_format, width=150)]
    table_width = 150
    number_format = '0.' + ('0' * decimals)
    for col in column_names:
        col_format = None
        col_width = (len(col) * 5) + 40
        if is_numeric_dtype(source[col]):
            col_format = NumberFormatter(format=number_format)
        if is_datetime64_any_dtype(source[col]):
            col_format = DateFormatter(format='%d-%m-%Y %H:%M:%S')
        columns.append(TableColumn(field=col, title=col, formatter=col_format,
                                   width=col_width))
        table_width += col_width
    table_width = min(table_width, width)
    data_table = DataTable(columns=columns, source=ColumnDataSource(source),
                           index_position=None,
                           reorderable=True,
                           height=height, fit_columns=False, header_row=True,
                           width=table_width)
    data_table.margin = (5, 5, 20, 40)
    title = title or ''
    p = Paragraph(text=title)
    p.margin = (20, 5, 5, 40)
    return layout(p, data_table)


def plot_text(text: str, width: float = 50, height: float = 50,
              angle: float = 0,
              fontsize: int = 12, color: str = None,
              outline_color: str = None) -> figure:
    """Plot text box.

    :param text: text to plot.
    :param width: width of text box. Default 50.
    :param height: height of tect box. Default 50.
    :param angle: angle (radiants) to rotate the text from the horizontal. Default 0.
    :param fontsize: font size of text. Default 12.
    :param color: font color of text (HEX codes or English names). Default 'black'.
    :param outline_color: color of outline around the text box. Default None (without outline).
    :return: bokeh figure.
    :author: Tecnalia Research and Innovation (Miguel Esteras and Sandra Riaño)
    """
    fontsize = str(f'{fontsize}pt')
    color = color or 'black'
    # create figure
    p = figure(plot_height=height, plot_width=width, min_border=10,
               min_border_left=10,
               x_range=(-1, 1), y_range=(-1, 1), toolbar_location=None)

    x, y = linspace(-1, 1, 3), linspace(-1, 1, 3)
    source = ColumnDataSource(dict(x=x, y=y, text=['', text, '']))
    p.text('x', 'y', text='text', text_align="center", source=source,
           angle=angle,
           text_baseline="middle", text_font_size=fontsize, text_color=color)

    p.axis.visible = False
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.outline_line_color = outline_color

    return p
