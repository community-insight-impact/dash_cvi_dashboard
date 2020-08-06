import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


sidebar_header = dbc.Row(
    [dbc.Col(children=[html.H2(children='How to Use the COVID-19 Community Vulnerability Index', 
        style = {'font-size':'25px','textAlign':'center'}), 
        html.Img(src= 'https://raw.githubusercontent.com/community-insight-impact/covid_community_vulnerability/master/CVI%20Logo%20FINAL%20ONE%20smaller.png')], 
        id= "title-sidebar",className="display-4", align='center'),
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
    [sidebar_header,
    html.Div(className= 'sidebar-para', children=[html.Hr(),
            html.Div(children= [
                html.P("This dashboard is part of an open source project designed to effectively understand community needs and allocate resources at the county level.\
                    Use this dashboard to visualize different health and demographic variables at the county level and assess county risk levels based on those variables. Interact with the map by zooming in on a specific area or search for a location by clicking the Magnifying Glass icon in the top right corner of the map. Use the Layers icon (to the right of the Magnifying Glass) to map a metric or an individual variable dataset. \
                    Click on a county on the map to view COVID-19 and population census data for that county. On the right side of the screen, select a state with the dropdown menu to view county vulnerability scores and rankings within that state.\
                    In those modules, use the arrows at the bottom to toggle between the scores for different metrics. \
                    For more information about the project, click the Menu icon in the top right corner. Feel free to reach out to our team with any questions or ideas!",
                className="lead",
                style = {'fontSize': '16px'})], style={'width': '100%', 'overflowY': 'scroll'})],
            id="blurb", #temporary name
        style={'width': '100%', 'overflowY': 'scroll'}),
        #use the Collapse component to animate hiding / revealing introduction
        # dbc.Collapse(
        #     dbc.Card(dbc.CardBody()),
        #     id="collapse", 
        # ),
    ],
    id="sidebar",
)

instruction_pullouttab= html.Div([sidebar], style = {'zIndex':100})

# app = dash.Dash(
#     external_stylesheets=[dbc.themes.BOOTSTRAP],
#     # these meta_tags ensure content is scaled correctly on different devices
#     # see: https://www.w3schools.com/css/css_rwd_viewport.asp for more
#     meta_tags=[
#         {"name": "viewport", "content": "width=device-width, initial-scale=1"}
#     ],
# )


# @app.callback(
#     Output("sidebar", "className"),
#     [Input("sidebar-toggle", "n_clicks")],
#     [State("sidebar", "className")],
# )
# def toggle_classname(n, classname):
#     if n and classname == "":
#         return "collapsed"
#     return ""

# if __name__ == "__main__":
#     app.run_server(port=8888, debug=True)
