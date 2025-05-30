import pandas as pd
from collections import Counter

df = pd.read_csv('SourceCode/Problem1/results.csv', na_values='N/a')
df.fillna(0, inplace= True)
df.drop(columns='Unnamed: 0', inplace= True)
df['Age'] = df['Age'].apply(lambda x: int(str(x).split('-')[0]))

statistics = df.select_dtypes(include=['number']).columns
for col in statistics:
    df[col] = pd.to_numeric(df[col].astype(str).replace(',', '', regex= True), errors= 'coerce')


teams =df['Team'].drop_duplicates().tolist()
teams_dict = {team: df[df['Team'] == team] for team in teams}

team_count = []

for statistic in statistics:
    tmp = {}
    if statistic == 'CrdY' or statistic == 'CrdR':
        for team, team_df in teams_dict.items():
            min_value = team_df[statistic].sum()
            tmp[min_value] = team
        minn = min(tmp.keys())
        print(f'Highest score for statistics {statistic} is {tmp[minn]}: {minn}')
    else:
        for team, team_df in teams_dict.items():
            max_value = team_df[statistic].mean()
            tmp[max_value] = team
        maxx = max(tmp.keys())
        team_count.append(tmp[maxx])
        print(f'Highest score for statistics {statistic} is {tmp[maxx]}: {maxx}')

team_count = Counter(team_count)
best_team = team_count.most_common(1)[0]
print('The team is performing the best in 2024 - 2025 Premier League season is:',  best_team[0], 'with', best_team[1], 'statistics with highest score')
