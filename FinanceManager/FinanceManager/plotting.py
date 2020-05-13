from plotly.offline import plot
import plotly.graph_objects as go


def get_gauge_chart(start, end):
    fig_indicator = go.Figure(
        go.Indicator(mode="number+delta+gauge", value=end, number={'prefix': "&#x20B9;"},
                     delta={"reference": start, 'relative': True},
                     gauge={'steps': [
                         {'range': [0, start], 'color': 'lightgray'},
                         {'range': [start, end], 'color': 'gray'}
                     ]},
                     title={"text": "Profit Percentage"},
                     domain={'y': [0, 1], 'x': [0.25, 0.75]})
    )

    fig_indicator.update_layout(template='plotly_white', margin=dict(t=10, b=0, l=0, r=0), height=180)
    return plot(fig_indicator, output_type='div', include_plotlyjs=False, config={'displayModeBar': False})
