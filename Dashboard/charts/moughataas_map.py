import plotly.graph_objects as go
import plotly.express as px

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
    
    fig.update_layout(height=800,
                      margin={"r":0,"t":80,"l":0,"b":0},
                      title={'text': "Taux d'insécurité alimentaire par Moughataa",
                             'x': 0.5,
                             'y': 0.98,
                             'font_size': 24
                            },
                      title_pad={'t': 10},
                      legend_title_text=None ,
                      legend=dict(orientation='h',
                                  yanchor='top',
                                  y=1.05,
                                  xanchor='center',
                                  x=0.5, 
                                  font=dict(size=14)
                                 ),
                      geo=dict(scope='africa',
                               projection={'type': 'equirectangular'},
                               fitbounds='geojson',
                               bgcolor='white', 
                               visible=False),
                      paper_bgcolor='white',                      
                      modebar=dict(orientation='v',
                                   color= 'white',
                                   bgcolor='#000066')
                     )
    
    #fig.update_geos(fitbounds='locations', visible=False)

    return(fig)