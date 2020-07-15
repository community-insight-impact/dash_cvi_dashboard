import dash
import dash_html_components as html
import pandas as pd
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import json
import flask
import glob
import os
import time

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'header': 'c0c0c0',
    'text': '#7FDBFF',
    'lavender': '#E6E6FA',
    "pink": '#FFC0CB',
    "gray": "#696969"
}

merged = pd.read_csv("../../../Downloads/covid_community_vulnerability-master/data/severe_cases_score_data.csv")
criteria = ['Severe COVID Case Complications', 'Risk of Severe Economic Harm', 'Need for Mobile Health Resources']


data = pd.read_csv("../../../Downloads/covid_community_vulnerability-master/data/severe_cases_score_data.csv", dtype={'FIPS': str})
data_str = data.applymap(str)
data2 = pd.read_csv("../../../Downloads/covid_community_vulnerability-master/data/economic_score_data.csv", dtype={'FIPS': str})
data3 = pd.read_csv("../../../Downloads/covid_community_vulnerability-master/data/mobile_health_score_data.csv", dtype={'FIPS': str})

side_data = data.merge(data2, how='outer').merge(data3, how='outer')

dropped = [
 'Years of Potential Life Lost Rate',
 '% Fair or Poor Health',
 '% Smokers',
 '% Adults with Obesity',
 'Primary Care Physicians Rate',
 'High School Graduation Rate',
 '% Unemployed',
 '% Children in Poverty',
 'Income Ratio',
 '% Single-Parent Households',
 '% Severe Housing Problems',
 '% Adults with Diabetes',
 '% Uninsured',
 '% Severe Housing Cost Burden',
 '% 65 and over',
 'covid_cases',
 'covid_deaths',
 'internet_percent']

full_datasets25 = {}
full_datasets50 = {}

#merged.drop(columns=dropped)
for i in range(3):
    merged_f=side_data[['County','State', criteria[i]]]
    sorted_cases = merged_f.sort_values(by=[criteria[i]], ascending= False)
    top_25 = sorted_cases.head(25)
    #top_50 = sorted_cases.head(50)
    full_datasets25[criteria[i]]= top_25

    #print(top_25)

#print(full_datasets25[criteria[0]])
#print(full_datasets25[criteria[1]])
#print(full_datasets25[criteria[2]])
#print(type(full_datasets25[criteria[0]][full_datasets25[criteria[0]]['County']=='Putnam']['Severe COVID Case Complications']))

def generate_table(ind, 
    #score, states ,
    max_rows=26):
    table_name = criteria[ind]
    dataframe = full_datasets25[table_name]
    return html.Table(
        # Header
        #[html.Tr([table_name])] +
        # Body
        [html.Tr([
            html.Td("{}".format(dataframe.iloc[i]['County']) + ", " + "{}".format(dataframe.iloc[i]['State']) + " = "+ str(round(dataframe.iloc[i][table_name], 2))
            )]) #for col in dataframe.columns
         for i in range(min(len(dataframe), max_rows))
        ]#, style= {'display': 'None'}
    )


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    dcc.Store(id= 'index', data=[0,1,2]),
    html.Button(id='prev', children='Previous'),
    html.Button(id='next', children= 'Next'),
    html.Div(id= "whole-table", children =[
        #html.H4(children='County Score: Severe COVID Case Complications'),
        #generate_table(full_datasets25[criteria[0]])
        ])
])

@app.callback(
    Output('index', 'data'),
    [Input('prev', 'n_clicks'),
    Input('next', 'n_clicks')], [State('index', 'data')])

def click_button(previous, next, score_lst):
    ctx = dash.callback_context
    if not ctx.triggered:
        return score_lst
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        print(button_id)
        if button_id == "prev":
            prev = score_lst.pop(-1)
            score_lst.insert(0, prev)
            return score_lst
        if button_id == 'next':
            nex = score_lst.pop(0)
            score_lst.append(nex)
            return score_lst

@app.callback(Output('whole-table', 'children'), 
     [Input('index', 'data')])

def display(score_i):
    #time.sleep(3)
    indx = score_i[0]
    return [
        html.H4(children=str('County Score: ' + criteria[indx])),
        generate_table(indx)
        ]



if __name__ == '__main__':
    app.run_server(debug=True)
