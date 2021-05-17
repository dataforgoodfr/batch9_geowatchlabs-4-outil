import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.express as px

def InfoMoughataas(gj) :
    # Création d'une table reprenant le taux d'insécurité alimenataire,
    # le nombre d'habitants et le nombre de ménages par Moughataas
    info_moughataas = pd.DataFrame()
    info_moughataas['nom'] = [gj['features'][i]['properties']['NAME_2'] for i in range(len(gj['features']))]
    info_moughataas['taux_ia'] = [gj['features'][i]['properties']['taux_IA'] for i in range(len(gj['features']))]
    info_moughataas['n_pop'] = [gj['features'][i]['properties']['n_pop'] for i in range(len(gj['features']))]
    info_moughataas['n_hh'] = [gj['features'][i]['properties']['n_hh'] for i in range(len(gj['features']))]
    
    # Résolution du problème d'encodage des lettres avec accent
    info_moughataas['nom'] = [name.encode("latin_1").decode("utf_8") for name in info_moughataas['nom']]
    return(info_moughataas)

def MoughataasMap(gj, df, tauxIA) : 
    # Ajout d'une colonne mentionnant l'intervalle d'insécurité alimenatire 
    # dans lequel chaque zone se trouvent. Le but est de pouvoir ensuite colorer 
    # les zones par rapport à leur intervalle respectif.
    df['filter_taux_ia'] = df['taux_ia']
    df.loc[(df['filter_taux_ia'] < tauxIA)] = 0
    df.loc[(df.filter_taux_ia==0), 'intervalles'] = 'Hors périmètre'
    df.loc[(df.filter_taux_ia>0)&(df.filter_taux_ia<0.05), 'intervalles'] = '0-5%'
    df.loc[(df.filter_taux_ia>=0.05)&(df.filter_taux_ia<0.10), 'intervalles'] = '5-10%'
    df.loc[(df.filter_taux_ia>=0.10)&(df.filter_taux_ia<0.20), 'intervalles'] = '10-20%'
    df.loc[(df.filter_taux_ia>=0.20)&(df.filter_taux_ia<0.30), 'intervalles'] = '20-30%'
    df.loc[(df.filter_taux_ia>=0.30)&(df.filter_taux_ia<0.40), 'intervalles'] = '30-40%'
    df.loc[(df.filter_taux_ia>=0.40), 'intervalles'] = '> 40%'

    # Color Map : dictionnaire permettat d'attribuer à chaque catégorie une couleur spécifique 
    color_map={
                "Hors périmètre": "#f1f1f1",
                "0-5%": "#024B1A",
                "5-10%": "#A2BF05",
                "10-20%": "#FAE147",
                "20-30%": "#FAA94B",
                "30-40%" : "#F16C54",
                "> 40%" : "#D21E42"}

    # Tri de la dataframe du plus petit au plus grand de sorte à ce que 
    # l'ordre des seuils corresponde à l'ordre des couleurs dans 'colorscales'
    df = df.sort_values('intervalles')

    # Mise en forme des valeurs 'nombre de d'habitants' et 'nombre de ménages'.
    # Utilisation de l'espace comme séparateur de milliers.
    df.n_pop = ['{:,.0f}'.format(v).replace(',',' ') for v in df.n_pop]
    df.n_hh = ['{:,.0f}'.format(v).replace(',',' ') for v in df.n_hh]


    # Carte représentant le taux d'insécurité par Moughataas.
    fig = px.choropleth_mapbox(geojson=gj, 
                                        locations=df.index, 
                                        featureidkey='properties.ID_2',
                                        color=df['intervalles'],
                                        color_discrete_map= color_map
    )
                                       
    # Mise en forme de la carte
    fig.update_traces(marker={'line': {'color': 'white', 'width': 1.15}}, 
                customdata = df,
                hovertemplate= "<br>".join([
                            "<b>%{customdata[0]}</b>",
                            "Taux IA: %{customdata[1]:.1%}",
                            "Population: %{customdata[2]}",
                            "Foyers: %{customdata[3]}",
                            "<extra></extra>"]),
                hoverlabel=dict(bgcolor='#000066')) # Couleur de fond du hover
    fig.update_layout(mapbox_style='white-bg', # Projeter la carte sans faire apparaître les pays voisins
                      mapbox_zoom=4.7, # Taille de la carte projetée
                      mapbox_center = {'lat': 21, 'lon': -10}, # Centrer la carte
                      margin={'r':0,'t':0,'l':0,'b':0}, # Marges de la figure
                     )
    return(fig)