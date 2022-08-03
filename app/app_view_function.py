from turtle import left, right
import plotly.express as px
import pandas as pd
import numpy as np
from flask import Flask, render_template,request, redirect, url_for
from app_utils_function import build_team, player_table_prepocessing


def view_player_table(player_info, all_teams, fav_file = None, role = 'P', filter_presence = 0, team_selected = 'Tutte', slot = 'Tutti', show_fav = True, show_not_fav = True, sort_by = [None,None], tool_asta = False):
    
    table, all_images, ids_favourite, slot_count = player_table_prepocessing (player_info = player_info,
                                                                              fav_file = fav_file , 
                                                                              role = role,
                                                                              filter_presence = filter_presence ,
                                                                              team_selected = team_selected , 
                                                                              slot = slot , 
                                                                              show_fav = show_fav, show_not_fav = show_not_fav , 
                                                                              sort_by = sort_by, 
                                                                              tool_asta = tool_asta )
    
    if tool_asta:
        return render_template('tool_asta.html', 
                            actual_role = role, actual_team = team_selected, 
                            actual_min_pres = filter_presence, actual_slot = slot,
                            images_existing = all_images, fav_ids = ids_favourite,
                            all_teams = all_teams, 
                            table = table, count_slot = slot_count,
                            show_fav = show_fav, show_not_fav = show_not_fav)
    
    else:
        return render_template( 'role_explorer.html', 
                            actual_role = role, actual_team = team_selected, 
                            actual_min_pres = filter_presence, actual_slot = slot,
                            images_existing = all_images, fav_ids = ids_favourite,
                            all_teams = all_teams, 
                            table = table,
                            show_fav = show_fav, show_not_fav = show_not_fav )

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
    return render_template('player_page.html', actual_name = nome,
                                               names = all_names,
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