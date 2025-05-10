import pandas as pd

df = pd.read_csv('SourceCode/Problem1/results.csv', na_values= ['N/a'])
df = df.fillna(0)
df = df.reset_index(drop= True)
statistics = df.columns[9:]
for col in statistics:
    df[col] = pd.to_numeric(df[col])

for statistic in statistics:
    sorted_df = df.sort_values(statistic, ascending= False).drop(columns= 'Unnamed: 0')
    top3 = sorted_df.head(3).copy()
    top3.insert(0, 'Note', 'Top 3')
    bottom3 = sorted_df.tail(3).copy()
    bottom3.insert(0, 'Note', 'Bottom 3')

    combined = pd.concat([top3, bottom3])

    with open('SourceCode/Problem2/top_3.txt', 'a', encoding= 'utf-8') as file:
        file.write('Top 3 hightest and lowest for statistic: {}\n'.format(statistic))
        file.write(combined.to_string(index= False))
        file.write('\n\n')

