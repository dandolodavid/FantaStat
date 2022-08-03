from cProfile import run
import pandas as pd
import numpy as np

def all_status() :
    return ['Titolare', 'Entrato', 'Infortunato', 'Squalificato', 'Inutilizzato']

def info_extraction(data, nome, stagione):
    '''
    '''

    ruolo = data['Ruolo'].unique()[0]
    
    data.Voto = data.Voto.apply(lambda x: str(x).replace('-','0')).astype(float)
    data.FV = data.FV.apply(lambda x: str(x).replace('-','0')).astype(float)
    data.Entrato = data.Entrato.fillna(0).apply(lambda x: str(x).split('-')[0]).astype(float)
    data.Uscito = data.Uscito.fillna(0).apply(lambda x: str(x).split('-')[0]).astype(float)
    
    data['Nome'] = nome
    data['Stagione'] = stagione

    if ruolo != 'P':
        data['Bonus'] = data['Gf'] * 3 + data['Ass']
        data['Malus'] = data['Amm'] * 0.5 + data['Esp'] * 1
    else:
        data['Bonus'] = data['Rp'] * 3 
        data['Malus'] = data['Amm'] * 0.5 + data['Esp'] * 1 + data['Gs']

    data['ha_voto'] = data['Voto']>0
    data['ha_bonus'] = data['Bonus']>0
    data['ha_malus'] = data['Malus']>0
    
    try:
        data['ha_sostituzione'] = data['Uscito'] > 0
    except:
        data['ha_sostituzione'] = data['Uscito'] > 0
        
    data['ha_entrata'] = (data.Status == 'Entrato')

    data['Minuti'] =  data['Uscito'] - data['Entrato']
    data.loc[data['Minuti']<0, 'Minuti'] = np.repeat( 90, len(data) ) - data['Entrato']
    data.loc[np.logical_and(data['Minuti']==0, data.Voto>0), 'Minuti'] = 90

    info = pd.DataFrame(pd.concat( [pd.DataFrame(data.Status.value_counts()).T, pd.DataFrame(data[['Gf','Ass','Rc','R+','Amm','Esp','Gs','Rp','Minuti']].sum()).T] ).sum()).T
        
    for status in all_status():
        if status not in info.columns:
            info[status] = 0
    
    info = info[['Gf','Ass','Rc','R+','Amm','Esp','Gs','Rp','Minuti'] + all_status()]
    
    info['Presenza'] = info['Titolare'] + info['Entrato']

    info['Nome'] = nome
    info['Stagione'] = stagione
    info['Ruolo'] = ruolo
    info['Squadra'] = data['Squadra'].unique()[0]
    info['Id'] = data['Id'].unique()[0]

    info['Bonus'] = data['Bonus'].sum()
    info['Malus'] = data['Malus'].sum()

    info['partite_bonus'] = data['ha_bonus'].sum()
    info['partite_malus'] = data['ha_malus'].sum()
    info['partite_voto'] = data['ha_voto'].sum()
    
    if info['Presenza'].values>0:
        info['minuti_medi'] = data['Minuti'].sum()/info['Presenza']
    else:
        info['minuti_medi'] = 0
        
    info['sostituito'] = data['ha_sostituzione'].sum()

    info['%_con_voto'] = data['ha_voto'].mean()*100
    info['%_bonus'] = data['ha_bonus'].mean()*100
    info['%_malus'] = data['ha_malus'].mean()*100
    info['%_sostituito'] = data['ha_sostituzione'].mean()*100
    info['%_subentrato'] = data['ha_entrata'].mean()*100
    
    info['Gol 90'] = info['Gf']/info['Presenza']
    info['Gol subiti 90'] = info['Gs']/info['Presenza']

    # solo dati con voto per le medie voto
    data_con_voto = data.loc[data.ha_voto]
    
    info['mediana_voto'] = data_con_voto['Voto'].median()
    info['media_voto'] = data_con_voto['Voto'].mean()
    info['mediana_fantavoto'] = data_con_voto['FV'].median()
    info['media_fantavoto'] = data_con_voto['FV'].mean()
    
    info['%_voto_<_5'] = (data_con_voto.Voto <= 5).mean()*100
    info['%_voto_5_6'] = np.logical_and(data_con_voto.Voto > 5, data_con_voto.Voto < 6).mean()*100
    info['%_voto_6_7'] = np.logical_and(data_con_voto.Voto >= 6, data_con_voto.Voto < 7).mean()*100
    info['%_voto_7_8'] = np.logical_and(data_con_voto.Voto >= 7, data_con_voto.Voto < 8).mean()*100
    info['%_voto_>_8'] = (data_con_voto.Voto >= 8).mean()*100

    info['%_fv_5'] = (data_con_voto.FV <= 5).mean()*100
    info['%_fv_5_6'] = np.logical_and(data_con_voto.FV > 5, data_con_voto.FV < 6).mean()*100
    info['%_fv_6_7'] = np.logical_and(data_con_voto.FV >= 6, data_con_voto.FV < 7).mean()*100
    info['%_fv_7_8'] = np.logical_and(data_con_voto.FV >= 7, data_con_voto.FV < 8).mean()*100
    info['%_fv_>_8'] = (data_con_voto.FV >= 8).mean()*100

    info = info.rename(columns={'Gf':'Gol',
                    'Ass':'Assist',
                    'Gs':'Gol subiti',
                    'Rp':'Rigori parati',
                    'Rc':'Rigori calciati',
                    'R+':'Rigori segnati',
                    'Amm':'Ammonizioni',
                    'Esp':'Espulsioni'
                    })
    
    info = np.round(info,2)
    
    return info, data


def normalize(df):
    
    for c in df.columns:
        df[c] = (df[c] - df[c].min()) /  (df[c].max() - df[c].min())
    
    return df

def appetibility_index(history_original, dixon_coles, player_info):
    '''
    '''   
    
    ### score per vedere se segna contro squadre "semplici"
    gestione_semplice_score = history_original.copy()
    gestione_semplice_score.Squadra = gestione_semplice_score.Squadra.apply(lambda x: x.upper()[0:3])
    
    gestione_semplice_score['Against'] = gestione_semplice_score.apply(lambda x: x['Partita'].replace('-','').replace(x['Squadra'],''), axis = 1)
    gestione_semplice_score.Against = gestione_semplice_score.Against.apply(lambda x: x.strip())

    gestione_semplice_score = gestione_semplice_score[['Nome','Squadra','Against','Gf']].merge(dixon_coles, left_on = 'Squadra', right_on='name').drop(columns = 'name').rename(columns={'Atk_Params':'player_atk_params','Def_Params':'player_def_params'})
    gestione_semplice_score = gestione_semplice_score.merge(dixon_coles, left_on = 'Against', right_on='name').drop(columns = 'name').rename(columns={'Atk_Params':'against_atk_params','Def_Params':'against_def_params'})
    gestione_semplice_score = gestione_semplice_score.drop_duplicates()
    
    # segnare contro una squadra con difesa scarsa è meglio
    easy_gambe_bonus = (-gestione_semplice_score['against_def_params'])*(gestione_semplice_score['Gf']>0)
    easy_gambe_bonus = (easy_gambe_bonus - easy_gambe_bonus.min())/(easy_gambe_bonus.max() - easy_gambe_bonus.min())
    gestione_semplice_score['easy_gambe_bonus'] = easy_gambe_bonus
    easy_gambe_bonus = gestione_semplice_score.groupby('Nome').mean()[['easy_gambe_bonus']]
    propensity_bonus_easy_game = easy_gambe_bonus.sort_values('easy_gambe_bonus',ascending=False)
    
    ### score propensità al cartellino giallo, rosso, avere bonus e avere voto
    bonus_malus_voto_propensity = history_original.groupby('Nome')[['Amm','Esp','ha_bonus','ha_voto']].mean()
    bonus_malus_voto_propensity = normalize(bonus_malus_voto_propensity)
    
    ### infortunio propensity
    infortunio_propensity = history_original.groupby(['Nome','Status']).count().reset_index()
    infortunio_propensity = infortunio_propensity.loc[infortunio_propensity.Status=='Infortunato'].set_index('Nome').rename(columns={'Giornata':'Infortunato'})[['Infortunato']]
    infortunio_propensity = normalize(infortunio_propensity)
    
    ### gol subito propensity
    ha_gol_subito = history_original[['Nome','Gs']]
    ha_gol_subito['Gs'] = (ha_gol_subito['Gs']>0)
    ha_gol_subito = ha_gol_subito.groupby('Nome').mean()[['Gs']]
    
    
    propensity_df = pd.concat([propensity_bonus_easy_game, bonus_malus_voto_propensity, infortunio_propensity, ha_gol_subito],axis=1)
    propensity_df['Infortunato'] = propensity_df['Infortunato'].fillna(0)


    propensity_df = propensity_df.merge(player_info[['Nome','Ruolo']], left_index = True, right_on='Nome')
    
    for bad_propensity in ['Infortunato','Esp','Amm','Gs']:
        propensity_df[bad_propensity] = 1-propensity_df[bad_propensity] 

    appetibility_index = []
    for idx,row in propensity_df.iterrows():
        if row['Ruolo'] == 'P':
            if row['ha_voto'] > 0:
                appetibility_index.append( { 'Ruolo':row['Ruolo'], 'Nome': row['Nome'] ,'appetibility':0.4 * row['Gs'] + 0.6 * row['ha_voto'] })
            else:
                appetibility_index.append( { 'Ruolo':row['Ruolo'], 'Nome': row['Nome'] ,'appetibility':0 } )
                
        if row['Ruolo'] == 'D':
            if row['ha_voto'] > 0:
                appetibility_index.append( { 'Ruolo':row['Ruolo'], 'Nome': row['Nome'] ,'appetibility': 0.15 * row['Amm'] + 0.1 * row['Esp'] + 0.35 * row['ha_bonus'] + 0.35 * row['ha_voto']  })
            else:
                appetibility_index.append( { 'Ruolo':row['Ruolo'], 'Nome': row['Nome'] ,'appetibility':0 } )
                
        if row['Ruolo'] == 'C':
            if row['ha_voto'] > 0:
                appetibility_index.append( { 'Ruolo':row['Ruolo'], 'Nome': row['Nome'] ,'appetibility': 0.15 * row['Amm'] + 0.5 * row['ha_bonus'] + 0.35 * row['ha_voto']  })
            else:
                appetibility_index.append( { 'Ruolo':row['Ruolo'], 'Nome': row['Nome'] ,'appetibility':0 } )
                
        if row['Ruolo'] == 'A':
            if row['ha_voto'] > 0:
                appetibility_index.append( { 'Ruolo':row['Ruolo'], 'Nome': row['Nome'] ,'appetibility': 0.2 * row['easy_gambe_bonus'] + 0.4 * row['ha_bonus'] + 0.4 * row['ha_voto']  })
            else:
                appetibility_index.append( { 'Ruolo':row['Ruolo'], 'Nome': row['Nome'] ,'appetibility':0 } )


    appettiblity = pd.DataFrame(appetibility_index)
    
    return propensity_df, appetibility_index