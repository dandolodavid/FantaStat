import pandas as pd
import numpy as np
import plotly.express as px


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