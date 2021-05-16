# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
from charts.moughataas_map import InfoMoughataas, MoughataasMap
from utils.loadGeojson import LoadGeojson
from charts.mapRepresentation import MapRepresentation

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

GJ = LoadGeojson('Dashboard/data/Moughataas_new.geojson')
info_moughataas = InfoMoughataas(GJ)
variable = 'text'

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
        dcc.Tabs( id = 'tabs', value = '1', children=
                [
                    dcc.Tab(label="Pays",  value = '1', children= [ dcc.Graph(id ='graph1')]),
                    dcc.Tab(label="Moughataas", value = '2', children= [html.Div ( id= 'graph2')])],
            )
])

@app.callback(
    Output('graph1', 'figure'),
    [Input('iaThreshold', 'value')])
def update_figure(value):
    MoughataasMap(gj= GJ, df=info_moughataas, valueInf= value[0]/10, valueSup=value[1]/10)
    return MoughataasMap(gj= GJ, df=info_moughataas, valueInf= value[0]/10, valueSup=value[1]/10)

@app.callback(
    Output('graph2', 'children'),
    Output('tabs', 'value'),
    [Input('graph1', 'clickData')])
def update_map(clickData):    
    if clickData is not None:            
        location = clickData['points'][0]['location']
        location = info_moughataas.loc[location, 'name']
        tab = '2'
    else : 
        location = 'pas de location'
        tab = '1'
    return location, tab

if __name__ == '__main__':
    app.run_server(debug=True)