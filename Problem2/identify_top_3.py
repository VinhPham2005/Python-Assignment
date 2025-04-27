import pandas as pd

df = pd.read_csv('Problem1/results.csv', na_values= ['N/a'])
df = df.fillna(0)
df = df.reset_index(drop= True)
statics = df.columns[9:]
for col in statics:
    df[col] = pd.to_numeric(df[col])

for static in statics:
    sorted_df = df.sort_values(static, ascending= False).drop(columns= 'Unnamed: 0')
    top3 = sorted_df.head(3).copy()
    top3.insert(0, 'Note', 'Top 3')
    bottom3 = sorted_df.tail(3).copy()
    bottom3.insert(0, 'Note', 'Bottom 3')

    combined = pd.concat([top3, bottom3])

    with open('Problem2/top_3.txt', 'a', encoding= 'utf-8') as file:
        file.write('Top 3 hightest and lowest for static: {}\n'.format(static))
        file.write(combined.to_string(index= False))
        file.write('\n\n')

