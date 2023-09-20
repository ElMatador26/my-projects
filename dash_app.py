# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 15:54:03 2023

@author: 2130006
"""

# import streamlit as st
# from streamlit_echarts import st_echarts

# st.write('Echarts plot')
# options = {
#     "xAxis": {
#         "type": "category",
#         "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
#     },
#     "yAxis": {"type": "value"},
#     "series": [
#         {"data": [820, 932, 901, 934, 1290, 1330, 1320], "type": "line"}
#     ],
#     'symbolSize': '[100, 200, 300, 400, 500, 600, 700]'
# }
# events = {"click": "function(params) { console.log(params.name); return params.name }"}
# val = st_echarts(options=options, events = events)
# st.write(val)
# st.write('Agraph graph')
# from streamlit_agraph import agraph, Node, Edge, Config

# nodes = []
# edges = []
# nodes.append( Node(id=1,  
#                    size=10, 
#                    x =100,
#                    y=50
#                    ) 
#             ) # includes **kwargs
# nodes.append( Node(id=2, 
#                    size=15,
#                    x=50,
#                    y=50
#                    ) 
#             )
# nodes.append( Node(id=3, 
#                    size=5,
#                    x=400,
#                    y=50
#                    ) 
#             )
# edges.append( Edge(source=1, 
#                    label='5', 
#                    target=2, 
#                    # **kwargs
#                    ) 
#             ) 
# edges.append( Edge(source=1, 
#                    label='7', 
#                    target=3, 
#                    # **kwargs
#                    ) 
#             )
# config = Config(width=600,
#                 height=200,
#                 directed=False, 
#                 physics=False, 
#                 hierarchical=False,
#                 # **kwargs
#                 )

# return_value = agraph(nodes=nodes, 
#                       edges=edges, 
#                       config=config)

# st.write(return_value)

# st.write('Using plotly events library')
# import plotly.express as px
# from streamlit_plotly_events import plotly_events

# # Writes a component similar to st.write()

# fig = px.scatter(x=[1, 2, 3], y=[1, 4, 9], size = [1,8,27])
# selected_points = plotly_events(fig)


# st.write(selected_points)

from data import data_processing
from dash import Dash, html, dcc, Input, Output, callback, State, ctx, dash_table

data = data_processing()

fig = data.create_empty_graph()
graph = dcc.Graph(figure=fig, id='graph')
input_min = dcc.Input(id='min', type='number', min=2000, max=2030, value=2018)
input_max = dcc.Input(id='max', type='number', min=2000, max=2030, value=2030)
submit = html.Button(id = 'submit', children = 'Submit', n_clicks = 0)
side_bar = [html.H1('Input min year'), input_min,
            html.H1('Input max year'), input_max, submit]
upload_button = html.Button(id='upload', children='Upload', n_clicks=0)
filter_div = html.Div(side_bar, id='sidebar', style={'visibility': 'hidden'})
name = dcc.Input(id='name')
dept = dcc.Input(id='dept')
salary = dcc.Input(id='salary', type='number')
button = html.Button(id='button', children='Submit', n_clicks=0)
click_div = html.Div(children=[name, dept, salary, button], style={
                     'display': 'none'}, id='answer')
col1 = html.Div(id = 'col1', children = [upload_button, filter_div, click_div])
col2_style = {
    'height': '70%',
    'width': '100%',
    'padding-right': '1em',
    'border-left': '0.4em solid',
    'border-color': 'deepskyblue',
    'padding-left': '1em',
    'padding-top': '2em',
    'padding-right': '1em'
}

tab1 = dcc.Tab(label='Graph View', value='gv')
tab2 = dcc.Tab(label='Dataframe View', value='dv')
tab = dcc.Tabs(id='tab', children=[tab1, tab2], value='gv')
div1 = html.Div(id='tab_gv_output', children=graph)
div2 = html.Div(id='tab_dv_output', style={
                'display': 'none'})
col2 = html.Div(id = 'col2', children=[tab, div1, div2], style=col2_style)
flex_div = html.Div(children = [col1, col2], id = 'flex', style = {'display': 'flex',
  'flex-direction': 'row'})

main_div = [flex_div, dcc.Store(id = 'Memory', storage_type = 'Session')]


@callback(Output(component_id='tab_gv_output', component_property='style'),
          Output(component_id='tab_dv_output', component_property='style'),
          Output(component_id='tab_dv_output', component_property='children', allow_duplicate=True),
          Input(component_id='tab', component_property='value'),    
          prevent_initial_call=True)
def tab_switch(tab):
    if tab == 'gv':
        return [{}, {'display': 'none'},'']
    if tab == 'dv':
        if data.fig is None:
            return [{'display': 'none'}, {}, 'No data']
        else:
            arr = []
            if data.filter_df is None:
                df = data.df.drop(columns=['x', 'y'])
            else:
                df = data.filter_df.drop(columns=['x', 'y'])
            for i in df.columns:
                arr.append({"name": i, "id": i})
            dataframe = dash_table.DataTable(df.to_dict('records'), arr)
            return [{'display': 'none'}, {}, dataframe]


@callback(Output(component_id='graph', component_property='figure'),
          Output(component_id='tab_dv_output', component_property='children'),
          Output(component_id='answer',
                 component_property='style', allow_duplicate=True),
          Output(component_id='sidebar', component_property='style'),
          Input(component_id='upload', component_property='n_clicks'),
          State(component_id='min', component_property='value'),
          State(component_id='max', component_property='value'),
          Input(component_id = 'submit', component_property = 'n_clicks'),
          Input('button', 'n_clicks'),
          State('dept', 'value'),
          State('salary', 'value'),
          State('name', 'value'),
          prevent_initial_call=True)
def update(upload, min_val, max_val, submit, button, dept, salary, name):
    trig_id = ctx.triggered_id
    if trig_id == 'upload':
        fig = data.create_mst_graph()
        arr = []
        df = data.df.drop(columns=['x', 'y'])
        for i in df.columns:
            arr.append({"name": i, "id": i})
            dataframe = dash_table.DataTable(df.to_dict('records'), arr)
        return [fig, dataframe,{'display': 'none'}, {}]

    if trig_id == 'submit':
        graph = data.update_graph([min_val, max_val])
        arr = []
        df = data.filter_df.drop(columns=['x', 'y'])
        for i in df.columns:
            arr.append({"name": i, "id": i})
        dataframe = dash_table.DataTable(df.to_dict('records'), arr)
        return [graph, dataframe, {'display': 'none'}, {}]
    else:
        return [data.update_df(name, dept, salary), 'No data', {'display': 'none'}, {}]


@callback(Output(component_id='answer', component_property='style'),
          Output('name', 'value'),
          Output('name', 'readOnly'),
          Output('dept', 'value'),
          Output('salary', 'value'),
          Input(component_id='graph', component_property='clickData'),
          prevent_initial_call=True)
def update(clickData):
    if clickData is not None:

        name = clickData['points'][0]['customdata'][0]
        dept = clickData['points'][0]['customdata'][1]
        salary = clickData['points'][0]['customdata'][3]

        return [{'padding-top': '2em'}, name, True, dept, salary]
    else:
        return [{'display': 'none'}, '', False, '', '']


div_style = {
    'opacity': '0.8',
    'background-color': '#ccc',
    'position': 'fixed',
    'width': '100%',
    'height': '100%',
    'top': '0px',
    'left': '0px',
    'z-index': '1000'
}

app = Dash(__name__, suppress_callback_exceptions=True)
app.layout = html.Div(main_div, style=div_style)
if __name__ == '__main__':
    app.run(debug=True)