# local imports
from assets.page_layout import index_string, main_layout, dropdowns

# imports
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go


app = dash.Dash(__name__)
app.index_string = index_string


app.layout = html.Div(
    children=main_layout(
        controls=dropdowns,
        content=dcc.Loading(
            type="dot",
            children=html.Div(
                children=[
                    dcc.Interval(
                        id='interval',
                        interval=10*1000,  # in milliseconds
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
                        ),
                        className='mx-2 mt-4'
                    )
                ]
            )
        ),
        footer=None
    )
)

if __name__ == '__main__':
    app.run_server(debug=True)
