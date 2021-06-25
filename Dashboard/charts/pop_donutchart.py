import pandas as pd
import numpy as np
import plotly.graph_objects as go

def PopDonutChart(df):

    # Calcul du nombre d'habitants et nombre de ménages touchés suivant les seuils d'IA
    pop_total = df['n_pop'].sum()
    intervals_to_plot = df.sort_values('taux_ia', ascending=False).intervalles.unique()
    pop_sum = [df.loc[df.intervalles==i, 'n_pop'].sum() for i in intervals_to_plot]
    menages_sum = [df.loc[df.intervalles==i, 'n_hh'].sum() for i in intervals_to_plot]

    # Definition des variables servant à dessiner le graph
    values = pop_sum
    labels = intervals_to_plot
    color_map = {'Hors périmètre': '#333333',
                 '0-5%': '#024B1A',
                 '5-10%': '#A2BF05',
                 '10-20%': '#FAE147',
                 '20-30%': '#FAA94B',
                 '30-40%' : '#F16C54',
                 '> 40%' : '#D21E42'
                }
    colors = [color_map[i] for i in intervals_to_plot]

    # Création d'une dataframe permettant d'enrichir le hover
    customdata = pd.DataFrame()
    customdata[0] = ['{:,.0f}'.format(v).replace(',', ' ') for v in pop_sum]
    customdata[1] = ['{:,.0f}'.format(v).replace(',', ' ') for v in menages_sum]

    fig = go.Figure(data=[go.Pie(labels=labels,
                                 values=values, 
                                 hole=0.55, 
                                 sort=False,
                                 insidetextorientation='horizontal',
                                 customdata=customdata,
                                 # Particularité de go.Pie, 
                                 # il faut spécifier 2 positions pour customdata (customdata[0][0]) 
                                 # au lieu d'une en général (customdata[0])
                                 hovertemplate = 
                                 'Population: %{customdata[0][0]}<br>'+ 
                                 'Nombre de ménages: %{customdata[0][1]}'+
                                 '<extra></extra>',
                                 hoverlabel=dict(bgcolor='#000066'),marker_colors=colors, 
                                 marker={'line': {'color': 'white',
                                                  'width': 1.15
                                                 }
                                        }
                                )
                         ]
                   )

    # Mise en forme
    fig.update_layout(height=600,
                      margin=dict(r=0, t=125, l=0, b=50), # Ajustement des marges
                      title={'text': "Population touchée par seuil",
                             'x': 0.5,
                             'y': 0.98,
                             'font_size': 24
                            },
                      title_pad={'t': 10},
                      # Positionnement de la légende
                      legend=dict(orientation='h',
                                  yanchor='top',
                                  y=1.15,
                                  xanchor='center',
                                  x=0.5, 
                                  font=dict(size=14)
                                 ),
                      paper_bgcolor='white',
                      modebar=dict(orientation='v',
                                   color= 'white',
                                   bgcolor='#000066')
                     )

    # Amélioration de la qualité d'image
    #config = {'toImageButtonOptions': {'scale': 3}}

    # return fig.show(config=config)
    return fig