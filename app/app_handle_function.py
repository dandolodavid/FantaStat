import pandas as pd
import numpy as np
from app_utils_function import slot_handler,build_team
from app_view_function import view_player_table, view_classifica, view_builded_team, view_player_page, view_team_builder
from flask import Flask, render_template,request, redirect, url_for, session

def player_table_handler(session):
    '''
    '''
    
    if 'sort' in request.form:
        sort_by = request.form.getlist('sort')
        if session['actual_sort_by'][0] == sort_by[0]:
            session['actual_sort_by'] = [sort_by[0],not session['actual_sort_by'][1]]
        else:
            session['actual_sort_by'] = [sort_by[0],True]
    
    if 'checked_fav' in request.form or  'checked_not_fav' in request.form:
        
        if 'checked_fav' in request.form:
            show_fav = True
        else:
            show_fav = False

        if 'checked_not_fav' in request.form:
            show_not_fav = True
        else:
            show_not_fav = False

        session['actual_show_fav'] = show_fav
        session['actual_show_not_fav'] = show_not_fav
        
    if 'slot_selector' in request.form:
        name_and_slot_list = request.form.getlist('slot_selector')
        slot_handler(name_and_slot_list)

    if 'add_to_fav' in request.form:
        
        name_for_fav = request.form.get('add_to_fav')    
        file_in = open('../tmp/favourite.txt',"r")

        names_favourite = file_in.read().splitlines()
        if '' in names_favourite: 
            names_favourite.remove('')
        file_in.close()
        
        if name_for_fav in names_favourite:
            file_write = open('../tmp/favourite.txt',"w")
            names_favourite.remove(name_for_fav)
            for names in names_favourite:
                if names != '':
                    file_write.write(names + '\n')
            file_write.close()
        else:
            file_append = open('../tmp/favourite.txt',"a")
            file_append.write(name_for_fav +'\n')
            file_append.close()
        
    if 'min_pres' in request.form:
        min_pres = request.form.get('min_pres')
        session['actual_min_pres'] = min_pres
        
    if 'role_selected' in request.form:
        min_pres = request.form.get('role_selected')
        session['actual_role_selected'] = min_pres

    if 'team_selected' in request.form:
        min_pres = request.form.get('team_selected')
        session['actual_team_selected'] = min_pres
    
    if 'slot_asta' in request.form:
        slot_asta = request.form.get('slot_asta')
        session['actual_slot_asta'] = slot_asta
        
    if 'remove' in request.form:
        
        id_to_remove = request.form.get('remove')    
        file_in = open('../tmp/remove_asta.txt',"a")

        file_append = open('../tmp/remove_asta.txt',"a")
        file_append.write(id_to_remove +'\n')
        file_append.close()


def home_page(session, all_names):
    
    session['actual_nome_selezionato'] = all_names[0]
    session['actual_team_list'] = []
    session['actual_modulo_scelto'] = '3-4-3'
    session['actual_role_selected'] = 'P'
    session['actual_min_pres'] = 0
    session['actual_team_selected'] = 'Tutte'
    session['actual_slot_asta'] = 'Tutti'
    session['actual_show_fav'] = True
    session['actual_show_not_fav'] = True
    session['actual_sort_by'] = [None,False]
    
    return render_template('home_page.html')


def handle_name(session, player_info, player_hist, all_names):
    nome_selected = request.form.get('nome_selezionato')
    session['actual_nome_selezionato'] = nome_selected
    return view_player_page(player_info,player_hist,all_names,session['actual_nome_selezionato'])


def handle_role_explorer_home(player_info, all_teams):
    fav_file = open("../tmp/favourite.txt", "r")
    return view_player_table(player_info, all_teams, fav_file = fav_file )


def handle_role_explorer(session, player_info, all_teams):
    '''
    
    '''
    
    player_table_handler(session=session)
    
    fav_file = open("../tmp/favourite.txt", "r")
    
    return view_player_table(player_info, all_teams, fav_file = fav_file,
                              slot = session['actual_slot_asta'],
                              role = session['actual_role_selected'], 
                              filter_presence = session['actual_min_pres'], 
                              team_selected = session['actual_team_selected'],
                              show_fav = session['actual_show_fav'],
                              show_not_fav = session['actual_show_not_fav'],
                              sort_by = session['actual_sort_by'])
    

def handle_team_builder(session,player_info, player_hist):
    session['actual_team_list'] = []
    if 'scegli_modulo' in request.form:
        modulo_scelto = request.form.get('modulo_scelto')
        session['actual_modulo_scelto']  = modulo_scelto
        return view_team_builder(player_info, session['actual_modulo_scelto'] )
    
    if 'build_team' in request.form:
        for i in range(1,12):
            session['actual_team_list'].append(request.form.get('nome_'+str(i)))
        return view_builded_team(session['actual_team_list'], player_info, player_hist)
    

def handle_tool_asta(session, listone, all_teams):
    
    player_table_handler(session=session)
    
    fav_file = open("../tmp/favourite.txt", "r")
    
    return view_player_table(listone, all_teams, fav_file = fav_file, tool_asta = True,
                              slot = session['actual_slot_asta'],
                              role = session['actual_role_selected'], 
                              filter_presence = session['actual_min_pres'], 
                              team_selected = session['actual_team_selected'],
                              show_fav = session['actual_show_fav'],
                              show_not_fav = session['actual_show_not_fav'],
                              sort_by = session['actual_sort_by'])