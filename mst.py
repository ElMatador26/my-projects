import pandas as pd
import nltk
import numpy as np
from scipy import sparse
from scipy.sparse.csgraph import minimum_spanning_tree
import plotly.express as px
from dash import Dash, html, dcc, Input, Output, callback, State, ctx


class data_processing:
    # this class be used to work with data

    def __init__(self):
        # this method creates dummy data when there is no dataframe

        dict1 = {'name': ['Ayan', 'Ram', 'Shyam', 'Jodu', 'Modu'],
                 'department': ['AIA', 'CDB', 'QEA', 'AIA', 'QEA'],
                 'doj': ['10/2/2021', '4/23/2023', '8/8/2021', '2/15/2019', '2/2/2020'],
                 'salary': [1000, 200, 300, 500, 600]}

        self.df = pd.DataFrame(dict1)
        self.df['doj'] = pd.to_datetime(self.df.doj, format='%m/%d/%Y')
        self.mat = None
        self.filter_df = None
        self.fig = None

    def _init_(self, df):
        # this method accepts the dataframe if its given
        self.df = df
        self.mat = None
        self.filter_df = None
        self.fig = None

    def distance(self, col: str = 'name'):
        # calculates the distance when given an attribute

        mat = np.zeros(shape=(self.df.shape[0], self.df.shape[0]))
        for i in range(self.df.shape[0]):
            for j in range(i, self.df.shape[0]):
                mat[i, j] = (nltk.edit_distance(
                    self.df.loc[i, col], self.df.loc[j, col]))
        mat = sparse.csr_matrix(mat)
        return mat

    def __coord_generator(self, prev=None, d=None):

        # make generate coordinates of new point based on old point

        if prev is None:
            x = np.random.uniform(0, 10)
            y = np.random.uniform(0, 10)
        else:
            angle = np.random.uniform(0, 7)
            x = prev[0]+(d*np.sin(angle))
            y = prev[1]+(d*np.cos(angle))
        # if prev is not None:
        #     dist = ((prev[0]-x)**2)+((prev[1]-y)**2)
        #     print(d, dist**0.5)
        return (x, y)

    def mst(self):
        #find the minimum spanning tree

        mat = self.mat
        if mat is None:
            mat = self.distance()
        mat = self.mat = minimum_spanning_tree(mat)
        return mat

    def __create_coord_dict(self, mat):
        #creates the coordinates of the data

        l = mat.shape[0]
        mat = sparse.coo_matrix(mat)
        dict1 = None
        i = 0
        j = 0
        while l != j:
            if dict1 is None:
                dict1 = {}
                dict1[mat.row[i]] = self.__coord_generator()
                j += 1
            if mat.row[i] in dict1 and mat.col[i] not in dict1:
                dict1[mat.col[i]] = self.__coord_generator(
                    dict1[mat.row[i]], mat.data[i])
                j += 1
            if mat.row[i] not in dict1 and mat.col[i] in dict1:
                dict1[mat.row[i]] = self.__coord_generator(
                    dict1[mat.col[i]], mat.data[i])
                j += 1

            i = (i+1) % l
        return dict1

    def create_empty_graph(self):
        # creates the empty graph

        fig = px.scatter()
        fig.update_yaxes(tickmode='linear', tick0=0, dtick=1)
        fig.update_xaxes(tickmode='linear', tick0=0, dtick=1)
        fig.update_layout(title_text='Sample Dataset')
        return fig

    def create_mst_graph(self):
        # creates the mst graph in plotly
        
        if self.fig is not None:
            return self.fig
        mat = self.mst()
        dict1 = self.__create_coord_dict(mat)
        for i in dict1:
            self.df.loc[i, 'x'] = dict1[i][0]
            self.df.loc[i, 'y'] = dict1[i][1]

        hover_dict = {}
        for i in self.df.columns:
            if i == 'x' or i == 'y':
                hover_dict[i] = False
            else:
                hover_dict[i] = True

        fig = px.scatter(self.df, x='x', y='y', size='salary',
                         hover_data=hover_dict)
        # maxy = np.roof(self.df['y'].max())
        # maxx = np.roof(self.df['x'].max())
        fig.update_yaxes(tickmode='linear', tick0=0, dtick=1)
        fig.update_xaxes(tickmode='linear', tick0=0, dtick=1)
        fig.update_layout(title_text='Sample Dataset')
        self.fig = fig

        return fig

    def update_graph(self, arr):
        # updates the graph based on the condition
        fig = self.fig
        df = self.df[(self.df['doj'].dt.year >= arr[0])
                     & (self.df['doj'].dt.year <= arr[1])]

        fig.data[0].x = df['x']
        fig.data[0].y = df['y']
        fig.data[0].marker.size = df['salary']
        fig.data[0].customdata = df

        self.filter_df = df.reset_index(drop=True)

        return fig

    def update_df(self, name, dept, salary):
        index = 0
        for i in self.df['name']:
            if i == name:
                break
            index += 1
        self.df.loc[index, 'salary'] = salary
        self.df.loc[index, 'department'] = dept
        df = self.df

        if self.filter_df is not None:

            index = 0
            for i in self.filter_df['name']:
                if i == name:
                    break
                index += 1
            self.filter_df.loc[index, 'salary'] = salary
            self.filter_df.loc[index, 'department'] = dept
            df = self.filter_df
        fig = self.fig
        fig.data[0].x = df['x']
        fig.data[0].y = df['y']
        fig.data[0].marker.size = df['salary']
        fig.data[0].customdata = df
        # print(fig.to_dict())
        return fig


data = data_processing()

fig = data.create_empty_graph()
graph = dcc.Graph(figure=fig, id='graph')
input_min = dcc.Input(id='min', type='number', min=2000, max=2030, value=2018)
input_max = dcc.Input(id='max', type='number', min=2000, max=2030, value=2030)
side_bar = [html.H1('Input min year'), input_min,
            html.H1('Input max year'), input_max]
upload_button = html.Button(id='upload', children='Upload', n_clicks=0)
filter_div = html.Div(side_bar, id='sidebar', style={'visibility': 'hidden'})

td1 = html.Td([upload_button, filter_div])
td2_style = {
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
                'display': 'none'}, children='Hello')
td2 = html.Td(children=[tab, div1, div2], style=td2_style)
tr = html.Tr([td1, td2])

table_style = {
    # 'height':'70%',
    'width': '100%',
    # 'position': 'absolute',
    'top': '0',
    'bottom': '0',
    'left': '0',
    'right': '0',
}
table = html.Table(children=tr, style=table_style)
name = dcc.Input(id='name')
dept = dcc.Input(id='dept')
salary = dcc.Input(id='salary', type='number')
button = html.Button(id='button', children='Submit', n_clicks=0)
click_div = html.Div(children=[name, dept, salary, button], style={
                     'display': 'none'}, id='answer')
main_div = [table, click_div]


@callback(Output(component_id='tab_gv_output', component_property='style'),
          Output(component_id='tab_dv_output', component_property='style'),
          Input(component_id='tab', component_property='value'),
          prevent_initial_call=True)
def tab_switch(tab):
    if tab == 'gv':
        return [{}, {'display': 'none'}]
    if tab == 'dv':
        return [{'display': 'none'}, {}]


@callback(Output(component_id='graph', component_property='figure'),
          Output(component_id='answer',
                 component_property='style', allow_duplicate=True),
          Output(component_id='sidebar', component_property='style'),
          Input(component_id='upload', component_property='n_clicks'),
          Input(component_id='min', component_property='value'),
          Input(component_id='max', component_property='value'),
          Input('button', 'n_clicks'),
          State('dept', 'value'),
          State('salary', 'value'),
          State('name', 'value'),
          prevent_initial_call=True)
def update(upload, min_val, max_val, button, dept, salary, name):
    trig_id = ctx.triggered_id
    if trig_id == 'upload':
        fig = data.create_mst_graph()
        return [fig, {'display': 'none'}, {}]

    if trig_id == 'max' or trig_id == 'min':
        return [data.update_graph([min_val, max_val]), {'display': 'none'}, {}]
    else:
        return [data.update_df(name, dept, salary), {'display': 'none'}, {}]


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
