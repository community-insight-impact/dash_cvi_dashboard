import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
data = pd.read_csv("data/severe_cases_score_data.csv", dtype={'FIPS': str})

#define colors
colors_chart = {
    'header': 'c0c0c0',
    'text': '#7FDBFF',
    'lavender': '#E6E6FA',
    "pink": '#FFC0CB',
    "gray": "#696969"
}

def sort_top_num(df, crit, num):
    #df_ = df.drop(columns=dropped)
    sorted_df = df.sort_values(by=crit, ascending= False)
    top_num_int = sorted_df.head(num)
    top_num = top_num_int.applymap(str)
    return top_num

top_10 = sort_top_num(data, 'covid_cases', 10)
top_10["covid"] = top_10.loc[:,'FIPS'] + "<br>" + "County= " + top_10.loc[:,'County'] + "<br>" + "State= " + top_10.loc[:, 'State'] + "<br>"+ "Number of Covid cases=" + top_10.loc[:, 'covid_cases']


bar_chart = html.Div(children=[
    html.H1(children='Confirmed Cases by County',
        style= {
        "textAlign": 'left',
        "color": colors_chart["gray"],
        "font": "Open Sans",  'font-size': 25, 'marginTop': '10px', 'margin-bottom':0
        }),
    dcc.Graph(
        id='top10-graph',
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
                , style= {'height': '95%', 'width': "95%", 'margin-top': 0, 'float':'left', 'display':'inline-block'}
                ),
                #last_updated_indicator
                ], style = {'display':'grid', 'width': "79%", 'margin': '5px'})

# if __name__ == '__main__':
#     app.run_server(debug=True)
