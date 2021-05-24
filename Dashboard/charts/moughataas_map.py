import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.express as px

def InfoMoughataas(gj) :
    # Création d'une table reprenant le taux d'insécurité alimenataire,
    # le nombre d'habitants et le nombre de ménages par Moughataas
    df = pd.DataFrame()
    df['nom'] = [gj['features'][i]['properties']['NAME_2'] for i in range(len(gj['features']))]
    df['taux_ia'] = [gj['features'][i]['properties']['taux_IA'] for i in range(len(gj['features']))]
    df['n_pop'] = [gj['features'][i]['properties']['n_pop'] for i in range(len(gj['features']))]
    df['n_hh'] = [gj['features'][i]['properties']['n_hh'] for i in range(len(gj['features']))]
    
    # Ajout d'une colonne mentionnant l'intervalle d'insécurité alimenatire 
    # dans lequel chaque zone se trouvent. Le but est de pouvoir ensuite colorer 
    # les zones par rapport à leur intervalle respectif.
    df.loc[(df.taux_ia>0)&(df.taux_ia<0.05), 'intervalles'] = '0-5%'
    df.loc[(df.taux_ia>=0.05)&(df.taux_ia<0.10), 'intervalles'] = '5-10%'
    df.loc[(df.taux_ia>=0.10)&(df.taux_ia<0.20), 'intervalles'] = '10-20%'
    df.loc[(df.taux_ia>=0.20)&(df.taux_ia<0.30), 'intervalles'] = '20-30%'
    df.loc[(df.taux_ia>=0.30)&(df.taux_ia<0.40), 'intervalles'] = '30-40%'
    df.loc[(df.taux_ia>=0.40), 'intervalles'] = '> 40%'
    
    # Résolution du problème d'encodage des lettres avec accent
    #df['nom'] = [name.encode("latin_1").decode("utf_8") for name in df['nom']]
    return(df)

def MoughataasMap(gj, df, tauxIA) :    
    # Filtre de la df par rapport au taux d'IA défini
    df.loc[df.taux_ia < tauxIA, 'intervalles'] = 'Hors périmètre'

    # Color Map : dictionnaire permettant d'attribuer à chaque catégorie une couleur spécifique 
    color_map = {'Hors périmètre': '#333333',
                 '0-5%': '#024B1A',
                 '5-10%': '#A2BF05',
                 '10-20%': '#FAE147',
                 '20-30%': '#FAA94B',
                 '30-40%' : '#F16C54',
                 '> 40%' : '#D21E42'
                }

    # Mise en forme des valeurs 'nombre d'habitants' et 'nombre de ménages'.
    # Utilisation de l'espace comme séparateur de milliers.
    df.n_pop = ['{:,.0f}'.format(v).replace(',',' ') for v in df.n_pop]
    df.n_hh = ['{:,.0f}'.format(v).replace(',',' ') for v in df.n_hh]


    # Carte représentant le taux d'insécurité par Moughataas
    fig = px.choropleth(geojson=gj, 
                        locations=df['nom'], 
                        featureidkey='properties.NAME_2',
                        color=df['intervalles'],
                        category_orders={'intervalles': ['Hors périmètre',
                                                         '0-5%',
                                                         '5-10%',
                                                         '10-20%',
                                                         '20-30%',
                                                         '30-40%',
                                                         '> 40%'
                                                        ]
                                        },
                        color_discrete_map=color_map,      
                        data_frame=df,
                        custom_data=['nom', 'taux_ia', 'n_pop', 'n_hh']
                       )
                                       
    # Mise en forme de la carte
    fig.update_traces(marker={'line': {'color': 'white', 'width': 1.15}},
                      hovertemplate= "<br>".join(["<b>%{customdata[0]}</b>",
                                                  "Taux IA: %{customdata[1]:.1%}",
                                                  "Population: %{customdata[2]}",
                                                  "Foyers: %{customdata[3]}",
                                                  "<extra></extra>"
                                                 ]
                                                ),
                      hoverlabel=dict(bgcolor='#000066')) # Couleur de fond du hover
    
    fig.update_layout(margin=dict(r=0, t=0, l=0, b=0), # Supression des marges de la figure
                      legend_title_text=None ,
                      legend=dict(orientation='h',
                                  yanchor='middle',
                                  y=-0.05,
                                  xanchor='center',
                                  x=0.5
                                 ),
                      geo=dict(bgcolor='#f0f2f4'),
                      paper_bgcolor='white'
                     )
    
    fig.update_geos(fitbounds='locations', visible=False)

    return(fig)