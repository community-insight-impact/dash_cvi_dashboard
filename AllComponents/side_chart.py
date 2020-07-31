import dash
import dash_html_components as html
import dash_core_components as dcc

side_chart = html.Div(children=[
            dcc.Store(id= 'index-score', data=[0,1,2]),
            dcc.Store(id= 'index-county', data = 0),
            html.Div([
            html.I(id='prev-county', className="fa fa-caret-left", **{'aria-hidden': 'true'}, style = {'display':'inline-block', 'font-size': '14px', 'margin-right': '8px'}),
            html.P(id= 'count-county' ,#children='1 of 50',
         style= {'display':'inline-block', 'textOverflow':'ellipsis', 'fontSize': '13px'}),
            html.I(id='next-county', className= "fa fa-caret-right", **{'aria-hidden': 'true'}, style={'display':'inline-block', 'font-size': '14px', 'margin-left': '8px'})
        ], style= {'textAlign': 'center', 'position':'static'}),
            html.Div(id= "chart_num", children =[]
        #html.H4(children='County Score: Severe COVID Case Complications'),
        #generate_table(full_datasets25[criteria[0]])
        , style = {'position':'static','display':'grid'}),
            html.Div(id= "choose_score", children = [
               html.I(id='prev-score', className="fa fa-caret-left", **{'aria-hidden': 'true'}, style = {'display':'inline-block', 'fontSize': '15px','marginRight': '10px', 'marginTop':'5px'}),
               html.Div(html.P(id= 'count-score', #children='Severe COVID Case Complications'
                    style= {'textAlign':'center', 'display':'inline-block', 'font-size': '12px', 'textOverflow':'ellipsis'}), style = {'width': '100%'}), #style = {'width': 150, 'position':'static', 'textOverflow':'ellipsis'}, 
               html.I(id='next-score', className="fa fa-caret-right", **{'aria-hidden': 'true'}, style={'display':'inline-block', 'fontSize': '15px', 'marginLeft': '10px',
           'marginTop':'5px'})
               ],style={'textAlign': 'center', 'position':'static', 'display':'flex', 'marginTop':'20px'})#'display':'flex', 'margin-top':55,'margin-left':30, 'position':'static'}) #'position':'static', 'text-align':'center'})
            ],
    style = {
            #'label':'no legend',
            'width':'20%', 'maxHeight':'300px', #'maxHeight':400, 
            #'overflowY': 'scroll', 
            #'margin-left': 10,
            'overflow':'scroll',
            'border': '5px solid gray', #'margin': 10,
            'display': 'grid', 
            #'position':'static', 
            'padding':'5px'
            })


