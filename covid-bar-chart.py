import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'header': 'c0c0c0',
    'text': '#7FDBFF',
    'lavender': '#E6E6FA',
    "pink": '#FFC0CB',
    "gray": "#696969"
}

merged = pd.read_csv("../../../Downloads/covid_community_vulnerability-master/data/merged_data.csv")
criteria = "covid_cases"


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

merged.drop(columns=dropped)
sorted_cases = merged.sort_values(by=[criteria], ascending= False)
top_10 = sorted_cases.head(10)
#print(top_10)



app.layout = html.Div(children=[
    html.H1(children='Number of COVID Cases by County',
        style= {
            "textAlign": 'center',
            "color": colors["gray"],
            "font": "Open Sans",
        }),
    dcc.Graph(
        id='example-graph',
        figure={
            'data' : [
                {'x': list(top_10.County), 
                'y': list(top_10.covid_cases), 
                'text': list(top_10.County), 
                'type': 'bar', 'name': 'Cases', 'marker': {'color': colors["header"]}
            }],
            'layout': {
                "plot_bgcolor": colors["gray"],
                "paper_bgcolor": colors["header"],
                'color': colors["text"],
                'font': {
                    'color': colors['gray']
                },
                'width': "90%",
                'margin': {'t':10, 'b':40 }
            }
            }
        ),

    html.Div(children='Last update: 23 mins ago.',
        style= {
            "textAlign": "right",
            "color": colors["gray"]
        })
])

if __name__ == '__main__':
    app.run_server(debug=True)
