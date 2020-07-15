import dash
import dash_html_components as html
import pandas as pd
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', '/assets/font-awesome.min.css', {
    'href': 'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
    'rel': 'stylesheet',
    'integrity': 'sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf',
    'crossorigin': 'anonymous'
}]

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

#full_datasets25 = {}
full_datasets50 = {}

#merged.drop(columns=dropped)
for i in range(3):
    merged_f=side_data[['County','State', criteria[i]]]
    sorted_cases = merged_f.sort_values(by=[criteria[i]], ascending= False)
    top_50 = sorted_cases.head(50)
    #top_50 = sorted_cases.head(50)
    full_datasets50[criteria[i]]= top_50

    #print(top_25)

#print(full_datasets50[criteria[0]])
#print(full_datasets50[criteria[1]])
#print(full_datasets50[criteria[2]])
#print(type(full_datasets50[criteria[0]][full_datasets50[criteria[0]]['County']=='Putnam']['Severe COVID Case Complications']))


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    dcc.Store(id= 'index-score', data=[0,1,2]),
    dcc.Store(id= 'index-county', data = 1),
    html.Div([
        html.I(id='prev-county', className="fa fa-caret-left", **{'aria-hidden': 'true'}, style = {'display':'inline-block', 'font-size': '20px', 'margin-right': '10px'}),
        html.P(id= 'count-county' ,#children='1 of 50',
         style= {'display':'inline-block'}),
        html.I(id='next-county', className= "fa fa-caret-right", **{'aria-hidden': 'true'}, style={'display':'inline-block', 'font-size': '20px', 'margin-left': '10px'})
        ], style= {'text-align': 'center'}),
    html.Div(id= "chart_num", children =[]
        #html.H4(children='County Score: Severe COVID Case Complications'),
        #generate_table(full_datasets25[criteria[0]])
        ),
    html.Div(id= "choose_score", children = [
        html.I(id='prev-score', className="fa fa-caret-left", **{'aria-hidden': 'true'}, style = {'display':'inline-block', 'font-size': '20px','margin-right': '10px'}),
        html.Div(html.P(id= 'count-score', #children='Severe COVID Case Complications',
         style= {'display':'inline-block', 'font-size': '12px', 'text-align':'center'})), 
        html.I(id='next-score', className="fa fa-caret-right", **{'aria-hidden': 'true'}, style={'display':'inline-block', 'font-size': '20px', 'margin-left': '10px'})
        ],style={'display':'flex'})
],
    style = {
            #'label':'no legend',
            'width':200, 'height':360, 
            #'overflowY': 'scroll', 
            'border': '10px solid gray', 'margin': 10, 
            'display': 'inline-block', 'position':'relative', 'padding':10
            })

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
            if num == 1:
                num = 50
            else:
                num = num -1
        if button_id == 'next-county':
            if num == 50:
                num = 1
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
        html.H4(children=score, style={'text-align':'center', 'margin-bottom':20}),
        html.H4('County Score',style={'text-align':'center', 'font-size': 20, 'margin-bottom': 5}),
        html.H4(str(round(df.iloc[cty_indx][score],2)), style= { 'font-weight': 'bold', 'text-align':'center', 'margin-bottom': 5}),
        html.H5(children= str(df.iloc[cty_indx]['County'] + ", " + df.iloc[cty_indx]['State']), style = {'text-align':'center', 'text-size': 10, 'margin-bottom': 40 })
        ], criteria[score_indx], ' {} of 50 '.format(cty_indx)


if __name__ == '__main__':
    app.run_server(debug=True)
