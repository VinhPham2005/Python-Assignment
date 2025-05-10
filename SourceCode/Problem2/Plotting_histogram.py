import os
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('SourceCode/Problem1/results.csv', na_values= 'N/a')
df.fillna(0, inplace=True)

statistics = ['Gls', 'xG', 'SCA90', 'Tkl', 'Int', 'Blocks']
for statistic in statistics:
    df[statistic] = pd.to_numeric(df[statistic].astype(str).replace(',', '', regex= True), errors= 'coerce')

teams = df['Team'].drop_duplicates().tolist()
teams_dict = {team: df[df['Team'] == team] for team in teams}

for statistic in statistics:
    fig, axes = plt.subplots(3, 7, figsize = (12, 6))
    
    axes[0, 0].hist(df[statistic], bins= 25, edgecolor= 'black', linewidth= 0.7, color= 'seagreen')
    axes[0, 0].set_title(f'Premier league - {statistic}', fontsize= 10)
    for i, (team, team_df) in enumerate(teams_dict.items(), start= 1):
        col = i % 7
        row = i // 7
        axes[row, col].hist(team_df[statistic], bins= 25, edgecolor= 'black', linewidth= 0.7)
        axes[row, col].set_title(f'{team} - {statistic}', fontsize= 10)
    statistic = statistic.replace('/','')
    file_name = f'{statistic}.png'
    plt.tight_layout()
    if not os.path.exists('SourceCode/Problem2/Data'):
        os.mkdir('SourceCode/Problem2/Data')
    plt.savefig('SourceCode/Problem2/Data/{}'.format(file_name))
    plt.close()
