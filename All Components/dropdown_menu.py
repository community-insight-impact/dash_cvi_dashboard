import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
from dash.exceptions import PreventUpdate
import json

indicators_lst = ['Severe COVID Case Complications',
'covid_cases',
'Years of Potential Life Lost Rate',
'% Fair or Poor Health',
'% Smokers',
'% Adults with Obesity',
'% Adults with Diabetes',
'% 65 and over']

criteria = ['Severe COVID Case Complications', 'Risk of Severe Economic Harm', 'Need for Mobile Health Resources']


item0 = html.Div([
	html.P('Describes likelihood that constituents within a community will develop severe complications following covid-19 infection', style = {'margin-bottom': 20}),
	html.P('Includes:'),
	html.P('Number of COVID cases'),
	html.P('% 65 and older'),
	html.P('% Adults with Obesity'),
	html.P('% Adults with Diabetes'),
	html.P('% Smokers'),
	html.P('Years of Potential Life Lost Rate'),
	html.P('% Fair or Poor Health')]
	)

item1 = html.Div([
	html.P('Describes existing need for food-based community efforts, services, and nonprofits', style={'margin-bottom': 20}),
	html.P('Includes:'),
	html.P('% Unemployed'),
	html.P('% Children in Poverty'),
	html.P('Income Ratio'),
	html.P('% Single-Parent Households'),
	html.P('% Severe Housing Problems'),
	html.P('% Enrolled in Free or Reduced Lunch'),
	html.P('% Uninsured'),
	html.P('Number of Covid Cases'),
	html.P('% Severe Housing Cost Burden')
	])

item2 = html.Div([
	html.P('describes the likelihood that a community could benefit from mobile health services', style={'margin-bottom': 20}),
	html.P('% Smokers'),
	html.P('% Uninsured'),
	html.P('% Adults with Obesity'),
	html.P('% Adults with Diabetes'),
	html.P('% 65 and older'),
	html.P('Primary Care Physicians Rate'),
	html.P('% Fair or Poor Health'),
	html.P('% Home Internet Access')
	])

graph_info =[item0, item1, item2]

accordion_text_colors = ['#ff385e', '#0c3f47', '#ffc05f']

def make_item(i):
    # we use this function to make the example items to avoid code duplication
    return dbc.Card(
        [
            dbc.CardHeader(
                html.Div(
                	children=[html.I(id= f"checkbox-{i}",
                    	className="fa fa-square-o", #style = {'font-weight':'bold'}, 
                    	#children= criteria[i],
                    	 **{'aria-hidden': 'true'},
                        #color="link",
                        style={'font-size':'15px', 'font-weight':'bold', 'display': 'inline-block'},
                    ), " ", html.H2(criteria[i], style={'font-size':'15px', 'display': 'inline-block', 'color': accordion_text_colors[i]}),
                    html.I(id=f"score-{i}-toggle", className="fa fa-caret-right", **{'aria-hidden': 'true'}, style= {'font-size': '15px', 'display':'inline-block', 'position': 'relative',
                    	 'float':'right', 'top': 20, #'right': 5  #'bottom': 5 #right':30, 'bottom': 0
                    	 })],
                    #style = {'height': '20px', 'text-align':'center'}#'display':'flex'}
                #style={'margin-top':'1px'}),
                  #style = {'height': '0px', 'text-align':'center'}
     style= {'vertical-align':'middle', 'margin':0}), 
     #),
                style={'height':'30%'}),
            dbc.Collapse(
                dbc.CardBody(graph_info[i]),
                id=f"collapse-{i}",
            )
        ]#, style={'height': 60}
    )

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', '/assets/font-awesome.min.css', dbc.themes.BOOTSTRAP]

accordion = html.Div([make_item(0), make_item(1), make_item(2)], className="accordion")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://codepen.io/chriddyp/pen/bWLwgP.css', '/assets/font-awesome.min.css'])

app.layout = html.Div([
	html.P('Select a Metric:', style={'margin-top': 10, 'margin-left': 10}), html.Div(accordion, style = {'width': '100%', 'overflowY':'scroll'})], #style = {'width': '20%', 'overflowY':'scroll',}
		style={'maxHeight':'400px', 'width':'22%', 'overflowY':'scroll', 'border': '5px solid gray', 'margin': 10})#,'overflowY':'hidden'})


		#[dbc.Row('Select a Metric', no_gutters=True), dbc.Row(dbc.Col(accordion, width=3), justify='end')])])
@app.callback(
	[Output(f"collapse-{i}", "is_open")for i in range(3)], #+ [Output(f"checkbox-{i}", "className") for i in range(3)] + [Output(f"arrow-{i}", "className") for i in range(3)] ,
	[Input(f"score-{i}-toggle", "n_clicks") for i in range(3)],
	[State(f"collapse-{i}", "is_open") for i in range(3)])

def toggle_accordion(n1, n2, n3, is_open1, is_open2, is_open3):
	ctx = dash.callback_context
	if not ctx.triggered:
		return False, False, False
	else:
		button_id = ctx.triggered[0]["prop_id"].split(".")[0]
		if button_id == "score-0-toggle":
			#print(n1)
			return not is_open1, False, False
		elif button_id == "score-1-toggle":
			return False, not is_open2, False
		elif button_id == "score-2-toggle":
			return False, False, not is_open3

@app.callback(
	[Output(f"score-{i}-toggle", "className") for i in range(3)],
 	[Input(f"collapse-{i}", "is_open") for i in range(3)])

def change_icon(is_open1, is_open2, is_open3):
	if is_open1 == True or is_open2 == True or is_open3 == True: 
		if is_open1 == True and is_open2 == False and is_open3 == False:
			return  "fa fa-caret-down", "fa fa-caret-right", "fa fa-caret-right"
		elif is_open2 == True and is_open1 == False and is_open3== False:
			return 'fa fa-caret-right', "fa fa-caret-down", 'fa fa-caret-right'
		elif is_open3 == True and is_open2 == False and is_open1== False:
			return 'fa fa-caret-right', 'fa fa-caret-right', "fa fa-caret-down"
	else:
 		return 'fa fa-caret-right', 'fa fa-caret-right','fa fa-caret-right'


if __name__ == '__main__':
    app.run_server(debug=True)





