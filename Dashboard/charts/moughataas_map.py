import pandas as pd
import plotly.graph_objects as go

def InfoMoughataas(gj) :
    # Création d'une table reprenant le taux d'insécurité alimenataire,
    # le nombre d'habitants et le nombre de ménages par Moughataas
    taux_ia = [gj['features'][i]['properties']['taux_IA'] for i in range(len(gj['features']))]
    n_pop = [gj['features'][i]['properties']['n_pop'] for i in range(len(gj['features']))]
    n_hh = [gj['features'][i]['properties']['n_hh'] for i in range(len(gj['features']))]
    info_moughataas = pd.DataFrame([taux_ia, n_pop, n_hh]).T.rename(columns={0:'taux_ia', 1:'n_pop', 2:'n_hh'})
    return(info_moughataas)

def MoughataasMap(gj, df, valueInf, valueSup) : 
    #Color map sur mesure créée avec https://vis4.net/palettes/
    custom_cmap = ['#ffffff', '#fffdfd', '#fffbfb', '#fff9f9', '#fff7f7', '#fff5f4', '#fff3f2', '#fff1f0', 
                   '#ffefee', '#ffedec', '#ffebea', '#ffe9e8',  '#ffe7e6', '#ffe5e4', '#ffe3e1', '#ffe1df', 
                   '#ffdfdd', '#ffdddb', '#ffdbd9', '#ffd9d7',  '#ffd7d5', '#ffd5d3', '#ffd3d0', '#ffd1ce', 
                   '#ffcfcc', '#ffcdca', '#ffcbc8', '#ffc9c6', '#ffc7c4', '#ffc5c2', '#ffc3c0', '#ffc1bd',
                   '#ffbfbb', '#ffbcb9', '#ffbab7', '#ffb8b5', '#ffb6b3', '#feb4b1', '#feb2af', '#feb0ad', 
                   '#feaeab', '#fdaca9', '#fdaaa7', '#fda8a5','#fca6a3', '#fca4a1', '#fca29f', '#fba09d', 
                   '#fb9e9b', '#fb9c99', '#fa9a97', '#fa9795','#f99593', '#f99391', '#f9918f', '#f88f8d',
                   '#f88d8b', '#f78b89', '#f78987', '#f68785', '#f68483', '#f58281', '#f5807f', '#f47e7d', 
                   '#f47c7b', '#f37a79', '#f37778', '#f27576','#f27374', '#f17172', '#f16f70', '#f06c6e',
                   '#ef6a6c', '#ef686a', '#ee6568', '#ed6367', '#ed6165', '#ec5e63', '#ec5c61', '#eb595f', 
                   '#ea575d', '#ea545c', '#e9525a', '#e84f58','#e74c56', '#e74a54', '#e64753', '#e54451', 
                   '#e5414f', '#e43e4d', '#e33b4c', '#e2384a', '#e23548', '#e13146', '#e02d45', '#df2943',
                   '#de2541', '#de203f', '#dd1b3e', '#dc143c'
                  ]

    # Carte représentant le taux d'insécurité par Moughataas
    fig = go.Figure(go.Choroplethmapbox(geojson=gj, 
                                        locations=df.index, 
                                        featureidkey='properties.ID_2',
                                        z=df['taux_ia'],
                                        colorscale=custom_cmap, 
                                        zmin=valueInf, zmax=valueSup, 
                                        marker_line_width=0,
                                        colorbar=dict(outlinecolor='white'),
                                        customdata = df, 
                                        hovertemplate="<br>".join([
                                                "Taux IA: %{customdata[0]:.1%}",
                                                "Population: %{customdata[1]}",
                                                "Foyers: %{customdata[2]}"])
                                       )
                                       
                   )

    # Mise en forme
    fig.update_traces(marker={'line': {'color': 'white', 'width': 1.15}}) # Faire apparaître les frontières en blanc
    fig.update_layout(mapbox_style='white-bg', # Projeter la carte sans faire apparaître les pays voisins
                      mapbox_zoom=4.7, # Taille de la carte projetée
                      mapbox_center = {'lat': 21, 'lon': -10}, # Centrer la carte
                      margin={'r':0,'t':0,'l':0,'b':0} # Marges de la figure
                     )

    # fig.show()
    return(fig)
