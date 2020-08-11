import dash_core_components as dcc
import dash_html_components as html
from AllComponents import dropdown_menu as menu
#from AllComponents import sigma_calculation as sig

colors_map = {'Severe COVID Case Complications': ['#fdc1f6', '#ff385e'], 'covid_cases': ['#bdb4fe', '#0d0c54'],
 'Years of Potential Life Lost Rate': ['#bdb4fe', '#0d0c54'], '% Fair or Poor Health': ['#bdb4fe', '#0d0c54'],
'% Smokers': ['#bdb4fe', '#0d0c54'],
'% Adults with Obesity':['#bdb4fe', '#0d0c54'],
'% Adults with Diabetes':['#bdb4fe', '#0d0c54'],
'% 65 and over':['#bdb4fe', '#0d0c54'],
'% Uninsured': ['#bdb4fe', '#0d0c54'],
'% Children in Poverty': ['#bdb4fe', '#0d0c54'],
'Income Ratio':['#bdb4fe', '#0d0c54'],
'% Single-Parent Households':['#bdb4fe', '#0d0c54'],
'% Fair or Poor Health':['#bdb4fe', '#0d0c54'],
'% Severe Housing Problems': ['#bdb4fe', '#0d0c54'],
'% Enrolled in Free or Reduced Lunch':['#bdb4fe', '#0d0c54'],
'% Unemployed':['#bdb4fe', '#0d0c54'],
'High School Graduation Rate':['#bdb4fe', '#0d0c54'],
'Primary Care Physicians Rate':['#bdb4fe', '#0d0c54'],
'% Home Internet Access' :['#bdb4fe', '#0d0c54'],
'Risk of Severe Economic Harm':['#40fcc7', '#0c3f47'], 
'Need for Mobile Health Resources':['#ffc05f', '#d81405']
}


map_plus_sidebox = html.Div(id = 'map plus legends', children=
    [html.Div(dcc.Loading(id= 'loading-1',children= [html.Div(dcc.Graph(id='counties-map', #figure= empty_fig
        ))], type='default'),
                style= {'width': "79%", 'height':'100%', 'display':'inline-block', 'marginLeft': '5px', 'marginTop': '5px'}),

    html.Div(children=[menu.accordion_box, menu.indicators_shown], style = {'width': '20%'})],
            style= {'width':'100%', 'height':'50%', 'display':'flex', 'zIndex': -2})




#--------------
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# app.layout = html.Div([

# if __name__ == '__main__':
# 	app.run_server(debug=True)


