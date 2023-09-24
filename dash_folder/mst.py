import pandas as pd
import nltk # type: ignore
import numpy as np
from scipy import sparse
from scipy.sparse.csgraph import minimum_spanning_tree
import plotly.express as px


class data_processing:
    # this class be used to work with data

    def __init__(self):
        # this method creates dummy data when there is no dataframe

        dict1 = {'name': ['Ayan', 'Ram', 'Shyam', 'Jodu', 'Modu'],
                 'department': ['', '', '', '', ''],
                 'doj': ['10/2/2021', '4/23/2023', '8/8/2021', '2/15/2019', '2/2/2020'],
                 'salary': [1000, 200, 300, 500, 600],
                 'edited': [False, False, False, False, False]}

        self.df = pd.DataFrame(dict1)
        self.df['doj'] = pd.to_datetime(self.df.doj, format='%m/%d/%Y')
        self.mat = None
        # self.filter_df = None
        self.fig = None

    def _init_(self, df):
        # this method accepts the dataframe if its given
        self.df = df
        self.mat = None
        # self.filter_df = None
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

    def create_graph(self, df):
        # create a graph from a dataframe

        if self.fig is None:
            hover_dict = {}
            for i in self.df.columns:
                if i == 'x' or i == 'y' or i == 'edited':
                    hover_dict[i] = False
                else:
                    hover_dict[i] = True

            fig = px.scatter(self.df, x='x', y='y', size='salary',
                             hover_data=hover_dict)
            fig.update_yaxes(tickmode='linear', tick0=0, dtick=1)
            fig.update_xaxes(tickmode='linear', tick0=0, dtick=1)
            fig.update_layout(title_text='Sample Dataset')
            fig.update_traces(marker=dict(color='green'))
            self.fig = fig

        else:
            fig = self.fig
            fig.data[0].x = df['x']
            fig.data[0].y = df['y']
            fig.data[0].marker.size = df['salary']
            fig.data[0].customdata = df
            arr = ['blue' if i else 'green' for i in df['edited']]
            fig.update_traces(marker=dict(color=arr))
        return fig

    def create_mst_graph(self):
        # creates the mst graph in plotly

        # if self.fig is not None:
        #     return self.fig
        mat = self.mst()
        dict1 = self.__create_coord_dict(mat)
        for i in dict1:
            self.df.loc[i, 'x'] = dict1[i][0]
            self.df.loc[i, 'y'] = dict1[i][1]

        return self.create_graph(self.df)

    def update_graph(self, arr):
        # updates the graph based on the condition

        df = self.df[(self.df['doj'].dt.year >= arr[0])
                     & (self.df['doj'].dt.year <= arr[1])]

        filter_df = df.reset_index(drop=True)
        return filter_df, self.create_graph(filter_df)
        # return self.create_graph(self.filter_df)

    def update_df(self, name, dept, salary):
        index = 0
        for i in self.df['name']:
            if i == name:
                break
            index += 1
        self.df.loc[index, 'salary'] = salary
        self.df.loc[index, 'department'] = dept
        self.df.loc[index, 'edited'] = True
        df = self.df
        return self.create_graph(df)

if __name__ == '__main__':
    data = data_processing()
    data.create_mst_graph()
    df, _ = data.update_graph([2018, 2022])

    print(df)