import dash_html_components as html
import dash_core_components as dcc

side_chart = html.Div(children=[
            #STORE THE DATA TO BE FLIPPED TO
            dcc.Store(id= 'index-score', data=[0,1,2]),
            dcc.Store(id= 'index-county', data = 0),
            dcc.Store(id='total-ctys', data=50),
            dcc.Store(id='cty-distance', data= 50),
            
            #HTML BOX COMPONENT    
            html.Div([
            html.I(id='prev-county', className="fa fa-caret-left", **{'aria-hidden': 'true'}, style = {'display':'inline-block', 'font-size': '15px', 'margin-right': '8px'}),
            html.P(id= 'count-county' ,
         style= {'display':'inline-block', 'textOverflow':'ellipsis', 'fontSize': '13px'}),
            html.I(id='next-county', className= "fa fa-caret-right", **{'aria-hidden': 'true'}, style={'display':'inline-block', 'font-size': '15px', 'margin-left': '8px'})
        ], style= {'textAlign': 'center', 'position':'static'}),
            html.Div(id= "chart_num", children =[]
        , style = {'position':'static','display':'grid'}),
            html.Div(id= "choose_score", children = [
               html.I(id='prev-score', className="fa fa-caret-left", **{'aria-hidden': 'true'}, style = {'display':'inline-block', 'fontSize': '16px','marginRight': '10px', 'marginTop':'5px'}),
               html.Div(html.P(id= 'count-score',
                    ), style = {'width': '100%'}), 
               html.I(id='next-score', className="fa fa-caret-right", **{'aria-hidden': 'true'}, style={'display':'inline-block', 'fontSize': '16px', 'marginLeft': '10px',
           'marginTop':'5px'})
               ],style={'textAlign': 'center', 'position':'static', 'display':'flex', 'marginTop':'10px'})
            ],
    style = {
            'width':'20%', 'maxHeight':'300px', 
            'overflow':'scroll',
            'border': '5px solid gray',
            'display': 'grid', 
            'padding':'5px'
            })


