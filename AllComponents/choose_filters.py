import pandas as pd
import dash_html_components as html
import dash_core_components as dcc

#LIST OF ALL STATES
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
data['County + State'] = all_counties

#FULL DATAFRAME
full_data = data.merge(data2, how='outer').merge(data3, how='outer')

all_states = list(full_data.State.unique())
all_states.insert(0, "United States")

#LIST OF COUNTIES
all_counties = []
big_i = data.shape[0]
for each_i in range(big_i):
    cty= str(data.iloc[each_i]['County'] + ", " + data.iloc[each_i]['State'])
    all_counties.append(cty)

choose_filters = html.Div([
        html.Div([
            html.Label('Filter by State'),
            dcc.Dropdown(
                id = 'choose-state',
                options= [{'label': state, 'value': state} for state in all_states],
                value= 'United States',
                clearable = False
        )
    ],
    style={'width': '50%', 'display': 'inline-block'}),

        html.Div([
            html.Label('Filter by County'),
            dcc.Dropdown(
                id='choose-county',
                options=[{'label': i, 'value': i} for i in all_counties],
                value=[],
                multi = True,
                placeholder= "Search..."
            )
    ],
    style={'width': '50%', 'display': 'inline-block'})
    ], 
    style={'height': '10%', 'display': 'flex', 'zIndex':-1, 'marginLeft': '5px'}
    )