from data import data_processing

from dash import Dash, html, dcc, Input, Output, callback, State, ctx, dash_table  # type: ignore
# import pandas as pd
import datetime
from dash_extensions import WebSocket  # type: ignore
import random

data = data_processing()
fig = data.create_empty_graph()
graph = dcc.Graph(figure=fig, id='graph')
input_min = dcc.Input(id='min', type='number', min=2000, max=2030, value=2018)
input_max = dcc.Input(id='max', type='number', min=2000, max=2030, value=2030)
submit = html.Button(id='submit', children='Submit', n_clicks=0)
side_bar = [html.Div('Input min year', id='min_div'), input_min,
            html.Div('Input max year', id='max_div'), input_max, html.Div(children=submit, id='submit_div')]
upload_button = html.Button(id='upload', children='Upload', n_clicks=0)

filter_div = html.Div(side_bar, id='sidebar', style={'visibility': 'hidden'})
name = dcc.Input(id='name')
dept = dcc.Input(id='dept')
salary = dcc.Input(id='salary', type='number')
button = html.Button(id='button', children='Submit', n_clicks=0)
name_div = html.Div([html.Div('Name:'), name], id='name_div')
dept_div = html.Div([html.Div('Dept:'), dept], id='dept_div')
salary_div = html.Div([html.Div('Salary:'), salary], id='salary_div')
button_div = html.Div(children=button, id='button_div')
click_div = html.Div(children=[name_div, dept_div, salary_div, button_div], style={
    'visibility': 'hidden',}, id='answer')
col1 = html.Div(id='col1', children=[upload_button,
                                     WebSocket(url="ws://127.0.0.1:5000/ws", id="ws"), filter_div, click_div])
tab1 = dcc.Tab(label='Graph View', value='gv')
tab2 = dcc.Tab(label='Dataframe View', value='dv')
tab = dcc.Tabs(id='tab', children=[tab1, tab2], value='gv')
div1 = html.Div(id='tab_gv_output', children=graph)
div2 = html.Div(id='tab_dv_output', style={
                'display': 'none'}, children='No data')
col2 = html.Div(id='col2', children=[tab, div1, div2])
flex_div = html.Div(children=[col1, col2], id='flex', style={'display': 'flex',
                                                             'flex-direction': 'row'})

main_div = [flex_div, dcc.Store(id='max_val'), dcc.Store(
    id='min_val'), dcc.Store(id='timestamp')]


app = Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div(main_div, id='main_div')

# tabs callback

@callback(Output(component_id='tab_gv_output', component_property='style'),
          Output(component_id='tab_dv_output', component_property='style'),
          Input(component_id='tab', component_property='value'),
          prevent_initial_call=True)
def tab_switch(tab):
    if tab == 'gv':
        return [{}, {'display': 'none'}]
    if tab == 'dv':
        if data.fig is None:
            return [{'display': 'none'}, {}]
        else:

            return [{'display': 'none'}, {}]

# upload callback

@callback(Output(component_id='graph', component_property='figure', allow_duplicate=True),
          Output(component_id='sidebar', component_property='style'),
          Output(component_id='tab_dv_output',
                 component_property='children', allow_duplicate=True),
          Input(component_id='upload', component_property='n_clicks'),
          State('graph', 'figure'),
          State('tab_dv_output', 'children'),
          State('min_val', 'data'),
          State('max_val', 'data'),
          prevent_initial_call=True)
def update(upload, fig, dataframe, min_val, max_val):
    if max_val is None and min_val is None:
        fig = data.create_mst_graph()
        arr = []
        df = data.df.drop(columns=['x', 'y'])
        for i in df.columns:
            arr.append({"name": i, "id": i})
        dataframe = dash_table.DataTable(df.to_dict('records'), arr)
        return [fig, {}, dataframe]
    else:
        return [fig, {}, dataframe]

# make edit inputs disappear


@callback(Output(component_id='answer', component_property='style', allow_duplicate=True),
          Input('button', 'n_clicks'),
          prevent_initial_call=True)
def hide(button):
    return {'visibility': 'hidden'}

# filter callback


@callback(Output(component_id='graph', component_property='figure', allow_duplicate=True),
          Output('min_val', 'data'),
          Output('max_val', 'data'),
          Output(component_id='tab_dv_output',
                 component_property='children', allow_duplicate=True),
          Input(component_id='submit', component_property='n_clicks'),
          State(component_id='min', component_property='value'),
          State(component_id='max', component_property='value'),
          prevent_initial_call=True)
def filter_graph(submit, min_val, max_val):
    filter_df, fig = data.update_graph([min_val, max_val])
    arr = []
    df = filter_df.drop(columns=['x', 'y'])
    for i in df.columns:
        arr.append({"name": i, "id": i})
    dataframe = dash_table.DataTable(df.to_dict('records'), arr)
    return [fig, min_val, max_val, dataframe]

# clickdata callback


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

        return [{}, name, True, dept, salary]
    else:
        return [{'visibility': 'hidden'}, '', False, '', '']

# Update graph and df


@callback(Output('graph', 'figure'),
          Output(component_id='tab_dv_output', component_property='children'),
          Input('ws', 'message'),
          State(component_id='min_val', component_property='data'),
          State(component_id='max_val', component_property='data'),
          prevent_initial_call=True)
def update_all(msg, min_val, max_val):
    if max_val is not None and min_val is not None:
        df, fig = data.update_graph([min_val, max_val])

    else:
        df = data.df
        fig = data.create_graph(df)
    df = df.drop(columns=['x', 'y'])
    arr = []
    for i in df.columns:
        arr.append({"name": i, "id": i})
    dataframe = dash_table.DataTable(df.to_dict('records'), arr)
    return [fig, dataframe]


# edit df callback
@callback(Output(component_id='ws', component_property='send', allow_duplicate = True),
          Input('button', 'n_clicks'),
          State('dept', 'value'),
          State('salary', 'value'),
          State('name', 'value'),
          prevent_initial_call=True)
def update_data(button, dept, salary, name):
    data.update_df(name, dept, salary)

    return "updated"+str(random.randint(0,1000))




if __name__ == '__main__':
    app.run(debug = True)



# data = data_processing()
# time = None
# fig = data.create_empty_graph()
# graph = dcc.Graph(figure=fig, id='graph')

# input_min = dcc.Input(id='min', type='number', min=2000, max=2030, value=2018)
# input_max = dcc.Input(id='max', type='number', min=2000, max=2030, value=2030)
# submit = html.Button(id='submit', children='Submit', n_clicks=0)
# side_bar = [html.Div('Input min year', id='min_div'), input_min,
#             html.Div('Input max year', id='max_div'), input_max, html.Div(children=submit, id='submit_div')]
# upload_button = html.Button(id='upload', children='Upload', n_clicks=0)
# filter_div = html.Div(side_bar, id='sidebar', style={'visibility': 'hidden'})
# name = dcc.Input(id='name')
# dept = dcc.Input(id='dept')
# salary = dcc.Input(id='salary', type='number')
# button = html.Button(id='button', children='Submit', n_clicks=0)
# name_div = html.Div([html.Div('Name:'), name], id='name_div')
# dept_div = html.Div([html.Div('Dept:'), dept], id='dept_div')
# salary_div = html.Div([html.Div('Salary:'), salary], id='salary_div')
# button_div = html.Div(children=button, id='button_div')
# click_div = html.Div(children=[name_div, dept_div, salary_div, button_div,WebSocket(url="ws://localhost:5000/ws", id="ws")], style={
#     'visibility': 'hidden',}, id='answer')
# col1 = html.Div(id='col1', children=[upload_button, filter_div, click_div])


# tab1 = dcc.Tab(label='Graph View', value='gv')
# tab2 = dcc.Tab(label='Dataframe View', value='dv')
# tab = dcc.Tabs(id='tab', children=[tab1, tab2], value='gv')
# div1 = html.Div(id='tab_gv_output', children=graph)
# div2 = html.Div(id='tab_dv_output', style={
#                 'display': 'none'}, children='No data')
# col2 = html.Div(id='col2', children=[tab, div1, div2])
# flex_div = html.Div(children=[col1, col2], id='flex', style={'display': 'flex',
#                                                              'flex-direction': 'row'})

# main_div = [flex_div, dcc.Store(id='max_val'), dcc.Store(
#     id='min_val'), dcc.Store(id='timestamp')]
# # main_div.append(WebSocket(url="ws://localhost:5000/ws", id="ws"))
# # tabs callback


# @callback(Output(component_id='tab_gv_output', component_property='style'),
#           Output(component_id='tab_dv_output', component_property='style'),
#           Input(component_id='tab', component_property='value'),
#           prevent_initial_call=True)
# def tab_switch(tab):
#     if tab == 'gv':
#         return [{}, {'display': 'none'}]
#     if tab == 'dv':
#         if data.fig is None:
#             return [{'display': 'none'}, {}]
#         else:

#             return [{'display': 'none'}, {}]

# # upload callback


# @callback(Output(component_id='graph', component_property='figure', allow_duplicate=True),
#           Output(component_id='sidebar', component_property='style'),
#           Output(component_id='tab_dv_output',
#                  component_property='children', allow_duplicate=True),
#           Input(component_id='upload', component_property='n_clicks'),
#           State('graph', 'figure'),
#           State('tab_dv_output', 'children'),
#           State('min_val', 'data'),
#           State('max_val', 'data'),
#           prevent_initial_call=True)
# def update(upload, fig, dataframe, min_val, max_val):
#     if max_val is None and min_val is None:
#         fig = data.create_mst_graph()
#         arr = []
#         df = data.df.drop(columns=['x', 'y'])
#         for i in df.columns:
#             arr.append({"name": i, "id": i})
#         dataframe = dash_table.DataTable(df.to_dict('records'), arr)
#         return [fig, {}, dataframe]
#     else:
#         return [fig, {}, dataframe]



# # make edit inputs disappear


# @callback(Output(component_id='answer', component_property='style', allow_duplicate=True),
#           Input('button', 'n_clicks'),
#           prevent_initial_call=True)
# def hide(button):
#     return {'visibility': 'hidden'}

# # filter callback


# @callback(Output(component_id='graph', component_property='figure', allow_duplicate=True),
#           Output('min_val', 'data'),
#           Output('max_val', 'data'),
#           Output(component_id='tab_dv_output',
#                  component_property='children', allow_duplicate=True),
#           Input(component_id='submit', component_property='n_clicks'),
#           State(component_id='min', component_property='value'),
#           State(component_id='max', component_property='value'),
#           prevent_initial_call=True)
# def filter_graph(submit, min_val, max_val):
#     filter_df, fig = data.update_graph([min_val, max_val])
#     arr = []
#     df = filter_df.drop(columns=['x', 'y'])
#     for i in df.columns:
#         arr.append({"name": i, "id": i})
#     dataframe = dash_table.DataTable(df.to_dict('records'), arr)
#     return [fig, min_val, max_val, dataframe]


# # clickdata callback
# @callback(Output(component_id='answer', component_property='style'),
#           Output('name', 'value'),
#           Output('name', 'readOnly'),
#           Output('dept', 'value'),
#           Output('salary', 'value'),
#           Input(component_id='graph', component_property='clickData'),
#           prevent_initial_call=True)
# def update(clickData):
#     if clickData is not None:

#         name = clickData['points'][0]['customdata'][0]
#         dept = clickData['points'][0]['customdata'][1]
#         salary = clickData['points'][0]['customdata'][3]

#         return [{}, name, True, dept, salary]
#     else:
#         return [{'visibility': 'hidden'}, '', False, '', '']

# # Update graph and df


# @callback(Output('graph', 'figure'),
#           Output(component_id='tab_dv_output', component_property='children'),
#           Input('ws', 'message'),
#           State(component_id='min_val', component_property='data'),
#           State(component_id='max_val', component_property='data'),
#           prevent_initial_call=True)
# def update_all(msg, min_val, max_val):
#     if max_val is not None and min_val is not None:
#         df, fig = data.update_graph([min_val, max_val])

#     else:
#         df = data.df
#         fig = data.create_graph(df)
#     df = df.drop(columns=['x', 'y'])
#     arr = []
#     for i in df.columns:
#         arr.append({"name": i, "id": i})
#     dataframe = dash_table.DataTable(df.to_dict('records'), arr)
#     return [fig, dataframe]

# # edit df callback


# @callback(Output(component_id='ws', component_property='send'),
#           Input('button', 'n_clicks'),
#           State('dept', 'value'),
#           State('salary', 'value'),
#           State('name', 'value'),
#           prevent_initial_call=True)
# def update_data(button, dept, salary, name):
#     data.update_df(name, dept, salary)

#     return "updated"

# app = Dash(__name__, suppress_callback_exceptions=True)
# app.layout = html.Div(main_div, id='main_div')
# if __name__ == '__main__':
#     app.run(debug=True)


