# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
# from charts.mapRepresentation import MapRepresentation
from charts.moughataas_map import InfoMoughataas, MoughataasMap
from utils.loadGeojson import LoadGeojson

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

GJ = LoadGeojson('Dashboard/data/Moughataas_new.geojson')
info_moughataas = InfoMoughataas(GJ)

app.layout = html.Div([
    html.H1("Appli GeoWatch Labs", style= {'text-align' : 'center', 'margin-bottom' : '40px'}),
    html.H6("Choix de l'année", style = {'margin-bottom' : '20px'}),
    dcc.Dropdown(id='yearChoice',
    options=[
        {'label': 'Année 2010', 'value': 2010},
        {'label': 'Année 2011', 'value': 2011},
        {'label': 'Année 2012', 'value': 2012},
        {'label': 'Année 2013', 'value': 2013},
        {'label': 'Année 2014', 'value': 2014}
    ],
    value='2011',
    style = {'margin-bottom' : '20px'}
) ,

    html.H6("Taux d'insécurité alimentaire", style = {'margin-bottom' : '20px'}),
    dcc.RangeSlider( id ='iaThreshold',
    marks = {i: '{}'.format(i/10) for i in range(1,10)}, 
    step= 0.05,
    min=0.,
    max=10,
    value=[0, 10]
), 

    dcc.Graph(
        id='graph-with-year'
    )
])

@app.callback(
    Output('graph-with-year', 'figure'),
    [Input('iaThreshold', 'value')])
def update_figure(value):
    # filtered_info_moughataas = FilterMoughatas(info_moughataas, 0.3, 0.7)
    # filtered_df = df[df.year == selected_year]
    return MoughataasMap(gj= GJ, df=info_moughataas, valueInf= value[0]/10, valueSup=value[1]/10)
    # return moughataas_map('Dashboard/data/Moughataas_new.geojson')

if __name__ == '__main__':
    app.run_server(debug=True)