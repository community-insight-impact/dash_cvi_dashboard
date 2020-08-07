# import pandas as pd
# pd.set_option('display.max_columns', None)
# from urllib.request import urlopen
# import json
# with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
#     counties = json.load(response)
# import plotly.express as px
# import plotly.graph_objects as go
# import dash
# import dash_core_components as dcc
import dash_html_components as html
# from dash.dependencies import Input, Output
# from AllComponents import dropdown_menu as menu
#import multimap_plotly as multimap 
#import sigma_calculation as sig

import base64

#MERGE ALL DATA INTO 1 DF
# data = pd.read_csv("data/severe_cases_score_data.csv", dtype={'FIPS': str})
# data_str = data.applymap(str)
# data2 = pd.read_csv("data/economic_score_data.csv", dtype={'FIPS': str})
# data3 = pd.read_csv("data/mobile_health_score_data.csv", dtype={'FIPS': str})

# #Add county +state name
# all_counties = []
# big_i = data.shape[0]
# for each_i in range(big_i):
#     cty= str(data.iloc[each_i]['County'] + ", " + data.iloc[each_i]['State'])
#     all_counties.append(cty)
# #print(all_counties)
# data['County + State'] = all_counties

# #FULL DATAFRAME
# full_data = data.merge(data2, how='outer').merge(data3, how='outer')
# full_data_str = full_data.applymap(str)

# #LIST OF ALL STATES
# all_states = list(full_data.State.unique())
# all_states.insert(0, "United States")

# #SCORES
# criteria = ['Severe COVID Case Complications', 'Risk of Severe Economic Harm', 'Need for Mobile Health Resources']


# #FOR SIDE CHART
# indicators_lst = ['Severe COVID Case Complications',
# #'Risk of Severe Economic Harm', 
# #'Need for Mobile Health Resources',
# 'covid_cases',
# 'Years of Potential Life Lost Rate',
# '% Fair or Poor Health',
# '% Smokers',
# '% Adults with Obesity',
# '% Adults with Diabetes',
# '% 65 and over',
# '% Uninsured',
# '% Children in Poverty',
# 'Income Ratio',
# '% Single-Parent Households',
# '% Fair or Poor Health',
# '% Severe Housing Problems',
# '% Enrolled in Free or Reduced Lunch',
# '% Unemployed',
# 'High School Graduation Rate',
# 'Primary Care Physicians Rate',
# '% Home Internet Access',
# 'Risk of Severe Economic Harm', 
# 'Need for Mobile Health Resources',
# ]

# # '% Children in Poverty', 'value': '% Children in Poverty'},
# #         {'label': 'Income Ratio', 'value': 'Income Ratio'},
# #         {'label': '% Single-Parent Households', 'value': '% Single-Parent Households'},
# #         {'label': '% Severe Housing Cost Burden', 'value': '% Fair or Poor Health'},
# #         {'label': '% Severe Housing Problems', 'value': '% Severe Housing Problems'},
# #         {'label': '% Enrolled in Free or Reduced Lunch', 'value': '% Enrolled in Free or Reduced Lunch'},
# #         {'label': '% Unemployed', 'value': '% Unemployed'},
# #         {'label': 'High School Graduation Rate', 'value': 'High School Graduation Rate'}]


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# colors_map = {'Severe COVID Case Complications': ['#fdc1f6', '#ff385e'], 'covid_cases': ['#bdb4fe', '#0d0c54'],
#  'Years of Potential Life Lost Rate': ['#bdb4fe', '#0d0c54'], '% Fair or Poor Health': ['#bdb4fe', '#0d0c54'],
# '% Smokers': ['#bdb4fe', '#0d0c54'],
# '% Adults with Obesity':['#bdb4fe', '#0d0c54'],
# '% Adults with Diabetes':['#bdb4fe', '#0d0c54'],
# '% 65 and over':['#bdb4fe', '#0d0c54'],
# '% Uninsured': ['#bdb4fe', '#0d0c54'],
# '% Children in Poverty': ['#bdb4fe', '#0d0c54'],
# 'Income Ratio':['#bdb4fe', '#0d0c54'],
# '% Single-Parent Households':['#bdb4fe', '#0d0c54'],
# '% Fair or Poor Health':['#bdb4fe', '#0d0c54'],
# '% Severe Housing Problems': ['#bdb4fe', '#0d0c54'],
# '% Enrolled in Free or Reduced Lunch':['#bdb4fe', '#0d0c54'],
# '% Unemployed':['#bdb4fe', '#0d0c54'],
# 'High School Graduation Rate':['#bdb4fe', '#0d0c54'],
# 'Primary Care Physicians Rate':['#bdb4fe', '#0d0c54'],
# '% Home Internet Access' :['#bdb4fe', '#0d0c54'],
# 'Risk of Severe Economic Harm':['#40fcc7', '#0c3f47'], 
# 'Need for Mobile Health Resources':['#ffc05f', '#d81405']
# }

#CALCULATE RANGES
# index_range = {}
# for indicator in indicators_lst:
#     if indicator == 'Income Ratio' or indicator == '% 65 and over' or indicator == '% Unemployed':
#         index_range[indicator] = sig.calculate_range(full_data, indicator, 1)
#     else:
#         index_range[indicator] = sig.calculate_range(full_data, indicator)

#help(plotly.colors.diverging)

#color = px.colors.sequential.Plasma([(0.00, "red"),   (0.33, "red"),
 #                                                    (0.33, "green"), (0.66, "green"),
  #                                                   (0.66, "blue"),  (1.00, "blue")])
# app = dash.Dash(__name__, external_stylesheets= external_stylesheets, 
#     meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

#app.layout = html.Div(color)

# index_range = {'Severe COVID Case Complications': (35, 65), 'Risk of Severe Economic Harm': (30, 65), 'Need for Mobile Health Resources': (32, 68), 'covid_cases': (1, 5682), 'Years of Potential Life Lost Rate': (4595, 11274), '% Fair or Poor Health': (13, 23), '% Smokers': (14, 21), '% Adults with Obesity': (27, 38), '% Adults with Diabetes': (8, 16), '% 65 and over': (14.5, 23.8), '% Uninsured': (7, 20), '% Children in Poverty': (12, 30), 'Income Ratio': (3.8, 5.3), '% Single-Parent Households': (22, 43), '% Severe Housing Problems': (9, 18), '% Enrolled in Free or Reduced Lunch': (31, 73), '% Unemployed': (2.7, 5.6), 'High School Graduation Rate': (71, 102), 'Primary Care Physicians Rate': (17, 88), '% Home Internet Access': (53, 87)}

#df = px.data.gapminder().query("year==2007")

# def make_graph(num):
# 	fig = px.choropleth_mapbox(full_data, 
#             geojson=counties, locations=full_data['FIPS'], 
#             color=indicators_lst[num],
#             color_continuous_scale=colors_map[indicators_lst[num]],
#             range_color=index_range[indicators_lst[num]],
#             mapbox_style="carto-positron",              
#             zoom=3.5, center = {"lat": 37.0902, "lon": -95.7129},
#             opacity=0.8,
#             labels={'covid_cases'}, hover_data= ['County', 'State'] + indicators_lst,
#             )
# 	fig.update_layout(coloraxis_showscale=True, title_text = indicators_lst[0], 
# 		width =800, height= 350, 
# 		margin={"r":50,"t":0,"l":0,"b":0})
# 	return fig

# fig = make_graph(20)
#fig.show()
# fig.update_layout(coloraxis_colorbar=dict(
#     title="covid_cases",
#     thicknessmode="pixels",
#     thickness=150,
#     lenmode="pixels", 
#     len=200,
#     yanchor="top", y=1,
#     ticks="outside", ticksuffix="cases",
#     dtick=5
# ))

def make_legend(index):
	image_filename = "colorscales/" + str(index) + ".png" # replace with your own image
	encoded_image = base64.b64encode(open(image_filename, 'rb').read())
	return html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))

# pic = make_legend(0)
# pic.show

# app.layout = html.Div([
#     html.Img(src='data:image/png;base64,{}'.format(encoded_image))
# ])


	#fig.show()

#for num in range(len(indicators_lst)):
#make_graph(19)

# map_example = html.Div(className='map-example',children = dcc.Graph(figure=make_graph(0)),
# 	 style= {'width': "79%", 'height':'100%', 'marginLeft': '5px'})
#html.Div(className='map-example',children = dcc.Graph(figure=make_graph(0)), )#style ={'width': 300, 'height':500})


# app = dash.Dash(__name__, external_stylesheets= external_stylesheets, 
#     meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

color_scale = html.Div(id= 'color-scales', className= 'legend',children=[])

# app.layout = html.Div(children=[map_example, 
# 	color_scale], 
# 	style = { 'height':'50%', 
# 	#'display':'flex', 
# 	'zIndex': -2})

# help(go.layout.Template)

# import plotly.io as pio
# plotly_template = pio.templates["plotly"]
# plotly_template.layout


# color_template = go.layout.Template()
# color_template.data.mesh3d =[go.Mesh3d(
#     #color = purple,
#     cmin = 23,
#     cmax= 24)]


# help(go.layout.Template().data)







# scale = px.colors.make_colorscale(colors=[0,1], scale=[[0.0, 'rgb(0,0,255)'], [1.0, 'rgb(255,0,0)']])
# scale.show()


#swatches = px.colors.sequential.Purples()
#	template=color_template)
	# template=[[0.0, "rgb(165,0,38)"],
 #                [0.1111111111111111, "rgb(215,48,39)"],
 #                [0.2222222222222222, "rgb(244,109,67)"],
 #                [0.3333333333333333, "rgb(253,174,97)"],
 #                [0.4444444444444444, "rgb(254,224,144)"],
 #                [0.5555555555555556, "rgb(224,243,248)"],
 #                [0.6666666666666666, "rgb(171,217,233)"],
 #                [0.7777777777777778, "rgb(116,173,209)"],
 #                [0.8888888888888888, "rgb(69,117,180)"],
 #                [1.0, "rgb(49,54,149)"]]
                
# swatches.show()
# if __name__ == '__main__':
#     app.run_server(debug=True)