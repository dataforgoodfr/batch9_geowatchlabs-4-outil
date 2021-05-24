# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_daq as daq
import dash_daq as daq
from charts.moughataas_map import  MoughataasMap
from charts.pop_donutchart import PopDonutChart
from utils.loadGeojson import LoadGeojson
from utils.readInfoMoughataas import InfoMoughataas

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
    dcc.Tabs( id = 'tabs', value = '1', children=
                [
                    dcc.Tab(label="Pays",  value = 'pays', style = {'display': 'flex'},
                    children= [ 
                                html.Div(style = {'margin-bottom' : '60px'}, 
                                    children = dcc.Graph (figure = PopDonutChart(info_moughataas))),
                                html.Div(
                                style={'width': '30%', 'float' : 'left', 'text-align' : 'center', 'padding-top' : '50px'},
                                children= [
                                html.H3( "Taux d'insécurité alimentaire limite"),
                                html.Div(style = {'margin' : 'auto', 'margin-top' : '50px', 'margin-bottom' : '60px'}, 
                                        children=[daq.Slider(id = 'iaThreshold', min=0, max=1, value=0.2, handleLabel={"showCurrentValue": True,"label": "IA"},step = 0.01)]),
                                html.H3('Population'),
                                html.Div(style = {'font-size' : '25px', 'margin-bottom': '60px'}, id= 'population'),
                                html.H3('Foyers'),
                                html.Div(style = {'font-size' : '25px'}, id='foyers')]),
                        html.Div( 
                            style = {'width' : '70%', 'float': 'right', 'padding-top' : '50px'},
                            children= [dcc.Graph(id ='graph1')])
                            ]),
                    dcc.Tab(label="Moughataas", value = 'region', children= [
                        dcc.Dropdown(id="dropdownRegions"), 
                        html.Div ( id= 'graph2')
                        ])],
                    )
                ])

@app.callback(
    Output('graph1', 'figure'),
    Output('population', 'children'),
    Output('foyers', 'children'),
    Output('dropdownRegions', 'options'),
    [Input('iaThreshold', 'value')])
def update_figure(value):
    df = info_moughataas.copy()
    df_filtered = df.loc[df.taux_ia> value, ['n_pop', 'n_hh']]
    pop = df_filtered.n_pop.sum()
    foy= df_filtered.n_hh.sum()
    opt = [{'label': i, 'value': i} for i in df.loc[df.taux_ia > value, 'nom'].sort_values()]
    return MoughataasMap(gj= GJ, df=df, tauxIA = value), '{:,.0f}'.format(pop), '{:,.0f}'.format(foy), opt

@app.callback(
    Output('graph2', 'children'),
    Output('tabs', 'value'),
    Output('dropdownRegions', 'value'),
    [Input('graph1', 'clickData'), 
    Input('graph2', 'children'), 
    Input('dropdownRegions', 'value')])
def update_map(clickData, children, value):    
    if clickData is not None:            
        location = clickData['points'][0]['location']
        if children == location : 
            location = value
        tab = 'region'
    elif value is not None : 
        tab = 'region'
        location= value
    else : 
        location = 'pas de location'
        tab = 'pays'
    return location, tab, location





if __name__ == '__main__':
    app.run_server(debug=True)