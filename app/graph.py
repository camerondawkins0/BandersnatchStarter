import altair as alt
from altair import Chart, X, Y, Color
from pandas import DataFrame

def chart(df: DataFrame, x: str, y: str, target: str) -> Chart:
    properties = {
        # "width": 400,
        # "height": 300,
        "padding": 20,
        "background": "#313131",  # Dark background color
    }

    base_chart = Chart(df)
    
    brush = alt.selection(type='interval')
    condition = alt.condition(brush, Color(field=target, bin=alt.BinParams(maxbins=10)), alt.value('lightgray'))
    
    graph = base_chart.mark_circle().encode(
        X(field=x, type='quantitative', title=x),
        Y(field=y, type='quantitative', title=y),
        color=condition
    ).add_selection(
        brush
    )
    median_line = base_chart.mark_rule().encode(x=X(f'mean({target}):Q', title=target),
                                                size=alt.value(5))
    hist = base_chart.mark_bar().encode(
        y=Y(field='Type', aggregate='count'),
        x=X(field=target, type='quantitative', bin=alt.BinParams(maxbins=10)),
        color=Color(field=target, bin=alt.BinParams(maxbins=10))
    ).transform_filter(
        brush
    )
    
    graph_boxplot = base_chart.mark_boxplot(extent='min-max')\
    .encode(x=X(field="Type", type='ordinal'),
            y=Y(field=y, type='quantitative'),
            color=Color(field=target, bin=alt.BinParams(maxbins=10))).transform_filter(brush)

    chart_ = alt.HConcatChart(data=df, hconcat=(graph, (hist+median_line), graph_boxplot))

    chart_ = chart_.properties(**properties, title='Click and drag to select & Hover to View Info')\
        .configure_legend(orient='bottom')\
            .configure_title(fontSize=20,
                             anchor='middle',
                             color='red').configure_axis(tickColor='white', labelColor='white', labelAngle=-45, titleColor='white')

    return chart_
