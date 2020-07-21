# local imports
from assets.get_data import market_list, ohlc

# imports
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

values = [60, 180, 300, 900, 1800, 3600, 7200, 14400, 21600, 43200, 86400, 259200, 604800]
labels = ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "12h", "1d", "3d", "1w"]

# index_string has important html structure
index_string = ''' <!DOCTYPE html>
                        <html>
                            <head>
                                <meta charset="utf-8">
                                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                                <title>OHLC Chart with Dash</title>
                                <link rel="icon" href="/static/images/hc.png">
                                <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
                                <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
                            </head>
                            <body style="background-color: #000000;">
                                {%app_entry%}
                                <footer>
                                    {%config%}
                                    {%scripts%}
                                    {%renderer%}
                                </footer>
                                <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
                                <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
                                <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js" integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI" crossorigin="anonymous"></script>
                            </body>
                        </html>'''

# dropdowns has all the dropdowns menus that will allow us to interact wit the OHLC chart
dropdowns = html.Div(children=[
    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                dcc.Dropdown(
                    id='period',
                    options=[
                        {
                            'label': label,
                            'value': value
                        }
                        for label, value in zip(labels, values)
                    ],
                    value=300,
                    style={"width": "70px", "background-color": "#000000"},
                    searchable=False,
                    placeholder="Period",
                    clearable=False,
                ),
                dcc.Dropdown(
                    id='datapoints',
                    options=[
                        {
                            'label': i,
                            'value': i
                        }
                        for i in [30, 60, 90, 120, 150, 240, 300, 420, 600, "max"]
                    ],  # Number of datapoints to be shown in the chart
                    value=150,
                    style={
                        "width": "70px",
                        "background-color": "#000000"
                    },
                    searchable=False,
                    placeholder="Data points",
                    disabled=False,
                    clearable=False,
                ),
                dcc.Dropdown(
                    id='markets',
                    options=market_list(),  # Market list from Cryptowat.ch
                    value='',
                    style={
                        "width": "250px",
                        "background-color": "#000000"
                    },
                    clearable=False,
                    searchable=True,
                    placeholder="Select market"
                ),
                dcc.Dropdown(
                    id='pairs',
                    options=[],  # The dropdown will update after a market is chosen
                    value='',
                    style={
                        "width": "150px",
                        "background-color": "#000000"
                    },
                    searchable=True,
                    placeholder="Select",
                    disabled=True,
                    clearable=False,
                )
            ], className="row justify-content-start")
        ], className="col")
    ], className="row")
], className="container mt-1")


# Main layout of the application
def main_layout(controls, content, footer):
    layout_out = [
        html.Div(children=[
            html.Nav(children=[
                html.Button([
                    html.Span("apps", className="material-icons")
                ],
                    className="navbar-toggler",
                    type="button",
                    **{
                        'aria-expanded': 'false',
                        "aria-label": "Toggle navigation",
                        'data-toggle': "collapse",
                        "data-target": "#navbarSupportedContent",
                        "aria-controls": "navbarSupportedContent"
                    }
                ),
                html.Div(children=[
                    html.Ul([
                        html.Li(html.A("Chart OHLC", href="#", className="nav-link active"), className="nav-item"),
                        html.Li(html.A("Link 1", href="#", className="nav-link"), className="nav-item"),
                        html.Li(html.A("Link 2", href="#", className="nav-link"), className="nav-item")
                    ], className="navbar-nav mr-auto")
                ], className="collapse navbar-collapse", id="navbarSupportedContent")
            ], className="navbar navbar-expand-sm navbar-dark", style={"background-color": "#000000"})
        ], className="container border-light border-bottom"),
        controls,
        content,
        footer
    ]
    return layout_out


# Content to be used inside the application
content = dcc.Loading(
            type="dot",
            children=html.Div(
                children=[
                    dcc.Interval(
                        id='interval',
                        interval=60*1000,  # in milliseconds
                        n_intervals=0
                    ),
                    dcc.Graph(
                        id='example-graph',
                        figure=go.Figure(data=[]).update_layout(
                            margin={'l': 20, 'b': 30, 't': 10, 'r': 20},
                            template="plotly_dark",
                            height=500,
                            plot_bgcolor='black',
                            paper_bgcolor='black',
                            annotations=[
                                {
                                    "text": "No data to show!<br>Please select a market",
                                    "xref": "paper",
                                    "yref": "paper",
                                    "showarrow": False,
                                    "font":
                                        {
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
                        ),
                        className='mx-2 mt-4'
                    )
                ]
            )
        )


# OHLC chart
def ohlcGraph(market, pair, before=None, after=None, periods=None):
    df = ohlc(market=market, pair=pair, before=before, after=after, periods=periods)
    if df.shape[0] == 0:
        return go.Figure(data=[]).update_layout(
                            margin={'l': 20, 'b': 30, 't': 10, 'r': 20},
                            template="plotly_dark",
                            height=500,
                            plot_bgcolor='black',
                            paper_bgcolor='black',
                            annotations=[
                                {
                                    "text": "No data to show!",
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
        df.CloseTime = pd.to_datetime(df.CloseTime, unit="s")
        df['CloseTime'] = df['CloseTime'].dt.tz_localize('utc').dt.tz_convert('Europe/London')
        df['moving_avg'] = df['ClosePrice'].rolling(5, min_periods=1).mean()
        df['moving_avg_2'] = df['ClosePrice'].ewm(com=0.9).mean()
        df['diff'] = df['moving_avg_2'] - df['moving_avg']
        df['color'] = df['diff'].apply(lambda x: "green" if x > 0 else "red")

        fig = make_subplots(
            rows=3, cols=1,
            row_heights=[0.8, 0.10, 0.1],
            shared_xaxes=True,
            vertical_spacing=0.02)
        fig.add_trace(
            go.Candlestick(x=df.CloseTime,
                           open=df.OpenPrice,
                           high=df.HighPrice,
                           low=df.LowPrice,
                           close=df.ClosePrice,
                           name="OHLC"),
            row=1, col=1)
        fig.add_trace(
            go.Scatter(x=df.CloseTime,
                       y=df.moving_avg,
                       opacity=0.4,
                       line=dict(color='royalblue', dash='dot'),
                       name="MovAvg"),
            row=1, col=1)
        fig.add_trace(
            go.Scatter(x=df.CloseTime,
                       y=df.moving_avg_2,
                       opacity=0.4,
                       line=dict(color='salmon', dash='dot'),
                       name="MovExp"),
            row=1, col=1)
        fig.add_trace(
            go.Bar(x=df.CloseTime,
                   y=df['diff'],
                   opacity=0.5,
                   marker_color=df['color'],
                   name="Ind"),
            row=2, col=1)
        fig.add_trace(
            go.Bar(x=df.CloseTime,
                   y=df.Volume,
                   opacity=0.5,
                   marker_color='blue',
                   name="Volume"),
            row=3, col=1)
        fig.update_layout(xaxis_rangeslider_visible=False,
                          margin={'l': 0, 'b': 50, 't': 0, 'r': 0},
                          showlegend=False,
                          template="plotly_dark",
                          height=700,
                          hovermode='x unified',
                          legend_orientation="h",
                          plot_bgcolor='black',
                          paper_bgcolor='black'
                          )
        fig['layout']['yaxis1']['showspikes'] = True
        fig['layout']['yaxis2']['showgrid'] = False
        fig['layout']['yaxis2']['showticklabels'] = False
        fig['layout']['yaxis2']['showspikes'] = False
        fig['layout']['yaxis3']['showgrid'] = False
        fig['layout']['yaxis3']['showticklabels'] = False
        fig['layout']['yaxis3']['showspikes'] = False
        return fig
