import datetime
#from write_csv# import read_county, read_nyc
#import write_csv
import dash
# import merge_clean_data
# import resources_targeting_indices
#import write_csv
#import merge_clean_data
#import resources_targeting_indices
#import make_gis_layers
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

timenow = datetime.datetime.now()


#print(timenow)



def format_time():
    t = datetime.datetime.now()
    s = t.strftime('%Y-%m-%d %H:%M:%S.%f')
    return s[:-7]

#print(format_time())

last_updated_indicator = html.Div(children =[html.Label("Last Updated:"), html.Div(id='show-time')], style = {#'border': '5px solid gray',
    'display':'inline-block','height':'10%', 'background-color':'gray', 'width':'20%'})

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app.layout = 

# @app.callback(
# 	[Output('county-data', 'data'),
# 	Output('nyc-data', 'data')],
# 	[Input('interval-component', 'n_intervals')])

# def update_csv(n):
# 	ct_data = write_csv.read_county()
# 	nyc_data = write_csv.read_nyc()
# 	return 0

#help(dcc.Store)

# @app.callback(
# 	Output('all-scores', 'data'),	
# 	[Input('interval-component', 'n_intervals')])

# def update_scores_file(n):
# 	resources_targeting_indices.calculate_indices()
# 	severe = make_gis_layers.make_severe_score()
# 	mobile = make_gis_layers.make_mobile_score()
# 	economic = make_gis_layers.make_economic_score(), 
# 	return [severe, economic, mobile]

# @app.callback(Output('show-time','children'), 
# 	[Input('interval-component','n_intervals')])

# def update_time(n):
# 	return 'done'

# if __name__ == '__main__':
# 	app.run_server(debug=True)





