import dash
import dash_html_components as html
import pandas as pd
import dash_core_components as dcc

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
criteria = 'Severe COVID Case Complications'


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

#merged.drop(columns=dropped)
merged_f=merged[['County','State', criteria]]
sorted_cases = merged_f.sort_values(by=[criteria], ascending= False)
top_25 = sorted_cases.head(25)
#print(top_25)

data = {'Cap' : ['A', 'B', 'C', ], 'non-Cap' : ['a','b','c', ]}
df = pd.DataFrame(data)

def generate_table(dataframe, max_rows=26):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns]) ] +
        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )





app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H4(children='County Score: Severe COVID Case Complications'),
    generate_table(top_25)
])

if __name__ == '__main__':
    app.run_server(debug=True)