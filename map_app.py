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
from dash.dependencies import Input, Output, State
import flask
import glob
import os
import dash_bootstrap_components as dbc
import datetime
from dash.exceptions import PreventUpdate

picture_dir="/pictures"


data = pd.read_csv("../severe_cases_score_data.csv", dtype={'FIPS': str})
data_str = data.applymap(str)
data2 = pd.read_csv("../economic_score_data.csv", dtype={'FIPS': str})
data3 = pd.read_csv("../mobile_health_score_data.csv", dtype={'FIPS': str})




full_data = data.merge(data2, how='outer').merge(data3, how='outer')

full_data_str = full_data.applymap(str)
criteria = ['Severe COVID Case Complications', 'Risk of Severe Economic Harm', 'Need for Mobile Health Resources']
full_datasets50 = {}

for i in range(3):
    merged_f=full_data[['County','State', criteria[i]]]
    sorted_cases = merged_f.sort_values(by=[criteria[i]], ascending= False)
    top_50 = sorted_cases.head(50)
    #top_50 = sorted_cases.head(50)
    full_datasets50[criteria[i]]= top_50

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]

indicators_lst = ['Severe COVID Case Complications',
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
]

all_states = list(full_data.State.unique())
all_states.insert(0, "United States")

all_counties = []
big_i = data.shape[0]
for each_i in range(big_i):
    cty= str(data.iloc[each_i]['County'] + ", " + data.iloc[each_i]['State'])
    all_counties.append(cty)
#print(all_counties)

data['County + State'] = all_counties
print(data['County + State'])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


colors_map = {'Severe COVID Case Complications': ['#fdc1f6', '#ff385e'], 'covid_cases': ['#bdb4fe', '#0d0c54'],
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



colors_chart = {
    'header': 'c0c0c0',
    'text': '#7FDBFF',
    'lavender': '#E6E6FA',
    "pink": '#FFC0CB',
    "gray": "#696969"
}

sidebar_data = ['Severe COVID Case Complications', 'Risk of Severe Economic Harm', 'Need for Mobile Health Resources']

merged = pd.read_csv("../../../Downloads/covid_community_vulnerability-master/data/merged_data.csv")



dropped = ['Severe COVID Case Complications',
'Years of Potential Life Lost Rate', '% Fair or Poor Health','% Smokers',
'% Adults with Obesity','% 65 and over','% Adults with Diabetes']


top_10_data = data.drop(columns=dropped)
#print(merged.head(5))
sorted_cases = top_10_data.sort_values(by='covid_cases', ascending= False)
top_10data = sorted_cases.head(10)
top_10 = top_10data.applymap(str)

dff2 = pd.DataFrame(columns=full_data.columns)
cty_df = data[data['County + State'] == 'Bibb, Alabama']
dff2 = pd.concat([dff2, cty_df], join='outer')
print(dff2)


data_lst = ['County', 'State'] + indicators_lst
data['all_data'] =  full_data['FIPS'] + "<br>" + "County= " + data['County'] + "<br>" + "State= " + data['State'] #+'<br>' + data['Severe COVID Case Complications']+'<br>' + data['covid_cases']



for indicator in indicators_lst:
	data['all_data'] = data['all_data'] + "<br>" + indicator +"= " + data_str[indicator]


top_10["covid"] = top_10.loc[:,'FIPS'] + "<br>" + "County= " + top_10.loc[:,'County'] + "<br>" + "State= " + top_10.loc[:, 'State'] + "<br>"+ "Number of Covid cases=" + top_10.loc[:, 'covid_cases']
#hovertemplate =  "FIPS=%{data.FIPS}<br>County=%%{data.County}<br>State=%%{data.State}<extra></extra>"

def format_time():
    t = datetime.datetime.now()
    s = t.strftime('%Y-%m-%d %H:%M:%S.%f')
    return s[:-7]


empty_fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=data.FIPS))
empty_fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=3.5, mapbox_center = {"lat": 37.0902, "lon": -95.7129}, showlegend=False, margin={"r":0,"t":0,"l":0,"b":0}, height=None)


all_indicators = {'Number of COVID cases': 'covid_cases', '% 65 and older': '% 65 and over', 
'% Adults with Obesity': '% Adults with Obesity', '% Adults with Diabetes': '% Adults with Diabetes',
'% Smokers': '% Smokers', }

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
	dcc.Checklist(id="economic-indicators", options=[ #{'label': 'Number of COVID cases', 'value': 'covid_cases'},
        #{'label': 'Risk of Severe Economic Harm', 'value': 'Risk of Severe Economic Harm'},
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

accordion_text_colors = ['#ff385e', '#0c3f47', '#ffc05f']

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
                        html.I(id=f"score-{i}-toggle", className="fa fa-caret-right", **{'aria-hidden': 'true'}, style= {'fontSize': '15px', 'display':'inline-block', 'position': 'relative', 'float':'right', 'marginTop':'-23px'  #'right': 5  #'bottom': 5 #right':30, 'bottom': 0
                    	})],
                  style= {'verticalAlign':'middle', }), 
     #),
            style={'height':'30%'}),
            dbc.Collapse(
                dbc.CardBody(graph_info[i]),
                id=f"collapse-{i}",
            )
        ],
        #, style={'height': 60}
    )

accordion = html.Div([make_item(0), make_item(1), make_item(2)], className="accordion")

accordion_box = html.Div([
	html.Label('Select a Metric:', style={'verticalAlign':'middle', 'padding': 10}), 
	html.Div(accordion, style = {'width': '100%', 'overflowY':'scroll'})], #style = {'width': '20%', 'overflowY':'scroll',}
		style={'height':'400px', 'width':'100%', 'overflowY':'scroll', 'border': '5px solid gray', 'margin': 5})#,'overflowY':'hidden'})


		#[dbc.Row('Select a Metric', no_gutters=True), dbc.Row(dbc.Col(accordion, width=3), justify='end')])])


#fig = px.choropleth_mapbox(data, geojson=counties, locations = data.FIPS)

choose_filters = html.Div([
        html.Div([
            html.Label('Filter by State'),
            dcc.Dropdown(
                id = 'choose-state',
                options= [{'label': state, 'value': state} for state in all_states],
                value= 'United States'
        )
    ],
    style={'width': '50%', 'display': 'inline-block'}),

        html.Div([
            html.Label('Filter by County'),
            dcc.Dropdown(
                id='choose-county',
                options=[{'label': i, 'value': i} for i in all_counties],
                value=[],
                multi = True,
                placeholder= "Search..."
            )
    ],
    style={'width': '50%', 'display': 'inline-block'})
    ], 
    style={'height': '10%', 'display': 'flex', 'zIndex':-1}
    )



nav_bar = html.Div(
    [
    html.Div(className='navbar', 
        children=[
            html.Img(src='https://raw.githubusercontent.com/community-insight-impact/covid_community_vulnerability/master/CVI%20Logo%20FINAL%20ONE%20smaller.png',
        style={'height':'28px','margin':8}), #html.A("COVID-19 Community Vulnerability Index"), 
            html.H2("COVID-19 Community Vulnerability Index  ", style={'font-size':18,'margin-top':14, 'vertical-align': 'middle', 'color': 'white'}),
            html.Div(className='dropdown', 
            children=[html.Button(className='dropbtn', children= html.Span(children=[html.P('Menu ',  style = {'display':'inline-block'}) ,#style={'margin-bottom': -10}),
                html.I(className="fa fa-caret-down", **{'aria-hidden': 'true'}, style = {'display':'inline-block', 'marginTop': '10px', 'marginLeft':'5px'})], style = {'display':'flex'})), 
                    html. Div(className='dropdown-content', children=
                        [html.A('About', href='https://github.com/community-insight-impact/covid_community_vulnerability', target="_blank"), 
                        html.A('Dataset', href='https://github.com/community-insight-impact/covid_community_vulnerability/blob/master/data/full_dataset.md', target="_blank"),
                        html.A('Methodology', href='https://github.com/community-insight-impact/covid_community_vulnerability/blob/master/documentation/methodology.md', target="_blank")])#, style = {'display':'inline-block'})
            ], style={'zIndex': 10}),
        ], style={'display':'flex', 'zIndex': 1}),#, html.Div('hi, testing', style={'color':'black', 'margin-top':10})
        #choose_filters
        ]) #style={'zIndex': 1})#choose_filters])

indicators_shown = html.Div(children= [html.P(children="Indicators shown:"), html.Div(id='indicators-shown', children= [])], style= {'height':'20%',"overflowY": 'scroll'})

map_plus_sidebox = html.Div(id = 'map plus legends', children=
	[html.Div(dcc.Graph(id='counties-map', figure= empty_fig),
   				style= {'width': "80%", 'height':'100%', 'display':'inline-block'}),
   	
    html.Div(children=[accordion_box, indicators_shown], style = {'width': '20%'})],
   			style= {'width':'100%', 'height':'500px', 'display':'flex', 'zIndex': -2})

last_updated_indicator = html.Div(children =[html.Label("Last Updated:"), html.Div(id='show-time')], style = {#'border': '5px solid gray',
	'display':'inline-block','height':'10%', 'background-color':'gray', 'width':'20%'}) #'margin-right': '50px'})

bar_chart = html.Div(children=[
	html.H1(children='Confirmed Cases by County',
		style= {
		"textAlign": 'left',
		"color": colors_chart["gray"],
		"font": "Open Sans",  'font-size': 25, 'margin-top': 0, 'margin-bottom':0
		}),
	dcc.Graph(
		id='example-graph',
		figure={
		'data' : [
		{'x': list(top_10.County), 
		'y': list(top_10.covid_cases), 
		'text': list(top_10["covid"]), 
		'type': 'bar', 'name': 'Cases', 'marker': {'color': colors_chart["header"]}
		}],
		'layout': {
		"plot_bgcolor": colors_chart["gray"],
		"paper_bgcolor": colors_chart["header"],
		'color': colors_chart["text"],
		'font': {
		'color': colors_chart['gray']
		},
                #'width': "50%",
                #'height': '30%',
                'margin': {'t':0,'l':30, 'r':0, 'b':30 }
                #'margin':{'t':0, 'b':0 }
                }
                }
                , style= {'height': 230, 'width': "80%", 'margin-top': 0, 'float':'left', 'display':'inline-block'}
                )], style = {'display':'grid', 'width': "80%"}) #style= {'height': 230,'width': "80%", 'margin-top': 0, 'float':'left', 'display':'inline-block'}],)


side_chart = html.Div(children=[
    		dcc.Store(id= 'index-score', data=[0,1,2]),
    		dcc.Store(id= 'index-county', data = 0),
   		 	html.Div([
        	html.I(id='prev-county', className="fa fa-caret-left", **{'aria-hidden': 'true'}, style = {'display':'inline-block', 'font-size': '20px', 'margin-right': '10px'}),
        	html.P(id= 'count-county' ,#children='1 of 50',
         style= {'display':'inline-block', 'textOverflow':'ellipsis'}),
        	html.I(id='next-county', className= "fa fa-caret-right", **{'aria-hidden': 'true'}, style={'display':'inline-block', 'font-size': '20px', 'margin-left': '10px'})
        ], style= {'textAlign': 'center', 'position':'static'}),
    		html.Div(id= "chart_num", children =[]
        #html.H4(children='County Score: Severe COVID Case Complications'),
        #generate_table(full_datasets25[criteria[0]])
        , style = {'position':'static','display':'grid'}),
    		html.Div(id= "choose_score", children = [
        	   html.I(id='prev-score', className="fa fa-caret-left", **{'aria-hidden': 'true'}, style = {'display':'inline-block', 'fontSize': '20px','margin-right': '10px'}),
        	   html.P(id= 'count-score', #children='Severe COVID Case Complications'
                    style= {'textAlign':'center', 'display':'inline-block', 'font-size': '12px', 'textOverflow':'ellipsis'}), #style = {'width': 150, 'position':'static', 'textOverflow':'ellipsis'}, 
       		   html.I(id='next-score', className="fa fa-caret-right", **{'aria-hidden': 'true'}, style={'display':'inline-block', 'fontSize': '20px', 'margin-left': '10px',
           })
        	   ],style={'textAlign': 'center', 'position':'static', 'display':'flex', 'marginTop':'20px'})#'display':'flex', 'margin-top':55,'margin-left':30, 'position':'static'}) #'position':'static', 'text-align':'center'})
			],
    style = {
            #'label':'no legend',
            'width':'20%', 'maxHeight':330, #'maxHeight':400, 
            #'overflowY': 'scroll', 
            #'margin-left': 10,
            'overflow':'scroll',
            'border': '10px solid gray', #'margin': 10,
            'display': 'grid', 
            'position':'static', 
            'padding':10
            })

horizontal_charts = html.Div(children= [bar_chart, side_chart], style={'display': 'flex'})


sidebar_header = dbc.Row(
    [dbc.Col(html.H2("Introduction", className="display-4", style = {'font-size':40})),
        dbc.Col(
            [html.Div(
                    # styled into an 'introduction' pull-out tab
                    html.Span(className="navbar-toggler-icon", children="Introduction"),
                    className="navbar-toggler",
                    id="sidebar-toggle"
                ),
            ],
          
            width=3,
            # vertically align the toggle in the center
            align="center",
        ),
    ]
)

sidebar = html.Div(
    [
        sidebar_header,
        html.Div(
            [
                html.Hr(),
                html.P(
                    'How to Use the COVID-19 Community Vulnerability Index',
                    className="lead",
                ),
            ],
            id="blurb", #temporary name
        ),
        #use the Collapse component to animate hiding / revealing introduction
        dbc.Collapse(
            dbc.Card(dbc.CardBody('How to Use the COVID-19 Community Vulnerability Index')),
            id="collapse", 
        ),
    ],
    id="sidebar",
)

content = html.Div(id = 'page-content', children= [
    html.P('Last Updated'),
    html.Div(id='show-time', children = '08/23/2020'),
    ], style={'border': '5px solid gray'})

instruction_pullouttab= html.Div([sidebar], style = {'zIndex':1000})





#charts_plus_time = html.Div(children= [horizontal_charts], style = {'display':'grid'})


app = dash.Dash(__name__, external_stylesheets= [dbc.themes.BOOTSTRAP, 
	'https://codepen.io/chriddyp/pen/bWLwgP.css'], 
	meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])
#app.layout = 					#html.Div([html.Meta(name='viewport', content="width=device-width, height=device-height, initial-scale=1.0"), 
app.layout = html.Div(children=[
	#nav_bar,
	nav_bar,
   
	choose_filters,
	map_plus_sidebox,
	horizontal_charts,
	last_updated_indicator,

    instruction_pullouttab,
    dcc.Store(id='chosen-indicators', data=[]),

    dcc.Store(id= 'chosen-data', data= [])
    ],
        
    #dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0),

    style={'height':'100%', 'width': '100%',}) #'overflow':'hidden'})# 'margin':{"r":0,"t":20,"l":0,"b":0}})
#])
	
@app.callback(
    Output('choose-county', 'options'),
    #Output('show-time', 'children')],
    [Input('choose-state', 'value')])

def change_cty_options(state):
    if state == "United States":
        return [{'label': i, 'value': i} for i in all_counties]
    else:
        dff= data[data['State']== state]
        return [{'label': str(dff.iloc[i]['County + State']), 'value' : str(dff.iloc[i]['County + State'])}  for i in range(dff.shape[0])]
        

@app.callback(
    Output('chosen-data','data'),
    [Input('choose-state','value'), 
    Input('choose-county', 'value')])

def define_data(state, counties):
    if state == "United States":
        if len(counties) == 0:
            return data.to_dict('list') 
        elif len(counties) != 0:
            dff = pd.DataFrame(columns=data.columns)
            for cty in counties:
                cty_df = data[data['County + State'] == cty]
                dff = pd.concat([dff, cty_df], join='outer')
            return dff.to_dict('list')
    else:
        if len(counties) == 0:
            return data[data['State']==state].to_dict('list')
        elif len(counties) != 0:
            dff2 = pd.DataFrame(columns=data.columns)
            for cty in counties:
                cty_df = data[data['County + State'] == cty]
                dff2 = pd.concat([dff2, cty_df], join='outer')
            return dff2.to_dict('list')

@app.callback(
    [Output('indicators-shown', 'children'), 
    Output('chosen-indicators', 'data')],
    [Input(f'checkbox-{i}', 'value') for i in range(3)]+
    [Input("severe-indicators", 'value')])

def show_indicators(score1, score2, score3, metrics):
	scores = score1 + score2 + score3 + metrics
	return " | ".join(score for score in scores if score), scores


@app.callback(
	Output('counties-map', 'figure'),
	#Output('show-time', 'children')],
	[Input('chosen-data', 'data'), 
   	Input('chosen-indicators', 'data')])

def update_map(chosen_data, chosen_indicator):
	#if chosen_state != None:
	#if chosen_state == "United States":
	if len(chosen_indicator) != 0:
			#if chosen_state == "United States":
		fig = px.choropleth_mapbox(chosen_data, 
			geojson=counties, locations=chosen_data['FIPS'], 
			color=chosen_indicator[0],
			color_continuous_scale=colors_map[chosen_indicator[0]],
			range_color=index_range[chosen_indicator[0]],
			mapbox_style="carto-positron",				
			zoom=3.5, center = {"lat": 37.0902, "lon": -95.7129},
			opacity=0.8,
			labels={chosen_indicator[0]}, hover_data= ['County', 'State'] + indicators_lst,
			)
		fig.update_layout(coloraxis_showscale=False, title_text = chosen_indicator[0], margin={"r":0,"t":0,"l":0,"b":0})
		#fig.update_layout(title_text = chosen_indicator[0], margin={"r":0,"t":0,"l":0,"b":0})
		if len(chosen_indicator) > 1:
			for val_indx in range(1, len(chosen_indicator)):
				fig.add_trace(go.Choroplethmapbox(name = chosen_indicator[val_indx], geojson=counties, locations=chosen_data['FIPS'], z=chosen_data[chosen_indicator[val_indx]],
						colorscale=colors_map[chosen_indicator[val_indx]],
						zmin=index_range[chosen_indicator[val_indx]][0],
						zmax=index_range[chosen_indicator[val_indx]][1],
						marker_line_width=0.1, marker_opacity=0.8, showscale=False, #hovertemplate =  "FIPS=%{data.FIPS}<br>County=%%{data.County}<br>State=%%{data.State}<extra></extra>"))
						text= chosen_data['all_data'], hovertemplate = 'FIPS= %{text} <extra></extra>'))#, hovertemplate= data_lst ))#, hovertext=[data[y] for y in indicators_lst]))
						#hovertemplate=[County: %{data['County']}, State:%{data['State']}] + [y: %{data[y]} for y in indicators_lst]))
				fig.update_layout(title_text = chosen_indicator[0], margin={"r":0,"t":0,"l":0,"b":0})
					#fig.update_layout(hover_data= ['County', 'State'] + indicators_lst)
	else:
		fig = empty_fig#go.Figure(go.Choroplethmapbox(geojson=counties, locations=data.FIPS))
		 	#fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=3.5, mapbox_center = {"lat": 37.0902, "lon": -95.7129}, showlegend=False)
		#fig.update_trace(hover_data= ['County', 'State'] + indicators_lst)
		#geojson=counties, locations=data.FIPS, hover_data= ['County', 'State'] + indicators_lst))
	return fig
	


#********SCORE CHART CALLBACK********
@app.callback(
    Output('index-score', 'data'),
    [Input('prev-score', 'n_clicks'),
    Input('next-score', 'n_clicks')], [State('index-score', 'data')])

def click_button(previous, next, score_lst):
    ctx = dash.callback_context
    if not ctx.triggered:
        return score_lst#, criteria[score_lst[0]]
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        print(button_id)
        if button_id == "prev-score":
            prev = score_lst.pop(-1)
            score_lst.insert(0, prev)
            return score_lst#, criteria[score_lst[0]]
        if button_id == 'next-score':
            nex = score_lst.pop(0)
            score_lst.append(nex)
            return score_lst#, criteria[score_lst[0]]

@app.callback(
    Output('index-county', 'data'),
    #Output('count-county', 'children')],
    [Input('prev-county', 'n_clicks'), 
    Input('next-county', 'n_clicks')],
    [State('index-county', 'data')])

def click_county(prev, next, num):
    ctx = dash.callback_context
    if not ctx.triggered:
        return num#, '{} of 50'.format(num) 
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'prev-county':
            if num == 0:
                num = 49
            else:
                num = num -1
            #return num
        if button_id == 'next-county':
            if num == 49:
                num = 0
            else:
                num = num +1
        return num#, '{} of 50'.format(num)        


@app.callback([Output('chart_num', 'children'), 
    Output('count-score','children'),
    Output('count-county', 'children')], 
    [Input('index-county', 'data'),
    Input('index-score', 'data')])

def chart_display(county_i, score_i):
    #time.sleep(3)
    cty_indx = county_i
    score_indx = score_i[0]
    score = criteria[score_indx]
    df = full_datasets50[score]
    
    return [
        html.Div(html.H4(children=score, style={'textAlign':'center','fontSize':20, 'marginBottom':20, 'position':'static', 'textOverflow':'ellipsis', 'overflow':'hidden'})),
        html.H4('County Score',style={'textAlign':'center', 'fontSize': 20, 'marginBottom': 5, 'position':'static'}),
        html.H4(str(round(df.iloc[cty_indx][score],2)), style= { 'fontWeight': 'bold', 'textAlign':'center', 'marginBottom': 5}),
        html.H5(children= str(df.iloc[cty_indx]['County'] + ", " + df.iloc[cty_indx]['State']), style = {'textAlign':'center', 'fontSize': 20, 'position':'static'})#'margin-bottom': 50,
        ], criteria[score_indx], ' {} of 50 '.format(cty_indx + 1)

		
@app.callback(
	[Output(f"collapse-{i}", "is_open")for i in range(3)],
    #+[Output(f"score-{i}-toggle", "className") for i in range(3)], #+ [Output(f"checkbox-{i}", "className") for i in range(3)] + [Output(f"arrow-{i}", "className") for i in range(3)] ,
	[Input(f"score-{i}-toggle", "n_clicks") for i in range(3)],
	[State(f"collapse-{i}", "is_open") for i in range(3)])

def toggle_accordion(n1, n2, n3, is_open1, is_open2, is_open3):
	ctx = dash.callback_context
	if not ctx.triggered:
		return is_open1, is_open2, is_open3 #,caret_list[is_open1], caret_list[is_open2], caret_list[is_open3])  
	else:
		button_id = ctx.triggered[0]["prop_id"].split(".")[0]
		if button_id == "score-0-toggle" and n1:
			#print(n1)
			return not is_open1, is_open2, is_open3 #caret_list[not is_open1], caret_list[is_open2], caret_list[is_open3])
		elif button_id == "score-1-toggle" and n2:
			return is_open1, not is_open2, is_open3 #caret_list[is_open1], caret_list[not is_open2], caret_list[is_open3])
		elif button_id == "score-2-toggle" and n3:
			return is_open1, is_open2, not is_open3#, caret_list[is_open1], caret_list[is_open2], caret_list[ not is_open3])


@app.callback(
    #list([Output(f"checkbox-{i}", "className")for i in range(3)] + 
    Output("score-0-toggle", "className"), #+ [Output(f"checkbox-{i}", "className") for i in range(3)] + [Output(f"arrow-{i}", "className") for i in range(3)] ,
    [Input("score-0-toggle", "n_clicks")],
    [State("collapse-0", "is_open")])

def change_icon(n0, is_open0): 
    # if is_open0 == 'collapse':
    #     return "fa fa-caret-right"
    caret_list = {True: "fa fa-caret-down", False: "fa fa-caret-right"}
    if n0 == None:
        return "fa fa-caret-right"
    elif n0 == 1:
        return "fa fa-caret-down"
    elif n0 and is_open0 == True:
        return "fa fa-caret-right"
    elif n0 and is_open0 == False:
        return "fa fa-caret-down"


@app.callback(
    #list([Output(f"checkbox-{i}", "className")for i in range(3)] + 
    Output("score-1-toggle", "className"), #+ [Output(f"checkbox-{i}", "className") for i in range(3)] + [Output(f"arrow-{i}", "className") for i in range(3)] ,
    [Input("score-1-toggle", "n_clicks")],
    [State("collapse-1", "is_open")])

def change_icon(n0, is_open0): 
    # if is_open0 == 'collapse':
    #     return "fa fa-caret-right"
    caret_list = {True: "fa fa-caret-down", False: "fa fa-caret-right"}
    if n0 == None:
        return "fa fa-caret-right"
    elif n0 == 1:
        return "fa fa-caret-down"
    elif n0 and is_open0 == True:
        return "fa fa-caret-right"
    elif n0 and is_open0 == False:
        return "fa fa-caret-down"
    
@app.callback(
    #list([Output(f"checkbox-{i}", "className")for i in range(3)] + 
    Output("score-2-toggle", "className"), #+ [Output(f"checkbox-{i}", "className") for i in range(3)] + [Output(f"arrow-{i}", "className") for i in range(3)] ,
    [Input("score-2-toggle", "n_clicks")],
    [State("collapse-2", "is_open")])

def change_icon(n0, is_open0): 
    # if is_open0 == 'collapse':
    #     return "fa fa-caret-right"
    caret_list = {True: "fa fa-caret-down", False: "fa fa-caret-right"}
    if n0 == None:
        return "fa fa-caret-right"
    elif n0 == 1:
        return "fa fa-caret-down"
    elif n0 and is_open0 == True:
        return "fa fa-caret-right"
    elif n0 and is_open0 == False:
        return "fa fa-caret-down"

   
@app.callback(
    Output("sidebar", "className"),
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar", "className")])
def toggle_classname(n, classname):
    if n and classname == "":
        return "collapsed"
    return ""



if __name__ == '__main__':
	app.run_server(debug=True)




