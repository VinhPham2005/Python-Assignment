import pandas as pd
import numpy as np
from collections import Counter
import time

def deduplicate_columns(columns):
    counts = Counter()
    new_col = []
    for col in columns:
        if counts[col]:
            new_col.append(f'{col}_{counts[col]}')
        else:
            new_col.append(col)
        counts[col] += 1
    return new_col

def put_to_df(df, target, statics):
    for col in statics:
        df[col] = df['Player'].map(target[col]) if col in target.columns else None

def process(target):
    target.columns = target.columns.droplevel() if isinstance(target.columns, pd.MultiIndex) else target.columns
    target.columns = deduplicate_columns(target.columns)
    target.set_index('Player', inplace= True)

def get_stat(url):
    table = pd.read_html(url)

    df = table[0]
    df.columns = df.columns.droplevel() if isinstance(df.columns, pd.MultiIndex) else df.columns
 
    df = df[df['Min'] > 90]
    df['Team'] = ' '.join(url.split('/')[-1].split('-')[0:-1])
    df['First_Name'] = df['Player'].apply(lambda x: x.split()[0])
    df = df.sort_values('First_Name')

    df = df[~df['Player'].isin(['Squad Total', 'Opponent Total'])]
    df.columns = deduplicate_columns(df.columns)

    #goalkeeping
    gk = table[2]
    gk_statics = ['GA90', 'Save%', 'CS%', 'PKsv']
    process(gk)
    put_to_df(df, gk, gk_statics)
    
    #shooting
    st = table[4]
    st_stactics = ['SoT%', 'SoT/90', 'G/Sh', 'Dist']
    process(st)
    put_to_df(df, st, st_stactics)

    #passing
    ps = table[5]
    ps_statics = ['Cmp', 'Cmp%', 'TotDist', 'Cmp%_1', 'Cmp%_2', 'Cmp%_3', 'KP', '1/3', 'PPA', 'CrsPA', 'PrgP']
    process(ps)
    put_to_df(df, ps, ps_statics)

    # goal and shoot creation
    gsc = table[7]
    gsc_statics = ['SCA', 'SCA90', 'GCA', 'GCA90']
    process(gsc)
    put_to_df(df, gsc, gsc_statics)

    #defensive actions
    dfa = table[8]
    dfa_statics = ['Tkl', 'TklW', 'Att', 'Lost', 'Blocks', 'Sh', 'Pass', 'Int']
    process(dfa)
    put_to_df(df, dfa, dfa_statics)

    #possestion
    pss = table[9]
    pss_statics = ['Touches', 'Def Pen', 'Def 3rd', 'Mid 3rd', 'Att 3rd', 'Att Pen', 'Att', 'Succ%', 'Tkld%',
                   'Carries', 'PrgDist', 'PrgC', '1/3', 'CPA', 'Mis', 'Dis', 'Rec', 'PrgR']
    process(pss)
    put_to_df(df, pss, pss_statics)

    #miscellaneous 
    ms = table[11]
    ms_statics = ['Fls', 'Fld', 'Off', 'Crs', 'Recov', 'Won', 'Lost', 'Won%']
    process(ms)
    put_to_df(df, ms, ms_statics)

    df = df[['First_Name', 'Player', 'Nation', 'Team', 'Pos', 'Age', 'MP', 'Starts',
            'Min', 'Gls', 'Ast', 'CrdY', 'CrdR', 'xG', 'xAG', 'PrgC', 'PrgP',
            'PrgR', 'Gls_1', 'Ast_1', 'xG_1', 'xAG_1'] + gk_statics + 
            st_stactics + ps_statics + gsc_statics + dfa_statics +
            pss_statics + ms_statics]

    df.fillna('N/a', inplace= True)
    return df

urls = [
    'https://fbref.com/en/squads/822bd0ba/Liverpool-Stats',
    'https://fbref.com/en/squads/18bb7c10/Arsenal-Stats',
    'https://fbref.com/en/squads/e4a775cb/Nottingham-Forest-Stats',
    'https://fbref.com/en/squads/cff3d9bb/Chelsea-Stats',
    'https://fbref.com/en/squads/b8fd03ef/Manchester-City-Stats',
    'https://fbref.com/en/squads/8602292d/Aston-Villa-Stats',
    'https://fbref.com/en/squads/b2b47a98/Newcastle-United-Stats',
    'https://fbref.com/en/squads/fd962109/Fulham-Stats',
    'https://fbref.com/en/squads/d07537b9/Brighton-and-Hove-Albion-Stats',
    'https://fbref.com/en/squads/4ba7cbea/Bournemouth-Stats',
    'https://fbref.com/en/squads/47c64c55/Crystal-Palace-Stats',
    'https://fbref.com/en/squads/cd051869/Brentford-Stats',
    'https://fbref.com/en/squads/19538871/Manchester-United-Stats',
    'https://fbref.com/en/squads/361ca564/Tottenham-Hotspur-Stats',
    'https://fbref.com/en/squads/d3fd31cc/Everton-Stats',
    'https://fbref.com/en/squads/7c21e445/West-Ham-United-Stats',
    'https://fbref.com/en/squads/8cec06e1/Wolverhampton-Wanderers-Stats',
    'https://fbref.com/en/squads/b74092de/Ipswich-Town-Stats',
    'https://fbref.com/en/squads/a2d435b3/Leicester-City-Stats',
    'https://fbref.com/en/squads/33c895d4/Southampton-Stats',
]

Premier_league = get_stat(urls[0])
for url in urls[1:]:
    next_team = get_stat(url)
    Premier_league = pd.concat([Premier_league, next_team], ignore_index= True)
    time.sleep(3)   

Premier_league = Premier_league.sort_values('First_Name')
Premier_league = Premier_league.reset_index(drop= True).drop(columns= 'First_Name', errors= 'ignore')
Premier_league.to_csv('results.csv', index= True)