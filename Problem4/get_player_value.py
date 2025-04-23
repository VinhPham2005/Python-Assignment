import unidecode
import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time

options = Options() 
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--blink-settings=imagesEnabled=false')
options.page_load_strategy = 'eager'

def clean_name(name):
    if pd.isnull(name): return ''
    name = name.lower()
    name = unidecode.unidecode(name)
    name = name.replace('-', ' ').replace('.', '').strip()
    tmp = name.split()
    name = [tmp[0], tmp[-1]]
    return ' '.join(sorted(name))

driver = webdriver.Edge(options= options)

df = pd.DataFrame(columns=['Player', 'Values'])

base_url = 'https://www.footballtransfers.com/us/values/players/most-valuable-soccer-players/playing-in-uk-premier-league'
for k in range(1, 23):
    url = base_url if k == 1 else base_url + f'/{k}'
    
    driver.get(url)
    time.sleep(2)

    rows = WebDriverWait(driver, 20).until(
        ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'tbody#player-table-body > tr'))
    )

    players = []
    for i in range(len(rows)):
        try:
            row = driver.find_elements(By.CSS_SELECTOR, 'tbody#player-table-body > tr')[i]
            name = row.find_element(By.CSS_SELECTOR, 'td.td-player a').text.strip()
            value = row.find_element(By.CSS_SELECTOR, 'span.player-tag').text.strip()
            players.append({'Player': name, 'Values': value})
        except:
            players.append({'Player': None, 'Values': None})
            
    player_df = pd.DataFrame(players)
    df = pd.concat([df, player_df], ignore_index= True)

all_pl = pd.read_csv('Problem1/results.csv')

df['Name'] = df['Player'].apply(clean_name)
all_pl['Name'] = all_pl['Player'].apply(clean_name)

df_all = pd.merge(df, all_pl, on= 'Name', how= 'inner')
df_all['Min'] = df_all['Min'].str.replace(',', '').astype(float)
df_all = df_all[df_all['Min'] > 900]
df_all.dropna(inplace= True)
drop_cols = ['Unnamed: 0', 'Name', 'Player_y']
df_all.drop(columns= drop_cols, inplace= True)
df_all.rename(columns= {'Player_x': 'Player'}, inplace= True)
df_all.reset_index(drop= True, inplace= True)
df_all.to_csv('Problem4/player_values.csv')