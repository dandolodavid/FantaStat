import plotly.express as px
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
from flask import Flask, render_template,request, redirect, url_for
from team_builder import build_team

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

### VIEW FUNCTION

def view_role_explorer(player_info, all_teams, role = 'P', filter_presence = 0, team_selected = ' ' ):
    
    # applichiamo i filtri
    
    ## ruolo
    role_table = player_info.loc[player_info.Ruolo == role]
    ## presenza
    role_table = role_table.loc[role_table.Presenza.fillna(0).astype(int)>int(filter_presence)]
    ## squadra
    if team_selected!= ' ':
        role_table = role_table.loc[role_table.Squadra == team_selected]
       
    table = role_table[get_features(role)] 
    
    first_level_header = get_first_header(role)
    first_level_header_name = first_level_header[0] 
    first_level_header_size = first_level_header[1]

    for feature in table.columns.tolist():
        if feature in cast_to_int_features():
            table[feature] = table[feature].astype(int)
    
    table = table.rename(columns = map_features_role_exploration())
       
    all_images = [f for f in listdir('static/img') if isfile(join('static/img', f))]
    
    return render_template( 'role_explorer.html', images_existing = all_images,
                           first_level_header_name = first_level_header_name,
                           first_level_header_size = first_level_header_size,
                           all_teams = all_teams, 
                           table = table)

def view_classifica(classifica):
    return render_template( 'classifica.html',  table =  classifica )

def view_player_page(player_info, player_hist, all_names, nome):
    
    #extract information from the player
    data =  player_info.loc[player_info.Nome == nome]
    data = data.T.to_dict()[data.index.values[0]]
    history_data = player_hist.loc[player_hist.Nome == nome]
    history_con_voto = history_data.loc[history_data.ha_voto]
    
    #plot generation
    tmp_fantavoto = history_data[['Giornata','FV']].rename(columns={'FV':'Voto'}).reset_index(drop=True)
    tmp_fantavoto['Legenda'] = 'Fantavoto'
    tmp_voto = history_data[['Giornata','Voto']].reset_index(drop=True)
    tmp_voto['Legenda'] = 'Voto'
    
    plot_history = pd.concat([tmp_voto,tmp_fantavoto])
    plot_bonus = history_con_voto.groupby('Bonus').count().reset_index()
    
    
    fig_history = px.line(plot_history, x="Giornata", y="Voto", color="Legenda")
    plot_history = fig_history.to_html()
    
    fig = px.bar(plot_bonus, x="Bonus", y="Giornata")
    fig = fig.update_layout(yaxis_range=[0,history_data.shape[0]])
    plot_bonus = fig.to_html()
    
    ##
    return render_template('player_page.html', names = all_names,
                                               nome = data['Nome'], 
                                               team = data['Squadra'],
                                               img_src = data['img'],
                                               ruolo_classic = data['Ruolo'],
                                               media_voto = data['media_voto'],
                                               media_fantavoto = data['media_fantavoto'],
                                               mediana_voto = data['mediana_voto'],
                                               mediana_fantavoto = data['mediana_fantavoto'],
                                               presenze = int(data['Presenza']),
                                               presenze_voto = data['partite_voto'],
                                               perc_match_voto = data['%_con_voto'],
                                               minuti_giocati = int(data['Minuti']),
                                               minuti_medi = data['minuti_medi'],
                                               titolare = int(data['Titolare']),
                                               entrato = int(data['Entrato']),
                                               perc_entrato = data['%_subentrato'],
                                               sostituito = int(data['sostituito']),
                                               perc_sostituito = data['%_sostituito'],
                                               infortunato = int(data['Infortunato']),
                                               inutilizzato = int(data['Inutilizzato']),
                                               gol_segnati = data['Gol'],
                                               gol_segnati_90 = data['Gol 90'],
                                               assist = data['Assist'],
                                               xG = data['xG'],
                                               xA = data['xA'],
                                               xG90 = data['xG90'],
                                               xA90 = data['xA90'],
                                               rigori_segnati = data['Rigori segnati'],
                                               rigori_calciati = data['Rigori calciati'],
                                               status = data['Performance_gol_segnati'],
                                               totale_bonus = data['Bonus'],
                                               totale_malus = data['Malus'],
                                               partite_bonus = data['partite_bonus'],
                                               perc_bonus_match = data['%_bonus'],
                                               perc_fv_5 = data['%_fv_5'],
                                               perc_fv_5_6 = data['%_fv_5_6'],
                                               perc_fv_6_7 = data['%_fv_6_7'], 
                                               perc_fv_7_8 = data['%_fv_7_8'], 
                                               perc_fv_8 = data['%_fv_>_8'],
                                               perc_v_5 = data['%_voto_<_5'],
                                               perc_v_5_6 = data['%_voto_5_6'],
                                               perc_v_6_7 = data['%_voto_6_7'], 
                                               perc_v_7_8 = data['%_voto_7_8'], 
                                               perc_v_8 = data['%_voto_>_8'],        
                                               history_plot = plot_history,
                                               bonus_plot = plot_bonus)
    
def view_team_builder(player_info,modulo_scelto):
    '''
    '''
    grid_list = modulo_scelto.split('-')
    dif_class = 'dif_'+grid_list[0]
    cen_class = 'cen_'+grid_list[1]
    att_class = 'att_'+grid_list[2]

    n_dif = int(grid_list[0])
    n_cen = int(grid_list[1])
    n_att = int(grid_list[2])

    nomi_dif = ['nome_' + str(2+i) for i in range(0,n_dif)]
    nomi_cen = ['nome_' + str(n_dif+2+i) for i in range(0,n_cen)]
    nomi_att = ['nome_' + str(n_dif+n_cen+2+i) for i in range(0,n_att)]

    por_names = player_info.loc[player_info.Ruolo == 'P'].Nome.unique()
    dif_names = player_info.loc[player_info.Ruolo == 'D'].Nome.unique()
    cen_names = player_info.loc[player_info.Ruolo == 'C'].Nome.unique()
    att_names = player_info.loc[player_info.Ruolo == 'A'].Nome.unique()

    return render_template( 'team_builder.html',  modulo_scelto = modulo_scelto,
                           por_names = por_names, dif_names = dif_names, cen_names = cen_names, att_names = att_names, 
                           dif_class=dif_class, cen_class=cen_class, att_class=att_class,
                           n_dif = n_dif,n_cen = n_cen,n_att = n_att,
                           nomi_dif= nomi_dif,
                           nomi_cen = nomi_cen,
                           nomi_att = nomi_att
                          )
    
def view_builded_team(team_list, player_info, player_hist):
    
    team_df, table, mean_pt, bonus_total, malus_total, fig_history_voto, fig_history_fantavoto, fig_history_punti_giornata = build_team(team_list, player_info, player_hist)
    
    counts_role = team_df.Ruolo.value_counts()
    
    nome_por = team_df.loc[team_df.Ruolo == 'P'].Nome.unique()[0]
    nomi_dif = team_df.loc[team_df.Ruolo == 'D'].Nome.unique()
    nomi_cen = team_df.loc[team_df.Ruolo == 'C'].Nome.unique()
    nomi_att = team_df.loc[team_df.Ruolo == 'A'].Nome.unique()
    
    img_por = team_df.loc[team_df.Ruolo == 'P'].img.unique()[0]
    img_dif = team_df.loc[team_df.Ruolo == 'D'].img.unique()
    img_cen = team_df.loc[team_df.Ruolo == 'C'].img.unique()
    img_att = team_df.loc[team_df.Ruolo == 'A'].img.unique()
    
    
    dif_class = 'dif_'+ str(counts_role.loc['D'])
    cen_class = 'cen_'+ str(counts_role.loc['C'])
    att_class = 'att_'+ str(counts_role.loc['A'])
    
    
    return render_template( 'builded_team.html', table = table, 
                        dif_class = dif_class, cen_class = cen_class, att_class = att_class,
                        img_por = img_por,img_dif = img_dif,img_cen = img_cen,img_att = img_att,
                        nome_por = nome_por, nomi_dif = nomi_dif, nomi_cen = nomi_cen, nomi_att = nomi_att,
                        mean_pt = mean_pt, bonus_total = bonus_total, malus_total = malus_total, 
                        fig_history_voto = fig_history_voto, fig_history_fantavoto = fig_history_fantavoto,  fig_history_punti_giornata = fig_history_punti_giornata )