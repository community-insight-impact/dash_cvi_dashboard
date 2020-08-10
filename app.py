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
import dash_bootstrap_components as dbc
from AllComponents import sigma_calculation as sig
from AllComponents import choose_filters as filters
from AllComponents import covid_bar_chart as bar
#from All Components import dropdown_menu as menu
from AllComponents import intro_sidebar as intro
from AllComponents import last_updated as updated 
from AllComponents import multimap_plotly as multimap 
from AllComponents import nav_bar as nav 
from AllComponents import side_chart as side
from AllComponents import show_legends as legend


#MERGE ALL DATA INTO 1 DF
data = pd.read_csv("data/severe_cases_score_data.csv", dtype={'FIPS': str})
data_str = data.applymap(str)
data2 = pd.read_csv("data/economic_score_data.csv", dtype={'FIPS': str})
data3 = pd.read_csv("data/mobile_health_score_data.csv", dtype={'FIPS': str})

#Add county +state name
all_counties = []
big_i = data.shape[0]
for each_i in range(big_i):
    cty= str(data.iloc[each_i]['County'] + ", " + data.iloc[each_i]['State'])
    all_counties.append(cty)
#print(all_counties)
data['County + State'] = all_counties

#FULL DATAFRAME
full_data = data.merge(data2, how='outer').merge(data3, how='outer')
full_data_str = full_data.applymap(str)

#SCORES
criteria = ['Severe COVID Case Complications', 'Risk of Severe Economic Harm', 'Need for Mobile Health Resources']

#FOR SIDE CHART
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
'% Severe Housing Problems',
'% Enrolled in Free or Reduced Lunch',
'% Unemployed',
'High School Graduation Rate',
'Primary Care Physicians Rate',
'% Home Internet Access',
'Risk of Severe Economic Harm', 
'Need for Mobile Health Resources',
]

#FOR HOVERBOARD
data_lst = ['County', 'State'] + indicators_lst
full_data['all_data'] =  full_data['FIPS'] + "<br>" + "County= " + full_data['County'] + "<br>" + "State= " + full_data['State'] 
for indicator in indicators_lst:
    full_data['all_data'] = full_data['all_data'] + "<br>" + indicator +"= " + full_data_str[indicator]


external_stylesheets = [dbc.themes.BOOTSTRAP, 'https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets= external_stylesheets, 
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

#LAYOUT
horizontal_charts = html.Div(children= [bar.bar_chart, side.side_chart], style={'display': 'flex'})

app.layout = html.Div(id= 'big-screen', children=[
    nav.nav_bar,
    filters.choose_filters,
    multimap.map_plus_sidebox,
    horizontal_charts,
    intro.instruction_pullouttab,
    dcc.Store(id='chosen-indicators', data=[]),
    dcc.Store(id= 'chosen-data', data= []),
    legend.color_scale,
    # dji.Import(src="/assets/intro_autocollapse.js")
    ],
    style={'height':'100%', 'width': '100%'}) #'overflow':'hidden'})# 'margin':{"r":0,"t":20,"l":0,"b":0}})
# app.layout += html.Article(dji.Import(src="/assets/intro_autocollapse.js"))

#CALLBACKS
@app.callback(
    Output('top10-graph', 'figure'),
    [Input('choose-state', 'value')])

def sort_top10(state):
    if state == 'United States':
        df = data
    else:           
        df = data[data['State'] == state]
    top_10_i = bar.sort_top_num(df, 'covid_cases', 10)
    top_10_i["covid"] = 'FIPS=' + top_10_i.loc[:,'FIPS'] + "<br>" + "County= " + top_10_i.loc[:,'County'] + "<br>" + "State= " + top_10_i.loc[:, 'State'] + "<br>"+ "Number of Covid cases=" + top_10_i.loc[:, 'covid_cases']
    return {
        'data' : [
        {'x': list(top_10_i.County), 
        'y': list(top_10_i.covid_cases), 
        'text': list(top_10_i["covid"]), 
        'type': 'bar', 'name': 'Cases', 'marker': {'color': bar.colors_chart["header"]}
        }],
        'layout': {
        "plot_bgcolor": bar.colors_chart["gray"],
        "paper_bgcolor": bar.colors_chart["header"],
        'color': bar.colors_chart["text"],
        'font': {
        'color': bar.colors_chart['gray']
        },
                #'width': "50%",
                #'height': '30%',
                'margin': {'t':0,'l':30, 'r':0, 'b':30 }
                #'margin':{'t':0, 'b':0 }
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
        dff= data[data['State']== state]
        return [{'label': str(dff.iloc[i]['County + State']), 'value' : str(dff.iloc[i]['County + State'])}  for i in range(dff.shape[0])]
        

@app.callback(
    Output('chosen-data','data'),
    [Input('choose-state','value'), 
    Input('choose-county', 'value')])

def define_data(state, counties):
    if state == "United States":
        if len(counties) == 0:
            return full_data.to_dict('list') 
        elif len(counties) != 0:
            dff = pd.DataFrame(columns=full_data.columns)
            for cty in counties:
                cty_df = full_data[full_data['County + State'] == cty]
                dff = pd.concat([dff, cty_df], join='outer')
            return dff.to_dict('list')
    else:
        if len(counties) == 0:
            return full_data[full_data['State']==state].to_dict('list')
        elif len(counties) != 0:
            dff2 = pd.DataFrame(columns=full_data.columns)
            for cty in counties:
                cty_df = full_data[full_data['County + State'] == cty]
                dff2 = pd.concat([dff2, cty_df], join='outer')
            return dff2.to_dict('list')

@app.callback(
    [Output('indicators-shown', 'children'), 
    Output('chosen-indicators', 'data')],
    [Input(f'checkbox-{i}', 'value') for i in range(3)]+
    [Input("severe-indicators", 'value'),
    Input("economic-indicators", 'value'),
    Input("mobile-indicators", 'value')])

def show_indicators(score1, score2, score3, metrics1, metrics2, metrics3):
    scores = score1 + score2 + score3 + metrics1 + metrics2 + metrics3
    return " | ".join(score for score in scores if score), scores

@app.callback(
    Output('counties-map', 'figure'),
    #Output('show-time', 'children')],
    [Input('chosen-data', 'data'), 
    Input('chosen-indicators', 'data')])

def update_map(chosen_data, chosen_indicator):
    #if chosen_state != None:
    #if chosen_state == "United States":
    already_shown = []
    if len(chosen_indicator) != 0:
            #if chosen_state == "United States":\
        already_shown.append(chosen_indicator[0])
        fig = px.choropleth_mapbox(chosen_data, 
            geojson=counties, locations=chosen_data['FIPS'], 
            color=chosen_indicator[0],
            color_continuous_scale=multimap.colors_map[chosen_indicator[0]],
            range_color=multimap.index_range[chosen_indicator[0]],
            mapbox_style="carto-positron",              
            zoom=3.5, center = {"lat": 37.0902, "lon": -95.7129},
            opacity=0.8,
            labels={chosen_indicator[0]}, hover_data= ['County', 'State'] + indicators_lst,
            )
        fig.update_layout(coloraxis_showscale=False, title_text = chosen_indicator[0], margin={"r":0,"t":0,"l":0,"b":0})
        #fig.update_layout(title_text = chosen_indicator[0], margin={"r":0,"t":0,"l":0,"b":0})
        if len(chosen_indicator) > 1:
            for val_indx in range(1, len(chosen_indicator)):
                if chosen_indicator[val_indx] not in already_shown:
                    already_shown.append(chosen_indicator[val_indx])
                    fig.add_trace(go.Choroplethmapbox(name = chosen_indicator[val_indx], geojson=counties, locations=chosen_data['FIPS'], z=chosen_data[chosen_indicator[val_indx]],
                            colorscale=multimap.colors_map[chosen_indicator[val_indx]],
                            zmin=multimap.index_range[chosen_indicator[val_indx]][0],
                            zmax=multimap.index_range[chosen_indicator[val_indx]][1],
                            marker_line_width=0.1, marker_opacity=0.8, showscale=False, #hovertemplate =  "FIPS=%{data.FIPS}<br>County=%%{data.County}<br>State=%%{data.State}<extra></extra>"))
                            text= chosen_data['all_data'], hovertemplate = 'FIPS= %{text} <extra></extra>'))#, hovertemplate= data_lst ))#, hovertext=[data[y] for y in indicators_lst]))
                            #hovertemplate=[County: %{data['County']}, State:%{data['State']}] + [y: %{data[y]} for y in indicators_lst]))
                    fig.update_layout(title_text = chosen_indicator[0], margin={"r":0,"t":0,"l":0,"b":0})
                    #fig.update_layout(hover_data= ['County', 'State'] + indicators_lst)
    else:
        fig = multimap.empty_fig#go.Figure(go.Choroplethmapbox(geojson=counties, locations=data.FIPS))
            #fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=3.5, mapbox_center = {"lat": 37.0902, "lon": -95.7129}, showlegend=False)
        #fig.update_trace(hover_data= ['County', 'State'] + indicators_lst)
        #geojson=counties, locations=data.FIPS, hover_data= ['County', 'State'] + indicators_lst))
    return fig

@app.callback(
    Output('color-scales', 'children'),
    [Input('chosen-indicators', 'data')])

def make_image(indicators):
    scales =[]
    for indicator in indicators:
        cscale = legend.make_legend(indicators_lst.index(indicator))
        scales.append(cscale)
    return scales

#********SCORE CHART CALLBACK********
#FOR SIDE CHART CALLBACK
def make_50_df(datamap, i):
    full_datasets50 = {}
    merged_f=datamap[['County','State', criteria[i]]]
    sorted_cases = merged_f.sort_values(by=[criteria[i]], ascending= False)
    top_50 = sorted_cases.head(50)
    #full_datasets50[criteria[i]]= top_50
    return top_50

@app.callback(
    Output('index-score', 'data'),
    [Input('prev-score', 'n_clicks'),
    Input('next-score', 'n_clicks')], 
    [State('index-score', 'data')])

def click_button(previous, next, score_lst):
    ctx = dash.callback_context
    if not ctx.triggered:
        return score_lst#, criteria[score_lst[0]]
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        # print(button_id)
        if button_id == "prev-score":
            prev = score_lst.pop(-1)
            score_lst.insert(0, prev)
            return score_lst#, criteria[score_lst[0]]
        if button_id == 'next-score':
            nex = score_lst.pop(0)
            score_lst.append(nex)
            return score_lst#, criteria[score_lst[0]]

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
        #df = full_datasets50[score]
        total_cty = len(datasets50)
    return total_cty

@app.callback(
    Output('index-county', 'data'),
    #Output('count-county', 'children')],
    [Input('prev-county', 'n_clicks'), 
    Input('next-county', 'n_clicks'), 
    Input('choose-state', 'value')],
    [
    State('total-ctys', 'data'),
    State('index-county', 'data')])

def click_county(prev, next, state, total_cty, num):
    ctx = dash.callback_context
    # dif = total_cty - num
    #num = total_cty - dif
    if not ctx.triggered:
        return num  #, '{} of 50'.format(num) 
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'choose-state':
            num = 0
        elif button_id == 'prev-county':
            if num == 0:
                num = total_cty - 1
            else:
                num = num - 1 
            #return num
        elif button_id == 'next-county':
            if num == total_cty - 1:
                num = 0
            else:
                num = num + 1
        # print(num)
        # ctx_msg = json.dumps({
        #     'states': ctx.states,
        #     'triggered': ctx.triggered,
        #     'inputs': ctx.inputs
        # }, indent=2)

        return num #, '{} of 50'.format(num)        


# print(full_data.shape[0])
# print(full_data)

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
        html.Div(html.H4(children=score, style={'textAlign':'center','fontSize':18, 'marginBottom':0, 'position':'static', 'textOverflow':'ellipsis', 'overflow':'hidden', 'color': text_colors[score_indx]})),
        html.H4('County Score',style={'textAlign':'center', 'fontSize': 18, 'marginBottom': 5, 'position':'static'}),
        html.H4(str(round(df.iloc[cty_indx][score],2)), style= { 'fontWeight': 'bold', 'textAlign':'center', 'marginBottom': 5}),
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


