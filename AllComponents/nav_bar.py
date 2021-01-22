import dash_html_components as html
import dash_bootstrap_components as dbc

#Navigation Bar at the right corner of the dashboard

logo = "https://raw.githubusercontent.com/community-insight-impact/covid_community_vulnerability/master/CVI%20Logo.png"
nav_bar = html.Div(
    children=[
        dbc.Navbar(className="navbar",
            children=[
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=logo, height="30px")),
                            dbc.Col(dbc.Navbar("COVID-19 Community Vulnerability Index")),
                        ],
                        align="center",
                        no_gutters=True,
                    ),
                ),
                dbc.NavbarToggler(id="navbar-toggler"),
            # dbc.Collapse(nav_bar, id="navbar-collapse", navbar=True),
            ],
            color="dark",
            dark=True,
        ),
        dbc.DropdownMenu(className="dropdown",
                    label='Menu',
                    in_navbar=True,
                    children=[
                        dbc.DropdownMenuItem('About', href='https://github.com/community-insight-impact/covid_community_vulnerability', target="_blank"), 
                        dbc.DropdownMenuItem('Dataset', href='https://github.com/community-insight-impact/covid_community_vulnerability/blob/master/data/full_dataset.md', target="_blank"),
                        dbc.DropdownMenuItem('Methodology', href='https://github.com/community-insight-impact/covid_community_vulnerability/blob/master/documentation/methodology.md', target="_blank"),#, style = {'display':'inline-block'})
                    ],
            ),
    ],
)

