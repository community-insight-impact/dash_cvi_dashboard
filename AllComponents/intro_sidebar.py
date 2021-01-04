import dash
import dash_html_components as html
import dash_bootstrap_components as dbc


sidebar_header = html.Div(
    [html.Div(children=[html.H2(children='How to Use the COVID-19 Community Vulnerability Index', 
        style = {'font-size':'25px','textAlign':'center'}), 
        html.Img(src= 'https://raw.githubusercontent.com/community-insight-impact/covid_community_vulnerability/master/CVI%20Logo%20FINAL%20ONE%20smaller.png')], 
        id= "title-sidebar",className="display-4"),
       
    ]
)

sidebar = html.Div(
    [sidebar_header,
    html.Div(className= 'sidebar-para', children=[html.Hr(),
            html.Div(children= [
                html.P("The "), 
                html.P("Covid-19 Community Vulnerability Index ", className = "bold"),
                html.P("is part of "), 
                html.A(href = "https://github.com/community-insight-impact/covid_community_vulnerability",
                    children = "an open source project", target="_blank", rel="noopener noreferrer"),
                    html.P([" aiming to effectively understand community needs, so that resources can be equitably allocated at the county level.\n", html.Br()], className = "spacebtwn"),
                    html.P(["Use this dashboard to visualize community needs assessment scores related to the impact of COVID-19, at the county level. Also map the underlying health and demographic variables used to build the scores.\n", html.Br()], className = "spacebtwn"),
                    html.P(["Assess county risk levels based on those scores.\n", html.Br()], className = "spacebtwn"),
                    html.P(["Choose a Location\n", html.Br()], className = "underline"),
                    html.P(["Zoom on the map or use the \"Filter by State\" and \"Filter by County\" dropdown menus above the map.\n", html.Br()], className = "spacebtwn"),
                    html.P(["Map a Metric or Variable Data Set\n", html.Br()], className= "underline"),
                    html.P(["Select a metric to map in the box on the right of the map.\n", html.Br()], className = "spacebtwn"),
                    html.P(["View Detailed Data for A County\n",html.Br()] , className = "underline"),
                    html.P(["Click on a county on the map to view COVID-19 and population census data.\n",html.Br()], className = "spacebtwn"),
                    html.P(["In the lower right hand corner, view the top 50 county vulnerability scores and rankings in a specific state.\
                    Use the arrows at the bottom of the module to toggle between the scores for different metrics.\
                    Change the state with the \"Filter by State\" dropdown menu above the map.\n",html.Br()], className = "spacebtwn"),
                    html.P("For more information ", className="bold"),
                    html.P("about the project, click  the Menu icon in the top right corner. Feel free to reach out to "),
                    html.A(href= "mailto: covid.vulnerability@gmail.com", children = "covid.vulnerability@gmail.com",  target="_blank", rel="noopener noreferrer"),
                    html.P(" to our team with any questions or ideas!\n"
                )], className="lead",
                    )],
            id="blurb", #temporary name
    )],
    id="sidebar"
)

instruction_pullouttab= html.Div([sidebar,
     html.Div(
            [html.Div(
                    # styled into an 'introduction' pull-out tab
                    html.Span(className="navbar-toggler-icon", children="Instructions"),
                    className="navbar-toggler",
                    id="sidebar-toggle"
                ),
            ],
        ),], style = {'zIndex':100}, id='intro-container')

