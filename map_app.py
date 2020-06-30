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

indicators_lst = ['Severe COVID Case Complications',
'covid_cases',
'Years of Potential Life Lost Rate',
'% Fair or Poor Health',
'% Smokers',
'% Adults with Obesity',
'% Adults with Diabetes',
'% 65 and over']


all_states = list(data.State.unique())
all_states.insert(0, "United States")


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


colors = {'Severe COVID Case Complications': ['#fdc1f6', '#ff385e'], 'covid_cases': ['#bdb4fe', '#0d0c54'],
 'Years of Potential Life Lost Rate': ['#bdb4fe', '#0d0c54'], '% Fair or Poor Health': ['#bdb4fe', '#0d0c54'],
'% Smokers': ['#bdb4fe', '#0d0c54'],
'% Adults with Obesity':['#bdb4fe', '#0d0c54'],
'% Adults with Diabetes':['#bdb4fe', '#0d0c54'],
'% 65 and over':['#bdb4fe', '#0d0c54'] }





#object for app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


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
            value='Severe COVID Case Complications',
            #multi = True
            )
    ],
    style={'width': '48%', 'display': 'inline-block'})]),

    dcc.Graph(id='counties-map')#WHERE THE MAP WOULD BE
    

])


@app.callback(
	Output('counties-map', 'figure'),
   	[Input('choose-state', 'value'), 
   	Input('choose-indicator', 'value')])

def update_map(chosen_state, chosen_indicator):
	if chosen_state == "United States":
		fig =  px.choropleth_mapbox(data, geojson=counties, locations=data.FIPS, color=chosen_indicator,
                           color_continuous_scale=colors[chosen_indicator],
                           #range_color=(min(data[chosen_indicator]), max(data[chosen_indicator])),
                           mapbox_style="carto-positron",
                           zoom=3.5, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.8,
                           labels={chosen_indicator}, hover_data= indicators_lst
                          )
		fig.update_layout(title_text = chosen_indicator, margin={"r":0,"t":0,"l":0,"b":0})
	else: 
		dff = data[data['State'] == chosen_state]
		fig = px.choropleth_mapbox(dff, geojson=counties, locations=dff.FIPS, color=chosen_indicator,
                           color_continuous_scale=colors[chosen_indicator],
                           #range_color=(min(dff[chosen_indicator]), max(dff[chosen_indicator])),
                           mapbox_style="carto-positron",
                           zoom=3.5, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.8,
                           labels={chosen_indicator},
							hover_data = indicators_lst)
		fig.update_layout(
		title_text = chosen_indicator,
	   	margin={"r":0,"t":0,"l":0,"b":20})
	return fig
							
                         

if __name__ == '__main__':
    app.run_server(debug=True)

