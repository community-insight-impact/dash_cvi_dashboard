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
import flask
import glob
import os

picture_dir="/pictures"
#list_of_images = [os.path.basename(x) for x in glob.glob('{}*.png'.format(image_directory))]


data = pd.read_csv("../../../Downloads/covid_community_vulnerability-master/data/severe_cases_score_data.csv", dtype={'FIPS': str})
data_str = data.applymap(str)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

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

index_range = {'Severe COVID Case Complications': (35, 65), 'covid_cases': (1, 500), 'Years of Potential Life Lost Rate': (5146, 11159),
'% Fair or Poor Health': (13.4, 22.6),
'% Smokers': (14.1, 21),
'% Adults with Obesity': (28, 38),
'% Adults with Diabetes':(8.2, 16),
'% 65 and over':(14.5, 23)}

color_scales= {'Severe COVID Case Complications': 'https://raw.githubusercontent.com/community-insight-impact/dash_cvi_dashboard/master/Color%20Scale%20for%20Map/Severe%20COVID%20Case%20Complications.png', 
'covid_cases': 'https://raw.githubusercontent.com/community-insight-impact/dash_cvi_dashboard/master/Color%20Scale%20for%20Map/covid_cases.png', 
'Years of Potential Life Lost Rate': 'https://raw.githubusercontent.com/community-insight-impact/dash_cvi_dashboard/master/Color%20Scale%20for%20Map/Years%20of%20Potential%20Life%20Lost%20Rate.png',
'% Fair or Poor Health': 'https://raw.githubusercontent.com/community-insight-impact/dash_cvi_dashboard/master/Color%20Scale%20for%20Map/%25%20Fair%20or%20Poor%20Health.png',
'% Smokers': 'https://raw.githubusercontent.com/community-insight-impact/dash_cvi_dashboard/master/Color%20Scale%20for%20Map/%25%20Smokers.png',
'% Adults with Obesity': 'https://raw.githubusercontent.com/community-insight-impact/dash_cvi_dashboard/master/Color%20Scale%20for%20Map/%25%20Adults%20with%20Obesity.png',
'% Adults with Diabetes':'https://raw.githubusercontent.com/community-insight-impact/dash_cvi_dashboard/master/Color%20Scale%20for%20Map/%25%20Adults%20with%20Diabetes.png',
'% 65 and over':'https://raw.githubusercontent.com/community-insight-impact/dash_cvi_dashboard/master/Color%20Scale%20for%20Map/%25%2065%20and%20Over.png'}


data_lst = ['County', 'State'] + indicators_lst
data['all_data'] =  data['FIPS'] + "<br>" + "County= " + data['County'] + "<br>" + "State= " + data['State'] 
for indicator in indicators_lst:
	data['all_data'] = data['all_data'] + "<br>" + indicator +"= " + data_str[indicator]


empty_fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=data.FIPS))
empty_fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=3.5, mapbox_center = {"lat": 37.0902, "lon": -95.7129}, showlegend=False)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


#fig = px.choropleth_mapbox(data, geojson=counties, locations = data.FIPS)

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
	style={'width': '50%', 'display': 'inline-block'}),

	html.Div([
		html.Label('Indicator'),
		dcc.Dropdown(
            id='choose-indicator',
            options=[{'label': i, 'value': i} for i in indicators_lst],
            value=[],
            multi = True
            )
    ],
    style={'width': '50%', 'display': 'inline-block'})]),

	
   	html.Div([
	  	dcc.Graph(id='counties-map' , figure=empty_fig)],
   				style= {'width': "85%", 'display':'inline-block'}),
   	html.Div(id = 'container',
   			children= html.Div(id='colorscale-list' , children=[],
   				#[html.Img(id='color-scale', src='https://raw.githubusercontent.com/community-insight-impact/dash_cvi_dashboard/master/Color%20Scale%20for%20Map/%25%20Adults%20with%20Obesity.png'),
   			#html.Img(id='color-scale2', src='https://raw.githubusercontent.com/community-insight-impact/dash_cvi_dashboard/master/Color%20Scale%20for%20Map/%25%20Smokers.png')],
   			style={'label':'no legend','width':200, 'height':400, 'overflowY': 'scroll', 'border': '10px solid gray', 'margin': 10, 'display':'inline-block'}),
   			style= {'width': "15%", 'display':'inline-block'}


   			)] #figure= fig),#WHERE THE MAP WOULD BE
	#html.Div(])[id='intermediate-value', style={'display': 'none'}])

	)
	

@app.callback(
	Output('counties-map', 'figure'),
	[Input('choose-state', 'value'), 
   	Input('choose-indicator', 'value')])



def update_map(chosen_state, chosen_indicator):
	#if chosen_state != None:
	if chosen_state == "United States":
		if len(chosen_indicator) != 0:
			#if chosen_state == "United States":
			fig = px.choropleth_mapbox(data, 
			geojson=counties, locations=data.FIPS, 
			color=chosen_indicator[0],
			color_continuous_scale=colors[chosen_indicator[0]],
			range_color=index_range[chosen_indicator[0]],
			mapbox_style="carto-positron",				
			zoom=3.5, center = {"lat": 37.0902, "lon": -95.7129},
			opacity=0.8,
			labels={chosen_indicator[0]}, hover_data= ['County', 'State'] + indicators_lst
			)
			fig.update_layout(coloraxis_showscale=False, title_text = chosen_indicator[0], margin={"r":0,"t":0,"l":0,"b":0})
		#fig.update_layout(title_text = chosen_indicator[0], margin={"r":0,"t":0,"l":0,"b":0})
			if len(chosen_indicator) > 1:
				for val_indx in range(1, len(chosen_indicator)):

					fig.add_trace(go.Choroplethmapbox(name = chosen_indicator[val_indx], geojson=counties, locations=data.FIPS, z=data[chosen_indicator[val_indx]],
						colorscale=colors[chosen_indicator[val_indx]],
						zmin=index_range[chosen_indicator[val_indx]][0],
						zmax=index_range[chosen_indicator[val_indx]][1],
						marker_line_width=0.1, marker_opacity=0.8, showscale=False, #hovertemplate =  "FIPS=%{data.FIPS}<br>County=%%{data.County}<br>State=%%{data.State}<extra></extra>"))
						text= data['all_data'], hovertemplate = 'FIPS= %{text} <extra></extra>'))#, hovertemplate= data_lst ))#, hovertext=[data[y] for y in indicators_lst]))
						#hovertemplate=[County: %{data['County']}, State:%{data['State']}] + [y: %{data[y]} for y in indicators_lst]))
					fig.update_layout(title_text = chosen_indicator[0], margin={"r":0,"t":0,"l":0,"b":0})
					#fig.update_layout(hover_data= ['County', 'State'] + indicators_lst)
		else:
		 	fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=data.FIPS))
		 	fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=3.5, mapbox_center = {"lat": 37.0902, "lon": -95.7129}, showlegend=False)
		#fig.update_trace(hover_data= ['County', 'State'] + indicators_lst)
		#geojson=counties, locations=data.FIPS, hover_data= ['County', 'State'] + indicators_lst))
		return fig
	else:
		dff = data[data['State'] == chosen_state]
		if len(chosen_indicator) != 0:
			#if chosen_state == "United States":
			fig = px.choropleth_mapbox(dff, 
				geojson=counties, locations=dff.FIPS, 
				color=chosen_indicator[0],
				color_continuous_scale=colors[chosen_indicator[0]],
				range_color=index_range[chosen_indicator[0]],
				mapbox_style="carto-positron",
				zoom=3.5, center = {"lat": 37.0902, "lon": -95.7129},
				opacity=0.8,
				labels={chosen_indicator[0]}, hover_data= ['County', 'State'] + indicators_lst
				)
			fig.update_layout(coloraxis_showscale=False, title_text = chosen_indicator[0], margin={"r":0,"t":0,"l":0,"b":0})
			if len(chosen_indicator) > 1:
				for val_indx in range(1, len(chosen_indicator)):
					fig.add_trace(go.Choroplethmapbox(geojson=counties, locations=dff.FIPS, z=dff[chosen_indicator[val_indx]],
					colorscale=colors[chosen_indicator[val_indx]],
					zmin=index_range[chosen_indicator[val_indx]][0],
					zmax=index_range[chosen_indicator[val_indx]][1],
					marker_line_width=0.1, marker_opacity=0.8, showscale=False, text= dff['all_data'], hovertemplate = 'FIPS= %{text} <extra></extra>'))
					#fig.update_layout(coloraxis_showscale=False, title_text = chosen_indicator[val_indx], margin={"r":0,"t":0,"l":0,"b":0})
			else:
				fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=data.FIPS))
				fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=3.5, mapbox_center = {"lat": 37.0902, "lon": -95.7129}, showlegend=False)
		return fig 



@app.callback(
	Output('container', 'children'),
	[Input('choose-indicator','value')])

def update_color_scale(chosen_indicators):
	all_scales = []
	if len(chosen_indicators) != 0:
		for indicator in chosen_indicators:
			all_scales.append(html.Img(src=color_scales[indicator]))
		return html.Div(children=all_scales, style= {'label':'Legends','width':200, 'height':400, 'overflowY': 'scroll', 'border': '10px solid gray', 'margin': 10})


if __name__ == '__main__':
	app.run_server(debug=True)




