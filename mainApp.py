# local imports
from assets.page_layout import index_string, main_layout, dropdowns, content
from assets.get_data import pairs_list

# imports
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate


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


if __name__ == '__main__':
    app.run_server(debug=True)
