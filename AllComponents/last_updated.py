import datetime
import dash
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






