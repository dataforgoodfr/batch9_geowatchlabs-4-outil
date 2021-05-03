# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
from charts.mapRepresentation import MapRepresentation

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.DataFrame({
    "x": [1,2,1,2],
    "y": [1,2,3,4],
    "year" : [2011, 2011, 2011, 2012],
    "customdata": [1,2,3,4],
    "fruit": ["apple", "apple", "orange", "orange"]
})
# df = pd.read_json('Dashboard/data/data2020.json')

fig = MapRepresentation(df)

app.layout = html.Div([
    html.H1("Appli GeoWatch Labs", style= {'text-align' : 'center', 'margin-bottom' : '40px'}),
    html.H6("Choix de l'année", style = {'margin-bottom' : '20px'}),
    dcc.RadioItems(id='yearChoice',
    options=[
        {'label': 'Année 2010', 'value': 2010},
        {'label': 'Année 2011', 'value': 2011},
        {'label': 'Année 2012', 'value': 2012},
        {'label': 'Année 2013', 'value': 2013},
        {'label': 'Année 2014', 'value': 2014}
    ],
    value='2011',
    labelStyle={'display': 'inline-block'}, style = {'margin-bottom' : '20px'}
) ,

    html.H6("Taux d'insécurité alimentaire", style = {'margin-bottom' : '20px'}),
    dcc.RangeSlider(
    marks = {i: '{}'.format(round(i, 2)) for i in np.arange(0, 1, 0.05)}, 
    min=0.,
    max=1.,
    value=[0., 1.]
), 

    dcc.Graph(
        id='graph-with-year'
    )
])

@app.callback(
    Output('graph-with-year', 'figure'),
    Input('yearChoice', 'value'))
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]
    return MapRepresentation(filtered_df)

if __name__ == '__main__':
    app.run_server(debug=True)