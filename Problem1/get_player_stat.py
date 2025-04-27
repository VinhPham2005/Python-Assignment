import pandas as pd
import numpy as np 
from functools import reduce
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

def get_static(target_static, target_rows):
    target = []
    for row in target_rows:
        try:
            name = row.find_element(By.CSS_SELECTOR, 'td[data-stat="player"]').text.strip()
            if not name:
                continue
        except:
            continue
        target_data = {}
        for static, static_id in target_static.items():
            target_data[static] = row.find_element(By.CSS_SELECTOR, f'td[data-stat="{static_id}"]').text.strip()
        target.append(target_data)
    df_target = pd.DataFrame(target)
    return df_target

options = Options()
options.add_argument('--headless')  
options.add_argument('--disable-gpu')  
options.add_argument('--log-level=3')  
options.add_argument("--disable-logging")
options.add_argument('--blink-settings=imagesEnabled=false')
options.page_load_strategy = 'eager'
driver = webdriver.Edge(options=options)

driver.get('https://fbref.com/en/comps/9/stats/Premier-League-Stats')

rows = WebDriverWait(driver, 20).until(
    ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'table#stats_standard tbody > tr:not(.thead):not(.rowSum)'))
)

player_static = {
    'Player': "player",
    'Nation': "nationality",
    'Team': "team",
    'Pos': "position",
    'Age': "age",
    'MP': "games",
    'Starts': "games_starts",
    'Min': "minutes",
    'Gls': "goals",
    'Ast': "assists",
    'CrdY': "cards_yellow",
    'CrdR': "cards_red",
    'xG': "xg",
    'xAG': "xg_assist",
    'PrgC': "progressive_carries",
    'PrgP': "progressive_passes",
    'PrgR': "progressive_passes_received",
    'Gls/90': "goals_per90",
    'Ast/90': "goals_assists_per90",
    'xG/90': "xg_per90",
    'xGA/90': "xg_assist_per90"
}

data = []
for row in rows:
    player_data = {}
    for static, static_id in player_static.items():
        player_data[static] = row.find_element(By.CSS_SELECTOR, f'td[data-stat="{static_id}"]').text.strip()
        
    if int(player_data['Min'].replace(',','')) > 90: 
        data.append(player_data)

df = pd.DataFrame(data)
df['First_name'] = df['Player'].apply(lambda x: x.split()[0])
df = df.sort_values(by= ['First_name', 'Player'])
players= set(df['Player'])

gk_static = {
    'Player': 'player',
    'Team': "team",
    'GA90': 'gk_goals_against_per90',
    'Save%': 'gk_save_pct',
    'CS%': 'gk_clean_sheets_pct',
    'PSave%': 'gk_pens_save_pct'
}

st_static = {
    'Player': 'player',
    'Team': "team",
    'SoT%': 'shots_on_target_pct',
    'SoT/90': 'shots_on_target_per90',
    'G/sh': 'goals_per_shot',
    'Dist': 'average_shot_distance'
}

ps_static = {
    'Player': 'player',
    'Team': "team",
    'Cmp': 'passes_completed',
    'Cmp%': 'passes_pct',
    'TotDist': 'passes_total_distance',
    'SCmp%': 'passes_pct_short',
    'MCmp%': 'passes_pct_medium',
    'LCmpt%': 'passes_pct_long',
    'KP': 'assisted_shots',
    '1/3(passing)': 'passes_into_final_third',
    'PPA': 'passes_into_penalty_area',
    'CrsPA': 'crosses_into_penalty_area',
    'PrgP(passing)': 'progressive_passes'
}

gca_static = {
    'Player': 'player',
    'Team': "team",
    'SCA': 'sca',
    'SCA90': 'sca_per90',
    'GCA': 'gca',
    'GCA90': 'gca_per90'
}

dfs_static = {
    'Player': 'player',
    'Team': "team",
    'Tkl': 'tackles', 
    'TklW': 'tackles_won',
    'Att(defense)': 'challenges',
    'Lost(defense)': 'challenges_lost',
    'Blocks': 'blocks',
    'Sh': 'blocked_shots',
    'Pass': 'blocked_passes',
    'Int': 'interceptions'
}

pss_static = {
    'Player': 'player',
    'Team': "team",
    'Touches': 'touches',
    'Def Pen': 'touches_def_pen_area',
    'Def 3rd': 'touches_def_3rd',
    'Mid 3rd': 'touches_mid_3rd',
    'Att 3rd': 'touches_att_3rd',
    'Att Pen': 'touches_att_pen_area',
    'Att(possession)': 'take_ons',
    'Succ%': 'take_ons_won_pct',
    'Tkld%': 'take_ons_tackled_pct',
    'Carries': 'carries',
    'PrgDist': 'carries_progressive_distance',
    'PrgC(possession)': 'progressive_carries',
    '1/3(possession)': 'carries_into_final_third',
    'CPA': 'carries_into_penalty_area',
    'Mis': 'miscontrols',
    'Dis': 'dispossessed',
    'Rec': 'passes_received',
    'PrgR(possession)': 'progressive_passes_received'
}

mis_static = {
    'Player': 'player',
    'Team': "team",
    'Fls': 'fouls',
    'Fld': 'fouled',
    'Off': 'offsides',
    'Crs': 'crosses',
    'Recov': 'ball_recoveries',
    'Won': 'aerials_won',
    'Lost':'aerials_lost',
    'Won%': 'aerials_won_pct'
}

targets = [
    ('table#stats_keeper',  gk_static, 'https://fbref.com/en/comps/9/keepers/Premier-League-Stats'),
    ('table#stats_shooting',st_static, 'https://fbref.com/en/comps/9/shooting/Premier-League-Stats'),
    ('table#stats_passing',ps_static, 'https://fbref.com/en/comps/9/passing/Premier-League-Stats'),
    ('table#stats_gca',gca_static, 'https://fbref.com/en/comps/9/gca/Premier-League-Stats'),
    ('table#stats_defense',dfs_static, 'https://fbref.com/en/comps/9/defense/Premier-League-Stats'),
    ('table#stats_possession',pss_static, 'https://fbref.com/en/comps/9/possession/Premier-League-Stats'),
    ('table#stats_misc',mis_static, 'https://fbref.com/en/comps/9/misc/Premier-League-Stats')
]

dataframes = [df]
for table, target_static, url in targets:
    driver.get(url)
    rows = WebDriverWait(driver, 20).until(
        ec.presence_of_all_elements_located((By.CSS_SELECTOR, f'{table} tbody > tr:not(.thead)'))
    )
    df_target = get_static(target_static, rows)
    df_target = df_target.dropna(subset=['Player']) 
    df_target = df_target[df_target['Player'].isin(df['Player'])]
    df_target = df_target.drop_duplicates(subset=['Player', 'Team'])
    dataframes.append(df_target)

df_all = reduce(lambda left, right: left.merge(right, on=['Player', 'Team'], how='left'), dataframes)
df_all = df_all.replace('', np.nan).fillna('N/a')
df_all = df_all.reset_index(drop= True).drop(columns= 'First_name', errors= 'ignore')

df_all.to_csv('Problem1/results.csv', index= True)
driver.quit()
