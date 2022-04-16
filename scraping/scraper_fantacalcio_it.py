import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
from selenium.webdriver.common.keys import Keys

def player_info_scraper(url):
    
    try:
        chromepath = "selenium/webdriver/chrome/chromedriver.exe"
        browser = webdriver.Chrome(chromepath)
        browser.get(url)
        time.sleep(5)
        browser.find_element_by_xpath('//*[@id="qc-cmp2-ui"]/div[3]/div/button[3]').click()
        for i in range(1,5):
            time.sleep(2) #time to complete the opta data loading
            scroll = browser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN) #necessary to make the page load all the table and the opta data
        time.sleep(5)

        player_info = {} #empty dictionary to store the file

        html = browser.page_source 
        soup = BeautifulSoup(html, 'lxml') #take the html code of the web page

        player_info['nome'] = soup.findAll('span', {"itemprop": "name"})[-1].text
        player_info['team'] = soup.findAll('span', {"itemprop": "name"})[-2].text
        player_info['img'] =  soup.findAll('img', {"class":'img-responsive'})[1]['src']

        presence_table = pd.read_html(str(soup.findAll('table')[2]))[0] #read the chart table to obtain number of match as Titolare, Entrato, Infortunato, Inutilizzato
        for idx,row in presence_table.iterrows():
            player_info[row.Status.lower()] = row.Presenze
            
        player_info['presenze'] = player_info['titolare'] + player_info['entrato'] #calculate total match of the player

        bonus_malus_table = pd.read_html(str(soup.findAll('table')[3]))[0] # read bonus malus table
        bonus_malus_table = bonus_malus_table.loc[bonus_malus_table.Giornate.apply(lambda x:'ª' in x )] #to remove future matches not already played
        voti_table = pd.read_html(str(soup.findAll('table')[0]))[0] #read voti/fantavoti
        history_table = bonus_malus_table.merge(voti_table[['Voto','Fantavoto']], left_index=True,right_index=True) #merge of voti and bonus/malus

        #from opta data we retrive number of sustituion, total minute, yellow card, red card
        for idx in soup.findAll('div',{'class':'Opta-Stat'})[1:4]: 
            number,event = re.sub( r"([A-Z])", r" ;\1", idx.text).split(';')
            player_info[event.lower().replace('da ','').replace(' ','_')] = int(number.replace('.',''))
        for idx in soup.findAll('div',{'class':'Opta-Stat'})[-2:]:
            number,event = re.sub( r"([A-Z])", r" ;\1", idx.text).split(';')
            player_info[event.lower().replace(' ','_')] = int(number)
            
        if player_info['presenze'] != 0:
            player_info['%_bonus_match'] = np.round(history_table.loc[history_table.Bonus>0].shape[0]/player_info['presenze']*100,2)
            player_info['%_malus_match'] = np.round(history_table.loc[history_table.Malus!=0].shape[0]/player_info['presenze']*100,2)
        else:
            player_info['%_bonus_match'] = 0
            player_info['%_malus_match'] = 0
                
        player_info['%_match_voto'] = np.round(history_table.loc[history_table.Voto!=0].shape[0]/bonus_malus_table.shape[0]*100,2)
        
        if player_info['titolare'] != 0:
            player_info['%_sostituzione'] = np.round(player_info['sostituito']/player_info['titolare']*100,2)
        else:
            player_info['%_sostituzione'] = 0

        browser.close()
        history_table['Nome'] = player_info['nome']

        return player_info,history_table

    except:
        browser.close()
        f = open("log_player_scraping.txt", "a")
        f.write(url + '\n')
        f.close()
        
        return 0,0