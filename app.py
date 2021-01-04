import pandas as pd
pd.set_option('display.max_columns', None)
from urllib.request import urlopen
import plotly.express as px
import plotly.graph_objects as go
import dash
import json
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import flask
# import os
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from AllComponents import sigma_calculation
from AllComponents import choose_filters
from AllComponents import covid_bar_chart
from AllComponents import intro_sidebar
from AllComponents import last_updated
from AllComponents import multimap_plotly
from AllComponents import nav_bar 
from AllComponents import side_chart 
from AllComponents import show_legends
from flask_caching import Cache
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

external_stylesheets = [dbc.themes.BOOTSTRAP, 'https://codepen.io/chriddyp/pen/bWLwgP.css']

    #MERGE ALL DATA INTO 1 DF
data = pd.read_csv("data/severe_cases_score_data.csv", dtype={'FIPS': str})
data_str = data.applymap(str)
data2 = pd.read_csv("data/economic_score_data.csv", dtype={'FIPS': str})
# print(data2)
data3 = pd.read_csv("data/mobile_health_score_data.csv", dtype={'FIPS': str})


full_data = data.merge(data2, how='outer', left_on = ["FIPS", "State", "County"], right_on =["FIPS", "State", "County"] )
full_data = full_data.merge(data3,how= 'outer', left_on = ["FIPS", "State", "County", "% Adults 65 and Older"], right_on = ["FIPS", "State", "County", "% Adults 65 and Older"])
full_data.round(2)

#Add county +state name
all_counties = []
big_i = full_data.shape[0]
for each_i in range(big_i):
    if str(full_data.iloc[each_i]['County']) != 'nan':
        cty= str(full_data.iloc[each_i]['County'] + ", " + full_data.iloc[each_i]['State'])
        all_counties.append(cty)
    else:
        all_counties.append('nan, nan')
full_data['County + State'] = all_counties

full_data_str = full_data.applymap(str)

#SCORES
criteria = ['Severe COVID Case Complications', 'Risk of Severe Economic Harm', 'Need for Mobile Health Resources']

#FOR SIDE CHART
indicators_lst = [
'Severe COVID Case Complications', #0
 'covid_cases',
 'Hypertension Death Rate',
'% Smokers',
'% Adults with Obesity',
'% Diagnosed Diabetes', #5
'% disabled',
'% Adults 65 and Older',
'% Uninsured',
'% Children in Poverty', 
'Income Ratio', #10
'% Single-Parent Households',
'% Fair or Poor Health',
'% Severe Housing Problems',
'% Enrolled in Free or Reduced Lunch',
'% Unemployed', #15
'High School Graduation Rate',
'Primary Care Physicians Rate',
'Heart Disease Death Rate',
'Risk of Severe Economic Harm', #19 
'Need for Mobile Health Resources', #20
'% Severe Housing Cost Burden',
'% Rural',
'% households wo car',
'% workers commuting by public transit',
'% Without Health Insurance', #25
'% Nonwhite',
'% Limited English Proficiency',
'% Veterans in Civilian Adult Population',
'% Fair or Poor Health',
'opioid death rate', #30
'Number of Hospitals'

]

index_range = {}
for indicator in indicators_lst:
    if indicator == 'Income Ratio' or indicator == '% Adults 65 and Older' or indicator == '% Unemployed':
        index_range[indicator] = sigma_calculation.calculate_range(full_data, indicator, 2)
    else:
        index_range[indicator] = sigma_calculation.calculate_range(full_data, indicator,2)

#FOR HOVERBOARD
data_lst = ['County', 'State'] + indicators_lst
full_data['all_data'] =  full_data['FIPS'] + "<br>" + "County= " + full_data['County'] + "<br>" + "State= " + full_data['State'] 
for indicator in indicators_lst:
    full_data['all_data'] = full_data['all_data'] + "<br>" + indicator +"= " + full_data_str[indicator]


app = dash.Dash(__name__, external_stylesheets= external_stylesheets, 
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

server = app.server

#LAYOUT
horizontal_charts = html.Div(children= [covid_bar_chart.bar_chart, side_chart.side_chart], style={'display': 'flex', 'maxHeight':'30%'})

app.layout = html.Div(id= 'big-screen', children=[
    nav_bar.nav_bar,
    html.Div(id='fil colors', children=[choose_filters.choose_filters, show_legends.color_scale]),
    intro_sidebar.instruction_pullouttab,
    multimap_plotly.map_plus_sidebox,
    horizontal_charts,
    dcc.Store(id='chosen-indicators', data=[]),
    dcc.Store(id= 'chosen-data', data= []),
    ],
    style={'height':'100%', 'width': '100%'}) 

#CALLBACKS
@app.callback(
    Output('top10-graph', 'figure'),
    [Input('choose-state', 'value')])

def sort_top10(state):
    if state == 'United States':
        df = data
    else:           
        df = data[data['State'] == state]
    top_10_i = covid_bar_chart.sort_top_num(df, 'covid_cases', 10)
    top_10_i["covid"] = 'FIPS=' + top_10_i.loc[:,'FIPS'] + "<br>" + "County= " + top_10_i.loc[:,'County'] + "<br>" + "State= " + top_10_i.loc[:, 'State'] + "<br>"+ "Number of Covid cases=" + top_10_i.loc[:, 'covid_cases']
    return {
        'data' : [
        {'x': list(top_10_i.County), 
        'y': list(top_10_i.covid_cases), 
        'text': list(top_10_i["covid"]), 
        'type': 'bar', 'name': 'Cases', 'marker': {'color': covid_bar_chart.colors_chart["header"]}
        }],
        'layout': {
        "plot_bgcolor": covid_bar_chart.colors_chart["gray"],
        "paper_bgcolor": covid_bar_chart.colors_chart["header"],
        'color': covid_bar_chart.colors_chart["text"],
        'font': {
        'color': covid_bar_chart.colors_chart['gray']
        },
                'margin': {'t':0,'l':30, 'r':0, 'b':30 }
                }
                }

    
@app.callback(
    Output('choose-county', 'options'),
    #Output('show-time', 'children')],
    [Input('choose-state', 'value')])

def change_cty_options(state):
    if state == "United States":
        return [{'label': i, 'value': i} for i in all_counties]
    else:
        dff= full_data[full_data['State'] == state]
        return [{'label': str(dff.iloc[i]['County + State']), 'value' : str(dff.iloc[i]['County + State'])}  for i in range(dff.shape[0])]
        

def define_data(state, counties):
    if state == "United States":
        if len(counties) == 0:
            return full_data 
        elif len(counties) != 0:
            dff = pd.DataFrame(columns=full_data.columns)
            for cty in counties:
                cty_df = full_data[full_data['County + State'] == cty]
                dff = pd.concat([dff, cty_df], join='outer')
            return dff
    else:
        if len(counties) == 0:
            return full_data[full_data['State']==state]
        elif len(counties) != 0:
            dff2 = pd.DataFrame(columns=full_data.columns)
            for cty in counties:
                cty_df = full_data[full_data['County + State'] == cty]
                dff2 = pd.concat([dff2, cty_df], join='outer')
            return dff2

def break_line(indicators):
    full = ""
    for indicator in indicators:
        full += "<br>" + indicator +" = " + full_data_str[indicator]
    return full


@app.callback(
    [Output('indicators-shown', 'children'), 
    Output('chosen-indicators', 'data')],
    [Input(f'checkbox-{i}', 'value') for i in range(3)]+
    [Input("severe-indicators", 'value'),
    Input("economic-indicators", 'value'),
    Input("mobile-indicators", 'value')])

def show_indicators(score1, score2, score3, metrics1, metrics2, metrics3):
    already_shown = []
    scores = score1 + score2 + score3 + metrics1 + metrics2 + metrics3
    for score in scores:
        if score not in already_shown:
            already_shown.append(score)
    return " | ".join(score for score in already_shown if score), already_shown

@app.callback(
    Output('counties-map', 'figure'),
    [Input('choose-state', 'value'),
    Input('choose-county', 'value'), 
    Input('chosen-indicators', 'data')])

def update_map(state, chosen_counties, chosen_indicator):
    already_shown = []
    chosen_data = define_data(state, chosen_counties)
    if len(chosen_indicator) != 0:
    #    already_shown.append(chosen_indicator[0])
        fig = px.choropleth_mapbox(chosen_data, 
            geojson=counties, locations=chosen_data['FIPS'], 
            color=chosen_indicator[0],
            color_continuous_scale=multimap_plotly.colors_map[chosen_indicator[0]],
            range_color=index_range[chosen_indicator[0]],
            mapbox_style="carto-positron",              
            zoom=3.5, center = {"lat": 37.0902, "lon": -95.7129},
            opacity=0.8,
            labels={chosen_indicator[0]}, hover_data= ["FIPS","State", "County"] + chosen_indicator,
            )
        fig.update_layout(coloraxis_showscale=False, title_text = chosen_indicator[0], margin={"r":0,"t":0,"l":0,"b":0})
        if len(chosen_indicator) > 1:
            for val_indx in range(1, len(chosen_indicator)):
        #        if chosen_indicator[val_indx] not in already_shown:
       #             already_shown.append(chosen_indicator[val_indx])
                fig.add_trace(go.Choroplethmapbox(name = chosen_indicator[val_indx], geojson=counties, locations=chosen_data['FIPS'], z=chosen_data[chosen_indicator[val_indx]],
                            colorscale=multimap_plotly.colors_map[chosen_indicator[val_indx]],
                            zmin=index_range[chosen_indicator[val_indx]][0],
                            zmax=index_range[chosen_indicator[val_indx]][1],
                            marker_line_width=0.1, marker_opacity=0.8, showscale=False, 
                            text= break_line(["FIPS", "State", "County"] + chosen_indicator)
                            # '<br> {} = {} <br>'.format(indicator, chosen_data[indicator]) for indicator in ["FIPS", "County", "State"] + chosen_indicator
                            , hovertemplate = '%{text} <extra></extra>'))
                fig.update_layout(title_text = chosen_indicator[0], margin={"r":0,"t":0,"l":0,"b":0})
    else:
        fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=data.FIPS))
        fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=3.5, mapbox_center = {"lat": 37.0902, "lon": -95.7129}, showlegend=False, margin={"r":0,"t":0,"l":0,"b":0}, height=None)
    return fig

@app.callback(
    Output('color-scales', 'children'),
    [Input('chosen-indicators', 'data')])

def make_image(indicators):
    scales =[]
    #already_shown = []
    for indicator in indicators:
        #if indicator not in already_shown:
        #already_shown.append(indicator)
        cscale = show_legends.make_legend(indicators_lst.index(indicator))
        scales.append(cscale)
    return scales

#********SCORE CHART CALLBACK********
#FOR SIDE CHART CALLBACK
def make_50_df(datamap, i):
    full_datasets50 = {}
    merged_f=datamap[['County','State', criteria[i]]]
    sorted_cases = merged_f.sort_values(by=[criteria[i]], ascending= False)
    top_50 = sorted_cases.head(50)
    return top_50

@app.callback(
    Output('index-score', 'data'),
    [Input('prev-score', 'n_clicks'),
    Input('next-score', 'n_clicks')], 
    [State('index-score', 'data')])

def click_button(previous, next, score_lst):
    ctx = dash.callback_context
    if not ctx.triggered:
        return score_lst
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == "prev-score":
            prev = score_lst.pop(-1)
            score_lst.insert(0, prev)
            return score_lst
        if button_id == 'next-score':
            nex = score_lst.pop(0)
            score_lst.append(nex)
            return score_lst

@app.callback(
    Output('total-ctys', 'data'),
    [Input('choose-state', 'value')], 
    [State('index-score', 'data')])

def determine_total_top(state, score_i):
    #ctx = dash.callback_context
    if state == 'United States':
        total_cty = 50
    else:
        score_indx = score_i[0]
        score = criteria[score_indx]
        datasets50 = make_50_df(full_data[full_data['State'] == state], score_indx)
        total_cty = len(datasets50)
    return total_cty

@app.callback(
    Output('index-county', 'data'),
    [Input('prev-county', 'n_clicks'), 
    Input('next-county', 'n_clicks'), 
    Input('choose-state', 'value')],
    [
    State('total-ctys', 'data'),
    State('index-county', 'data')])

def click_county(prev, next, state, total_cty, num):
    ctx = dash.callback_context
    if not ctx.triggered:
        return num  
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'choose-state':
            num = 0
        elif button_id == 'prev-county':
            if num == 0:
                num = total_cty - 1
            else:
                num = num - 1 
        elif button_id == 'next-county':
            if num == total_cty - 1:
                num = 0
            else:
                num = num + 1
        return num        

text_colors = ['#ff385e', '#0c3f47', '#ffc05f']

@app.callback([Output('chart_num', 'children'), 
    Output('count-score','children'),
    Output('count-score','style'),
    Output('count-county', 'children')], 
    [Input('index-county', 'data'),
    Input('index-score', 'data'), 
    Input('choose-state', 'value'), 
    Input('total-ctys', 'data')])

def chart_display(cty_indx, score_i, state, total_cty):
    #time.sleep(3)
    # cty_indx = county_i
    score_indx = score_i[0]
    score = criteria[score_indx]
    if state == 'United States':
        data = full_data
    else: 
        data = full_data[full_data['State'] == state]
    df = make_50_df(data, score_indx)
    #çdf = full_datasets50[score]
    
    return [
        html.Div(html.H4(children=score, style={'textAlign':'center','fontSize':19, 'marginBottom':0, 'marginTop':0, 'position':'static', 'textOverflow':'ellipsis', 'overflow':'hidden', 'color': text_colors[score_indx]})),
        html.H4('County Score',style={'textAlign':'center', 'fontSize': 18, 'marginBottom': 0, 'position':'static'}),
        html.H4(str(round(df.iloc[cty_indx][score],2)), style= { 'fontWeight': 'bold', 'textAlign':'center', 'marginBottom': 0}),
        html.H5(children= str(df.iloc[cty_indx]['County'] + ", " + df.iloc[cty_indx]['State']), 
        style = {'textAlign':'center', 'fontSize': 19, 'position':'static'})#'margin-bottom': 50,
        ], score, {'textAlign':'center', 'display':'inline-block', 'font-size': '12px', 'textOverflow':'ellipsis', 'color': text_colors[score_indx]}, '{} of {}'.format(cty_indx + 1, total_cty)

        
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
        #return (is_open1, is_open2, is_open3)

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
    Output("score-1-toggle", "className"),
    [Input("score-1-toggle", "n_clicks")],
    [State("collapse-1", "is_open")])

def change_icon(n0, is_open0): 
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
    Output("score-2-toggle", "className"), 
    [Input("score-2-toggle", "n_clicks")],
    [State("collapse-2", "is_open")])

def change_icon(n0, is_open0): 
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
    [Output("sidebar", "className"),
    Output("sidebar-toggle", "className")],
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar", "className")])
def toggle_classname(n, classname):
    if n and classname == "":
        return "collapsed", "collapsed"
    return "", ""

if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port=8080, debug=True)



