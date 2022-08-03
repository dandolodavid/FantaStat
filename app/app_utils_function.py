import pandas as pd
import numpy as np
import plotly.express as px
import os.path
from os import listdir
from os.path import isfile, join

def map_features_role_exploration():
    
    map_features_role_exploration={
        'Presenza':'Pres',
        'Gol':'Gol',
        'Assist':'Ass',
        'xG':'xGol', 
        'xA':'xAss',
        'Gol 90':'Gol90',
        'Gol subiti':'Gol subiti',
        'Gol subiti 90':'Gol subiti90',
        'Rigori parati':'Rp',
        'Titolare':'Tit',
        'Entrato':'Ent',
        'Rigori calciati':'Rc',
        'Rigori segnati':'Rs',
        'Ammonizioni':'Amm',
        'Espulsioni':'Esp',
        'media_voto' : 'MV', 
        'media_fantavoto':'MFV',
        '%_con_voto' : '%Voto',
        '%_bonus' : '%Bonus', 
        '%_malus' : '%Malus',
        'Bonus' : 'Bonus',
        'Malus' : 'Malus',
        'Performance_gol_segnati' : 'Perf',
        '%_voto_<_5': '% V<5', 
        '%_voto_5_6': '% 5<=V<6',  
        '%_voto_6_7': '% 6<=V<7', 
        '%_voto_7_8': '% 7<=V<8', 
        '%_voto_>_8': '% V>8', 
        '%_fv_5': '% FV<5', 
        '%_fv_5_6': '% 5<=FV<6',  
        '%_fv_6_7': '% 6<=FV<7', 
        '%_fv_7_8': '% 7<=FV<8', 
        '%_fv_>_8': '% FV>8', 
    }
    
    return map_features_role_exploration

def get_first_header(role):
    
    first_level_header = {
        'P':[['Giocatore','Presenze','Gol subiti','Bonus Malus','Voti','Comportamento %','Distributione Voto','Distribuzione Fantavoto'],
             [2,1,2,3,2,3,5,5]],
        'D':[['Giocatore','Presenze', 'Statistiche','Totali Bonus/Malus','Voti', 'Comportamento %', 'Expected Bonus','Distributione Voto','Distribuzione Fantavoto'],
             [2,3,7,2,2,3,5,5,5]],
        'C':[['Giocatore','Presenze', 'Statistiche','Totali Bonus/Malus','Voti', 'Comportamento %', 'Expected Bonus','Distributione Voto','Distribuzione Fantavoto'],
             [2,3,7,2,2,3,5,5,5]],
        'A':[['Giocatore','Presenze', 'Statistiche','Totali Bonus/Malus','Voti', 'Comportamento %', 'Expected Bonus','Distributione Voto','Distribuzione Fantavoto'],
             [2,3,7,2,2,3,5,5,5]],
    }
    
    return first_level_header[role]

def get_features(role):

    features = {
                
                    'P': ['img','Nome','Squadra','Presenza','Gol subiti','Gol subiti 90','Rigori parati','Ammonizioni','Espulsioni',
                        'media_voto', 'media_fantavoto',
                        '%_con_voto','%_bonus', '%_malus',
                        '%_voto_<_5', '%_voto_5_6', '%_voto_6_7', '%_voto_7_8','%_voto_>_8', 
                        '%_fv_5', '%_fv_5_6', '%_fv_6_7', '%_fv_7_8', '%_fv_>_8'],
            
                    'D':  [ 'img','Nome','Squadra', 
                           'Presenza','Titolare', 'Entrato',
                            'Gol', 'Assist', 'Gol 90', 'Rigori calciati','Rigori segnati', 'Ammonizioni','Espulsioni',
                            'Bonus','Malus',
                            'media_voto', 'media_fantavoto',
                            '%_con_voto','%_bonus', '%_malus',
                            'xG', 'xA','xG90', 'xA90','Performance_gol_segnati',
                            '%_voto_<_5', '%_voto_5_6', '%_voto_6_7', '%_voto_7_8','%_voto_>_8', 
                            '%_fv_5', '%_fv_5_6', '%_fv_6_7', '%_fv_7_8', '%_fv_>_8'],
            
                    'C':  [ 'img','Nome','Squadra', 
                           'Presenza','Titolare', 'Entrato',
                            'Gol', 'Assist', 'Gol 90', 'Rigori calciati','Rigori segnati',
                            'Ammonizioni','Espulsioni',
                            'Bonus','Malus',
                            'media_voto', 'media_fantavoto',
                            '%_con_voto','%_bonus', '%_malus',
                            'xG', 'xA','xG90', 'xA90','Performance_gol_segnati',
                            '%_voto_<_5', '%_voto_5_6', '%_voto_6_7', '%_voto_7_8','%_voto_>_8', 
                            '%_fv_5', '%_fv_5_6', '%_fv_6_7', '%_fv_7_8', '%_fv_>_8'],
            
                    'A':[ 'img','Nome','Squadra', 
                           'Presenza','Titolare', 'Entrato',
                            'Gol', 'Assist', 'Gol 90', 'Rigori calciati','Rigori segnati',
                            'Ammonizioni','Espulsioni',
                            'Bonus','Malus',
                            'media_voto', 'media_fantavoto',
                            '%_con_voto','%_bonus', '%_malus',
                            'xG', 'xA','xG90', 'xA90','Performance_gol_segnati',
                            '%_voto_<_5', '%_voto_5_6', '%_voto_6_7', '%_voto_7_8','%_voto_>_8', 
                            '%_fv_5', '%_fv_5_6', '%_fv_6_7', '%_fv_7_8', '%_fv_>_8'],
                }

    return features[role]

def cast_to_int_features():
    return ['Amm','Esp','Rs','Rc','Tit','Ent','Rp','Rs','P','Gs','A','G']

def get_images(cols):
    img_dict = {}
    for col in cols:
        img_dict[col] = col.lower().replace(' ','_') + '.png'

    return img_dict

def player_table_prepocessing(player_info, fav_file = None, role = 'P', filter_presence = 0, team_selected = 'Tutte', slot = 'Tutti', show_fav = True, show_not_fav = True, sort_by = [None,None], tool_asta=False):
    
    #carichiamo lo slot
    player_info.Id = player_info.Id.astype(str)
    if os.path.exists('../tmp/slot_df.csv'):
        slot_df = pd.read_csv('../tmp/slot_df.csv',index_col=[0])
        slot_df.Id = slot_df.Id.astype(str) 
        if 'Slot' in player_info.columns:
            player_info = player_info.drop(columns='Slot')
        player_info = player_info.merge(slot_df, left_on='Id', right_on='Id', how='left')
        player_info['Slot'] = player_info['Slot'].fillna('Non settato')
    else:
        player_info['Slot'] = 'Non settato'
        
    #carichiamo i preferiti
    ids_favourite = fav_file.read().splitlines()
    ids_favourite = [str(x) for x in ids_favourite]
    if '' in ids_favourite: 
        ids_favourite.remove('')
    fav_file.close()
    
    # applichiamo i filtri
    ## ruolo
    filtered_table = player_info.loc[player_info.Ruolo == role]
    ## presenza
    if int(filter_presence)>0:
        filtered_table = filtered_table.loc[filtered_table.Presenza.fillna(0).astype(int)>int(filter_presence)]
    ## squadra
    if team_selected!= 'Tutte':
        filtered_table = filtered_table.loc[filtered_table.Squadra == team_selected]
    if slot!= 'Tutti':
        filtered_table = filtered_table.loc[filtered_table.Slot == slot]
    ## vedere preferiti/non preferiti
    ids_not_favourite = list(np.setdiff1d( filtered_table.Id.unique(), ids_favourite ))
    ids_to_return = []
    if show_fav:
        ids_to_return = ids_to_return + ids_favourite
    if show_not_fav:
        ids_to_return = ids_to_return + ids_not_favourite

    filtered_table = filtered_table.loc[filtered_table.Id.isin(ids_to_return)]
       
    table = filtered_table[get_features(role) + ['Slot'] + ['Id'] ]
    
    if tool_asta:
        if os.path.exists('../tmp/remove_asta.txt'):
            remove_asta = open("../tmp/remove_asta.txt", "r")
            ids_to_remove_asta = remove_asta.read().splitlines()
            if '' in ids_to_remove_asta: 
                ids_to_remove_asta.remove('')
            table = table.loc[~table.Id.isin(ids_to_remove_asta)]
    
    #first_level_header = get_first_header(role)
    #first_level_header_name = first_level_header[0] 
    #first_level_header_size = first_level_header[1]

    for feature in table.columns.tolist():
        if feature in cast_to_int_features():
            table[feature] = table[feature].astype(int)
    
    table = table.rename(columns = map_features_role_exploration())
       
    all_images = [f for f in listdir('static/img') if isfile(join('static/img', f))]
    
    if sort_by[0]:
        table = table.sort_values(sort_by[0], ascending=sort_by[1])
        
    slot_count = table.groupby('Slot').count()['Nome'].to_dict()
    slot_count['Tutti'] = table.shape[0]
        
    
    return table.fillna(0), all_images, ids_favourite, slot_count

def build_team(team_list, player_info, player_hist):
    
    team_df = player_info.loc[player_info.Nome.isin(team_list)].copy()
    
    role_total = team_df.groupby('Ruolo')[['Bonus','Malus','Gol','Assist']].sum()
    role_mean = team_df.groupby('Ruolo')[['media_voto','media_fantavoto','%_con_voto', '%_fv_5', '%_fv_5_6', '%_fv_6_7', '%_fv_7_8', '%_fv_>_8',]].mean()
    
    table = role_total.merge(role_mean, left_index=True,right_index=True).loc[['P','D','C','A']].reset_index().rename(columns={ 'media_fantavoto' :'FMV',
                                                                                                                                'media_voto':'MV',
                                                                                                                                '%_con_voto':'% Voto',
                                                                                                                                '%_fv_5':'% FV<5',
                                                                                                                                '%_fv_5_6':'% 5<=FV<7',
                                                                                                                                '%_fv_6_7':'% 6<=FV<7',
                                                                                                                                '%_fv_7_8':'% 7<=FV<8 ',
                                                                                                                                '%_fv_>_8':'% FV>=8',
                                                                                                                            })
    table = np.round(table,2)

    team_hist = player_hist.loc[ player_hist.Nome.isin(team_list) ].copy()

    team_hist.loc[team_hist['Voto'] == 0,'FV'] = 6
    team_hist.loc[team_hist['Voto'] == 0,'Voto'] = 6
    
    mean_by_role_giornata = team_hist.groupby(['Ruolo','Giornata']).mean()[['Voto','FV']].reset_index()
    pt_giornata = team_hist.groupby(['Giornata']).sum()[['FV']].reset_index().rename(columns={'FV':'Punti'})
     
    mean_pt = np.round(pt_giornata['Punti'].mean(),2)
    bonus_total = table.Bonus.sum()
    malus_total = table.Malus.sum()
    
    color_discrete_map = {'P': 'orange', 'D': 'Yellow', 'C': 'blue','A':'red'}
    
    fig_history_punti_giornata = px.bar(pt_giornata, x="Giornata", y="Punti", title="Punti per giornata", color_discrete_map=color_discrete_map).to_html()
    fig_history_voto = px.line(mean_by_role_giornata, x="Giornata", y="Voto", color="Ruolo", title="Media voto per ruolo per giornata",  color_discrete_map=color_discrete_map).to_html()
    fig_history_fantavoto = px.line(mean_by_role_giornata, x="Giornata", y="FV", color="Ruolo", title="Media Fantavoto per ruolo per giornata",  color_discrete_map=color_discrete_map).to_html()
    
    return team_df, table, mean_pt, bonus_total, malus_total, fig_history_voto, fig_history_fantavoto, fig_history_punti_giornata

def slot_handler(slot_selector_list):
    
    records = []
    for slot_selector in slot_selector_list:
        ids = slot_selector.split(' + ')[0]
        slot = slot_selector.split(' + ')[1]
        
        records.append({'Id':ids,'Slot':slot})
    
    new_slot_df = pd.DataFrame(records)
    
    if os.path.exists('../tmp/slot_df.csv'):
        slot_df = pd.read_csv('../tmp/slot_df.csv',index_col=[0])
        slot_df.Id = slot_df.Id.astype(str)
        slot_df = pd.concat( [slot_df, new_slot_df] )
        slot_df = slot_df.drop_duplicates(subset='Id',keep='last').reset_index(drop=True)
    else:
        slot_df = new_slot_df.reset_index(drop=True)
        slot_df.Id = slot_df.Id.astype(str)
    
    slot_df.to_csv('../tmp/slot_df.csv')
    
        
    
    
    