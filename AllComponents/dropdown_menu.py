import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

accordion_text_colors = ['#ff385e', '#0c3f47', '#ffc05f']

criteria = ['Severe COVID Case Complications', 'Risk of Severe Economic Harm', 'Need for Mobile Health Resources']

#CONTENTS OF ACCORDION 
item0 = html.Div([
    html.P('Describes likelihood that constituents within a community will develop severe complications following covid-19 infection', style = {'margin-bottom': 20}),
    html.P('Includes:'),
    dcc.Checklist(id="severe-indicators", options=[ {'label': 'Number of COVID cases', 'value': 'covid_cases'},
        {'label': '% 65 and over', 'value': '% 65 and over'},
        {'label': '% Adults with Obesity', 'value': '% Adults with Obesity'},
        {'label': '% Adults with Diabetes', 'value': '% Adults with Diabetes'},
        {'label': '% Smokers', 'value': '% Smokers'},
        {'label': 'Years of Potential Life Lost Rate', 'value': 'Years of Potential Life Lost Rate'},
        {'label': '% Fair or Poor Health', 'value': '% Fair or Poor Health'}], value=[], inputClassName= "fa fa-square-o")
        ]#, style={'display': 'grid'}
        )

item1 = html.Div([
    html.P('Describes existing need for food-based community efforts, services, and nonprofits', style={'margin-bottom': 20}),
    html.P('Includes:'),
    dcc.Checklist(id="economic-indicators", options=[ 
        {'label': '% Uninsured', 'value': '% Uninsured'},
        {'label': '% Children in Poverty', 'value': '% Children in Poverty'},
        {'label': 'Income Ratio', 'value': 'Income Ratio'},
        {'label': '% Single-Parent Households', 'value': '% Single-Parent Households'},
        {'label': '% Severe Housing Cost Burden', 'value': '% Fair or Poor Health'},
        {'label': '% Severe Housing Problems', 'value': '% Severe Housing Problems'},
        {'label': '% Enrolled in Free or Reduced Lunch', 'value': '% Enrolled in Free or Reduced Lunch'},
        {'label': '% Unemployed', 'value': '% Unemployed'},
        {'label': 'High School Graduation Rate', 'value': 'High School Graduation Rate'},
        {'label': 'Number of Covid Cases', 'value': 'covid_cases'}], value=[], inputClassName= "fa fa-square-o")
    ])

item2 = html.Div([
    html.P('Describes the likelihood that a community could benefit from mobile health services', style={'margin-bottom': 20}),
    html.P('Includes:'),
    dcc.Checklist(id="mobile-indicators", options=[ #{'label': 'Number of COVID cases', 'value': 'covid_cases'},
        #{'label': 'Risk of Severe Economic Harm', 'value': 'Risk of Severe Economic Harm'},
        {'label': '% Uninsured', 'value': '% Uninsured'},
        {'label': '% 65 and over', 'value': '% 65 and over'},
        {'label': '% Adults with Obesity', 'value': '% Adults with Obesity'},
        {'label': '% Adults with Diabetes', 'value': '% Adults with Diabetes'},
        {'label': '% Smokers', 'value': '% Smokers'},
        {'label': 'Primary Care Physicians Rate', 'value': 'Primary Care Physicians Rate'},
        {'label': '% Fair or Poor Health', 'value': '% Fair or Poor Health'},
        {'label': '% Home Internet Access', 'value': '% Home Internet Access'}], value=[], inputClassName= "fa fa-square-o")
    ])

graph_info =[item0, item1, item2]

def make_item(i):
    # we use this function to make the example items to avoid code duplication
    return dbc.Card(
        [
            dbc.CardHeader(
                html.Div(
                    children=[
                        dcc.Checklist(id= f"checkbox-{i}", options= [{'label': criteria[i], 'value': criteria[i]}], 
                            inputStyle = {'display': 'inline-block', 'marginRight':'5px'},  labelStyle= {'marginBottom':'5px','fontSize':'14px', 'display': 'inline-block', 'color': accordion_text_colors[i]}, 
                            value=[]),
                        html.I(id=f"score-{i}-toggle", className="fa fa-caret-right", **{'aria-hidden': 'true'}, style= {'fontSize': '15px', 'display':'inline-block', 'position': 'relative', 'float':'right', 'marginTop':'-23px'
                        })],
                  style= {'verticalAlign':'middle', }), 
            style={'height':'30%'}),
            dbc.Collapse(
                dbc.CardBody(graph_info[i]),
                id=f"collapse-{i}",
            )
        ],
    )

accordion = html.Div([make_item(0), make_item(1), make_item(2)], className="accordion")

accordion_box = html.Div([
    html.Label('Select a Metric:', style={'verticalAlign':'middle', 'padding': 10}), 
    html.Div(accordion, style = {'width': '100%', 'overflowY':'scroll'})],
        style={'height':'350px', 'width':'100%', 'overflowY':'scroll', 'border': '5px solid gray', 'margin': 5})

indicators_shown = html.Div(id = "indicators-box", children= [html.P(children="Indicators shown:"), html.Div(id='indicators-shown', children= [])], style= {'height':'90px',"overflowY": 'scroll',
    'border': '5px solid gray', 'margin': '5px', 'padding': '5px', 'width':'100%'})






