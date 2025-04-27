import os
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('Problem1/results.csv', na_values= 'N/a')
df.fillna(0, inplace=True)
df.drop(columns='Unnamed: 0', inplace= True)
df['Age'] = df['Age'].apply(lambda x: int(str(x).split('-')[0]))

statics = ['Gls', 'xG', 'SCA90', 'Tkl', 'Int', 'Blocks']
for static in statics:
    df[static] = pd.to_numeric(df[static].astype(str).replace(',', '', regex= True), errors= 'coerce')

teams = df['Team'].drop_duplicates().tolist()
teams_dict = {team: df[df['Team'] == team] for team in teams}

for static in statics:
    fig, axes = plt.subplots(3, 7, figsize = (12, 6))
    
    axes[0, 0].hist(df[static], bins= 25, edgecolor= 'black', linewidth= 0.7, color= 'seagreen')
    axes[0, 0].set_title(f'Premier league - {static}', fontsize= 10)
    for i, (team, team_df) in enumerate(teams_dict.items(), start= 1):
        col = i % 7
        row = i // 7
        axes[row, col].hist(team_df[static], bins= 25, edgecolor= 'black', linewidth= 0.7)
        axes[row, col].set_title(f'{team} - {static}', fontsize= 10)
    static = static.replace('/','')
    file_name = f'{static}.png'
    plt.tight_layout()
    if not os.path.exists('Problem2/Data'):
        os.mkdir('Problem2/Data')
    plt.savefig('Problem2/Data/{}'.format(file_name))
    plt.close()