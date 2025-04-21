import pandas as pd

df = pd.read_csv('Problem1/results.csv', na_values='N/a')
df = df.apply(pd.to_numeric, errors='ignore')
df.fillna(0, inplace= True)

median_df = df.groupby('Team', as_index= False).median(numeric_only= True)
mean_df = df.groupby('Team', as_index= False).mean(numeric_only= True)
std_df = df.groupby('Team', as_index= False).std(numeric_only= True)

mean_df.drop(columns= ['Unnamed: 0', 'MP', 'Starts'], inplace= True)
median_df.drop(columns= ['Unnamed: 0', 'MP', 'Starts'], inplace= True)
std_df.drop(columns= ['Unnamed: 0', 'MP', 'Starts'], inplace= True)
combined_dict = {}

for col in median_df.columns:
    if col == 'Team':
        combined_dict['Team'] = median_df['Team']
        continue
    combined_dict[f'Median of {col}'] = median_df[col]
    combined_dict[f'Mean of {col}'] = mean_df[col]
    combined_dict[f'Std of {col}'] = std_df[col]

combined_df = pd.concat(combined_dict.values(), axis= 1)
combined_df.columns = combined_dict.keys()

combined_df.to_csv('Problem2/results2.csv', index= True)