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