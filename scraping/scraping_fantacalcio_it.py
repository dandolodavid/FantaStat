from webbrowser import get
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from tqdm import tqdm
import re
from selenium.webdriver.common.keys import Keys
from os import listdir,rename
from os.path import isfile, join
import time

def status_map(status):
    status_dict = { '': 'Inutilizzato', '0' : 'Titolare', '1':'Entrato', '2':'Infortunato', '3':'Squalificato', '4':'Inutilizzato' }
    return status_dict[status]

def getDownLoadedFileName(driver, waitTime):
    driver.execute_script("window.open()")
    # switch to new tab
    driver.switch_to.window(driver.window_handles[-1])
    # navigate to chrome downloads
    driver.get('chrome://downloads')
    # define the endTime
    endTime = time.time()+waitTime
    while True:
        try:
            # get downloaded percentage
            downloadPercentage = driver.execute_script(
                "return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('#progress').value")
            # check if downloadPercentage is 100 (otherwise the script will keep waiting)
            if downloadPercentage == 100:
                # return the file name once the download is completed
                return driver.execute_script("return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('div#content  #file-link').text")
        except:
            pass
        time.sleep(1)
        if time.time() > endTime:
            break


def scraping_url(browser, url, download_path, extra_path = ''):
    '''
    Params:
    -------
    
    browser : object
        a selenium driver with already done login to fantacalcio.it
    url : str
        a valid url
        (example : https://www.fantacalcio.it/squadre/Lazio/Adamonis/5502/1/2021-22)
    path : str
        path to download the data 
    
    '''
    
    try:
            
        browser.get(url)
        stagione = url.split('/')[-1].replace('-','_')
        
        #esplorazione html
        html = browser.page_source 
        soup = BeautifulSoup(html, 'lxml') #take the html code of the web page    
        
        nome = soup.findAll('h1', {"class":'h5 player-name'})[0].text
        ruolo = soup.findAll('span', {"class":'role'})[0]['data-value'].upper()
        squadra = soup.findAll('a', {"class":'team-name team-link'})[0].text
        
        #status per ogni partita
        status_list = []
        for x in str(soup.findAll('ul', {"class":'dot-stripe'})[0]).split('\n'):
            if 'data-count' in x:
                for s in x.split(' '):
                    if 'data-count' in s:
                        giornata = s.split('=')[1].replace('"','')
                    if 'data-value' in s:
                        status = s.split('=')[1].split('>')[0].replace('"','')
                status_list.append({'Giornata':giornata,'Status':status})
        status_data = pd.DataFrame(status_list)
        status_data.Status = status_data.Status.map(status_map)
        
        #salvare url immagine
        img = soup.findAll('img', {"class":'player-image'})[0]['src']
        f = open(extra_path + 'img_src.txt', "a")
        f.write( ' { "Stagione" : "' + stagione + '", "Nome" : "' + nome + '", "Ruolo" : "' + ruolo + '", "Squadra" : "' + squadra + '", "Src" : "' + img + '" } \n ' )
        f.close()
        
        status_data.to_csv(extra_path + nome + '^(Status ' + stagione + ').csv')
        
        #download statistiche riepilogo
        onlyfiles_before = [f for f in listdir(download_path) if isfile(join(download_path, f))]
        browser.find_element_by_xpath('//*[@id="download-control"]').click()
        time.sleep(2)
        onlyfiles_after = [f for f in listdir(download_path) if isfile(join(download_path, f))]
        new_files = np.setdiff1d( onlyfiles_after, onlyfiles_before )[0]
        #rinomina il file
        rename(download_path+'\\'+new_files, download_path+'\\'+nome+ '^(Stagione ' + stagione + ').xlsx' )

    except:
        
        f = open("log_player_scraping.txt", "a")
        f.write(url + '\n')
        f.close()