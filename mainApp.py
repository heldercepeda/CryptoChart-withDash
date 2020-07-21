# local imports
from assets.page_layout import index_string, main_layout, dropdowns, content, ohlcGraph
from assets.get_data import pairs_list

# imports
import dash
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import time


app = dash.Dash(__name__)
app.index_string = index_string


app.layout = html.Div(
    children=main_layout(
        controls=dropdowns,
        content=content,
        footer=None
    )
)


# Adjust the refresh rate according to the period
@app.callback(
    Output("interval", "interval"),
    [
        Input("period", "value")
    ]
)
def update_interval(period):
    if not period:
        raise PreventUpdate
    else:
        return period*1000


# Update pairs when a market is selected
@app.callback(
    [
        Output("pairs", "options"),
        Output("pairs", "disabled")
    ],
    [
        Input("markets", "value")
    ]
)
def update_pairs(market):
    if not market:
        raise PreventUpdate
    else:
        return pairs_list(market), False


# Update OHLC chart
@app.callback(
    Output("example-graph", "figure"),
    [
        Input("markets", "value"),
        Input("pairs", "value"),
        Input("period", "value"),
        Input("datapoints", "value"),
        Input("interval", "n_intervals")
    ]
)
def upload(market, pair, period, datapoints, n):
    if datapoints == "max":
        after = None
    else:
        after = int(time.time())-datapoints*period
    if not market:
        raise PreventUpdate
    elif not pair:
        return go.Figure(data=[]).update_layout(
                            margin={'l': 20, 'b': 30, 't': 10, 'r': 20},
                            template="plotly_dark",
                            height=500,
                            plot_bgcolor='black',
                            paper_bgcolor='black',
                            annotations=[
                                {
                                    "text": "No data to show!<br>Please select a pair",
                                    "xref": "paper",
                                    "yref": "paper",
                                    "showarrow": False,
                                    "font": {
                                        "size": 18,
                                        "color": "gray"
                                    }
                                }
                            ],
                            xaxis={
                                "visible": False
                            },
                            yaxis={
                                "visible": False
                            }
                        )
    else:
        return ohlcGraph(market, pair, before=None, after=after, periods=period)


if __name__ == '__main__':
    app.run_server(debug=True)
