import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    # these meta_tags ensure content is scaled correctly on different devices
    # see: https://www.w3schools.com/css/css_rwd_viewport.asp for more
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
)

sidebar_header = dbc.Row(
    [dbc.Col(html.H2("Introduction", className="display-4", style = {'font-size':40})),
        dbc.Col(
            [html.Div(
                    # styled into an 'introduction' pull-out tab
                    html.Span(className="navbar-toggler-icon", children="Introduction"),
                    className="navbar-toggler",
                    id="sidebar-toggle"
                ),
            ],
          
            width=3,
            # vertically align the toggle in the center
            align="center",
        ),
    ]
)

sidebar = html.Div(
    [
        sidebar_header,
        html.Div(
            [
                html.Hr(),
                html.P(
                    'How to Use the COVID-19 Community Vulnerability Index',
                    className="lead",
                ),
            ],
            id="blurb", #temporary name
        ),
        #use the Collapse component to animate hiding / revealing introduction
        dbc.Collapse(
            dbc.Card(dbc.CardBody('How to Use the COVID-19 Community Vulnerability Index')),
            id="collapse", 
        ),
    ],
    id="sidebar",
)

content = html.Div(id = 'page-content', children= [
    html.P('Last Updated'),
    html.Div(id='show-time', children = '08/23/2020'),
    ], style={'border': '5px solid gray'}) #temporary content

app.layout = html.Div([sidebar, content])

@app.callback(
    Output("sidebar", "className"),
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar", "className")],
)
def toggle_classname(n, classname):
    if n and classname == "":
        return "collapsed"
    return ""

if __name__ == "__main__":
    app.run_server(port=8888, debug=True)
