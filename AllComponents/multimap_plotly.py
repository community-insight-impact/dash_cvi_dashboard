import pandas as pd
pd.set_option('display.max_columns', None)
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from AllComponents import dropdown_menu as menu
from AllComponents import sigma_calculation as sig

#MERGE ALL DATA INTO 1 DF
data = pd.read_csv("data/severe_cases_score_data.csv", dtype={'FIPS': str})
data_str = data.applymap(str)
data2 = pd.read_csv("data/economic_score_data.csv", dtype={'FIPS': str})
data3 = pd.read_csv("data/mobile_health_score_data.csv", dtype={'FIPS': str})

#Add county +state name
all_counties = []
big_i = data.shape[0]
for each_i in range(big_i):
    cty= str(data.iloc[each_i]['County'] + ", " + data.iloc[each_i]['State'])
    all_counties.append(cty)
#print(all_counties)
data['County + State'] = all_counties

#FULL DATAFRAME
full_data = data.merge(data2, how='outer').merge(data3, how='outer')
full_data_str = full_data.applymap(str)

#LIST OF ALL STATES
all_states = list(full_data.State.unique())
all_states.insert(0, "United States")

#SCORES
criteria = ['Severe COVID Case Complications', 'Risk of Severe Economic Harm', 'Need for Mobile Health Resources']


#FOR SIDE CHART
indicators_lst = ['Severe COVID Case Complications',
'Risk of Severe Economic Harm', 
'Need for Mobile Health Resources',
'covid_cases',
'Years of Potential Life Lost Rate',
'% Fair or Poor Health',
'% Smokers',
'% Adults with Obesity',
'% Adults with Diabetes',
'% 65 and over',
'% Uninsured',
'% Children in Poverty',
'Income Ratio',
'% Single-Parent Households',
'% Fair or Poor Health',
'% Severe Housing Problems',
'% Enrolled in Free or Reduced Lunch',
'% Unemployed',
'High School Graduation Rate',
'Primary Care Physicians Rate',
'% Home Internet Access'
]

# '% Children in Poverty', 'value': '% Children in Poverty'},
#         {'label': 'Income Ratio', 'value': 'Income Ratio'},
#         {'label': '% Single-Parent Households', 'value': '% Single-Parent Households'},
#         {'label': '% Severe Housing Cost Burden', 'value': '% Fair or Poor Health'},
#         {'label': '% Severe Housing Problems', 'value': '% Severe Housing Problems'},
#         {'label': '% Enrolled in Free or Reduced Lunch', 'value': '% Enrolled in Free or Reduced Lunch'},
#         {'label': '% Unemployed', 'value': '% Unemployed'},
#         {'label': 'High School Graduation Rate', 'value': 'High School Graduation Rate'}]


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


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

#CALCULATE RANGES
index_range = {}
for indicator in indicators_lst:
    if indicator == 'Income Ratio' or indicator == '% 65 and over' or indicator == '% Unemployed':
        index_range[indicator] = sig.calculate_range(full_data, indicator, 1)
    else:
        index_range[indicator] = sig.calculate_range(full_data, indicator)


#FOR HOVERBOARD
data_lst = ['County', 'State'] + indicators_lst
full_data['all_data'] =  full_data['FIPS'] + "<br>" + "County= " + full_data['County'] + "<br>" + "State= " + full_data['State'] #+'<br>' + data['Severe COVID Case Complications']+'<br>' + data['covid_cases']

for indicator in indicators_lst:
    full_data['all_data'] = full_data['all_data'] + "<br>" + indicator +"= " + full_data_str[indicator]

empty_fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=data.FIPS))
empty_fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=3.5, mapbox_center = {"lat": 37.0902, "lon": -95.7129}, showlegend=False, margin={"r":0,"t":0,"l":0,"b":0}, height=None)

map_plus_sidebox = html.Div(id = 'map plus legends', children=
    [html.Div(dcc.Loading(id= 'loading-1',children= [html.Div(dcc.Graph(id='counties-map', figure= empty_fig))], type='default'),
                style= {'width': "79%", 'height':'100%', 'display':'inline-block', 'marginLeft': '5px', 'marginTop': '5px'}),

    html.Div(children=[menu.accordion_box, menu.indicators_shown], style = {'width': '20%'})],
            style= {'width':'100%', 'height':'50%', 'display':'flex', 'zIndex': -2})




#--------------
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# app.layout = html.Div([

# if __name__ == '__main__':
# 	app.run_server(debug=True)


