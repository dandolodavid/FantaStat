import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
from selenium.webdriver.common.keys import Keys

def xg_scraper(url):
    
    x_path_button_orig = '//*[@id="league-players"]/div[1]/ul/li'
    
    #try:
    chromepath = "selenium/webdriver/chrome/chromedriver.exe"
    browser = webdriver.Chrome(chromepath)
    browser.get(url)
    scroll = browser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN) #necessary to make the page load all the table and the opta data

    html = browser.page_source 
    soup = BeautifulSoup(html, 'lxml') #take the html code of the web page

    #overall stats
    classifica_table = pd.read_html(str(soup.findAll('table')[0]))[0]
    classifica_table.xG = classifica_table.xG.apply(lambda x: x.replace('+','-').split('-')[0])
    classifica_table.xGA = classifica_table.xGA.apply(lambda x: x.replace('+','-').split('-')[0])
    classifica_table.xPTS = classifica_table.xPTS.apply(lambda x: x.replace('+','-').split('-')[0])
    classifica_table['Performance_gol_segnati'] = 'Under'
    classifica_table.loc[classifica_table['G'].astype(float) > classifica_table['xG'].astype(float),'Performance_gol_segnati'] = 'Over'

    
    #player xG and xA
    dfs = []
    i = 1
    bc_click = 1

    while i < int(soup.findAll('li',{'class':'page'})[-1].text)+1:
        html = browser.page_source 
        soup = BeautifulSoup(html, 'lxml')
        dfs.append( pd.read_html(str(soup.findAll('table')[1]))[0].dropna() )
        i = i+1
        bc_click = i
        if bc_click>5:
            bc_click = 5
        x_path = x_path_button_orig+'['+str(bc_click)+']'
        browser.find_element_by_xpath(x_path).click()
        time.sleep(1)

    x_path = x_path_button_orig+'[6]'
    html = browser.page_source 
    soup = BeautifulSoup(html, 'lxml')
    dfs.append( pd.read_html(str(soup.findAll('table')[1]))[0].dropna() )    

    x_path = x_path_button_orig+'[7]'
    html = browser.page_source 
    soup = BeautifulSoup(html, 'lxml')
    dfs.append( pd.read_html(str(soup.findAll('table')[1]))[0].dropna() )    
    
    player_xg = pd.concat(dfs).reset_index(drop=True)
    player_xg.xG = player_xg.xG.apply(lambda x: x.replace('+','-').split('-')[0])
    player_xg.xA = player_xg.xA.apply(lambda x: x.replace('+','-').split('-')[0])
    player_xg['Performance_gol_segnati'] = 'Under'
    player_xg.loc[player_xg['G'].astype(float) > player_xg['xG'].astype(float),'Performance_gol_segnati'] = 'Over'

    return player_xg, classifica_table
    
    #except:
    #    browser.close()
    #    return 0,0