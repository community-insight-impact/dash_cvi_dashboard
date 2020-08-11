import dash
import dash_html_components as html


sidebar_header = html.Div(
    [html.Div(children=[html.H2(children='How to Use the COVID-19 Community Vulnerability Index', 
        style = {'font-size':'25px','textAlign':'center'}), 
        html.Img(src= 'https://raw.githubusercontent.com/community-insight-impact/covid_community_vulnerability/master/CVI%20Logo%20FINAL%20ONE%20smaller.png')], 
        id= "title-sidebar",className="display-4"),
        html.Div(
            [html.Div(
                    # styled into an 'introduction' pull-out tab
                    html.Span(className="navbar-toggler-icon", children="Introduction"),
                    className="navbar-toggler",
                    id="sidebar-toggle"
                ),
            ],
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
    ],
    id="sidebar",
)

instruction_pullouttab= html.Div([sidebar], style = {'zIndex':100})