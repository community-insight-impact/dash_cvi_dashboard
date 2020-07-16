import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
from dash.exceptions import PreventUpdate


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
	html.P('Describes likelihood that constituents within a community will develop severe complications following covid-19 infection', style = {'margin-bottom': 50}),
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
	html.P('Describes existing need for food-based community efforts, services, and nonprofits', style={'margin-bottom': 50}),
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
	html.P('describes the likelihood that a community could benefit from mobile health services', style={'margin-bottom': 50}),
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

def make_item(i):
    # we use this function to make the example items to avoid code duplication
    return dbc.Card(
        [
            dbc.CardHeader(
                html.Div(
                  html.H2(
                   dbc.Button(
                    	criteria[i], 
                    	#children= criteria[i],
                    	 #**{'aria-hidden': 'true'},
                        color="link",
                        id=f"score-{i}-toggle", #style={'font-size':2},
                    )
                   )
                )
            )
    ,
            dbc.Collapse(
                dbc.CardBody(graph_info[i]),
                id=f"collapse-{i}",
            )
        ]
    )


accordion = html.Div([make_item(0), make_item(1), make_item(2)], className="accordion")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://codepen.io/chriddyp/pen/bWLwgP.css', 'https://kit.fontawesome.com/14b16196e0.js'])

app.layout = html.Div([
	html.Div(dbc.Row(dbc.Col(accordion, width=3), justify='end'))])

@app.callback(
	[Output(f"collapse-{i}", "is_open") for i in range(3)],
	[Input(f"score-{i}-toggle", "n_clicks") for i in range(3)],
	[State(f"collapse-{i}", "is_open") for i in range(3)])

def toggle_accordion(n1, n2, n3, is_open1, is_open2, is_open3):
	ctx = dash.callback_context
	if not ctx.triggered:
		return False, False, False
	else:
		button_id = ctx.triggered[0]["prop_id"].split(".")[0]
		if button_id == "score-0-toggle" and n1:
			return not is_open1, False, False
		elif button_id == "score-1-toggle" and n2:
			return False, not is_open2, False
		elif button_id == "score-2-toggle" and n3:
			return False, False, not is_open3
		


if __name__ == '__main__':
    app.run_server(debug=True)





