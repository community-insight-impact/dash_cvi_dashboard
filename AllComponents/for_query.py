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


data = pd.read_csv("../../../Downloads/covid_community_vulnerability-master/data/severe_cases_score_data.csv", dtype={'FIPS': str})
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


long_lat = pd.read_csv('../data/long_lat.csv')


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


fig = px.choropleth_mapbox(data, geojson=counties, locations=data.FIPS, color=data['Severe COVID Case Complications'],
                           color_continuous_scale='Blues',
                           range_color=(35,65),
                           mapbox_style="carto-positron",
                           zoom=3.5, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.1,
                           labels={"severe_cases_score_data"},
						hover_data = ['County', 'State'] + indicators_lst)
fig.update_traces(marker={"line":{"width":2, 'color':'DarkSlateGrey'}})
fig.update_layout(
		title_text = 'severe_cases_score_data',
	   	margin={"r":0,"t":0,"l":0,"b":20})

dff = data[data['County']== 'Harris'][data['State'] == 'Texas'] 
#dff = dff1[dff1['State'] == 'Texas']
fig2 = px.choropleth_mapbox(dff, geojson=counties, locations=dff.FIPS, color=dff['Severe COVID Case Complications'],
                           color_continuous_scale='Blues',
                           range_color=(35,65),
                           mapbox_style="carto-positron",
                           zoom=5, center = {'lat' : float(long_lat[long_lat['name'] == 'Texas']['latitude']), "lon": float(long_lat[long_lat['name'] == 'Texas']['longitude'])},
                           opacity=0.1,
                           labels={"severe_cases_score_data"},
						hover_data = ['County', 'State'] + indicators_lst)
fig2.update_traces(marker={"line":{"width":8, 'color':'Fuchsia'}})
fig.update_layout(
		#title_text = 'severe_cases_score_data',
	   	margin={"r":0,"t":0,"l":0,"b":20})

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']



#object for app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


#CHANGE TIME PERIOD?
app.layout = html.Div([
	html.Div([
		html.Div([
			html.Label('Choose State'),
			dcc.Dropdown(
				id = 'choose-state',
				options= [{'label': state, 'value': state} for state in all_states],
				value= 'United States'
)
],
	style={'width': '48%', 'display': 'inline-block'}),

	html.Div([
		html.Label('Indicator'),
		dcc.Dropdown(
            id='choose-indicator',
            options=[{'label': i, 'value': i} for i in indicators_lst],
            value='Severe COVID Case Complications'
            )
    ],
    style={'width': '48%', 'display': 'inline-block'})]),

    #dcc.Graph(id='counties-map', figure=fig),#WHERE THE MAP WOULD BE
  	dcc.Graph(id='counties-map2', figure=fig2)  

])


if __name__ == '__main__':
    app.run_server(debug=True)

