import pandas as pd

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