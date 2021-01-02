import dash_core_components as dcc
import dash_html_components as html
from AllComponents import dropdown_menu as menu
#from AllComponents import sigma_calculation as sig


#ALL METRICS
colors_map = {'Severe COVID Case Complications': ['#fdc1f6', '#ff385e'], 'covid_cases': ['#bdb4fe', '#0d0c54'],
 'Hypertension Death Rate': ['#bdb4fe', '#0d0c54'],
'% Smokers': ['#bdb4fe', '#0d0c54'],
'% Adults with Obesity':['#bdb4fe', '#0d0c54'],
'% Diagnosed Diabetes':['#bdb4fe', '#0d0c54'],
'% Adults 65 and Older':['#bdb4fe', '#0d0c54'],
'Heart Disease Death Rate': ['#bdb4fe', '#0d0c54'],

'Risk of Severe Economic Harm':['#40fcc7', '#0c3f47'],
'% Uninsured': ['#bdb4fe', '#0d0c54'],
'% Children in Poverty': ['#bdb4fe', '#0d0c54'],
'Income Ratio':['#bdb4fe', '#0d0c54'],
'% Single-Parent Households':['#bdb4fe', '#0d0c54'],
'% Severe Housing Cost Burden': ['#bdb4fe', '#0d0c54'],
'% Severe Housing Problems': ['#bdb4fe', '#0d0c54'],
'% Enrolled in Free or Reduced Lunch':['#bdb4fe', '#0d0c54'],
'% Unemployed':['#bdb4fe', '#0d0c54'],
'High School Graduation Rate':['#bdb4fe', '#0d0c54'],

'Need for Mobile Health Resources':['#ffc05f', '#d81405'],
'% Rural': ['#bdb4fe', '#0d0c54'],
'% households wo car':['#bdb4fe', '#0d0c54'],
'% workers commuting by public transit': ['#bdb4fe', '#0d0c54'],
'Primary Care Physicians Rate':['#bdb4fe', '#0d0c54'],
'% Without Health Insurance': ['#bdb4fe', '#0d0c54'],
'% Nonwhite': ['#bdb4fe', '#0d0c54'],
'% Limited English Proficiency': ['#bdb4fe', '#0d0c54'],
'% Veterans in Civilian Adult Population': ['#bdb4fe', '#0d0c54'],
'% disabled':['#bdb4fe', '#0d0c54'],
'opioid death rate': ['#bdb4fe', '#0d0c54'],
'% Fair or Poor Health': ['#bdb4fe', '#0d0c54'],
'Number of Hospitals': ['#bdb4fe', '#0d0c54']
}

#style is the same format as HTML/CSS
map_plus_sidebox = html.Div(id = 'map-legends', children=
    [html.Div(id = "inner-map", children = dcc.Loading(id= 'loading-1',children= [html.Div(dcc.Graph(id='counties-map', #figure= empty_fig
        ))], type='default'),
        style= {'width': "79%", 'height':'100%', 'display':'inline-block', 'marginLeft': '5px'}),

    html.Div(children=[menu.accordion_box, menu.indicators_shown], style = {'width': '20%'})],
            style= {'width':'100%', 'height':'50%', 'display':'flex', 'zIndex': -2})





#--------------
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# app.layout = html.Div([

# if __name__ == '__main__':
#   app.run_server(debug=True)



