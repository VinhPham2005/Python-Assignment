import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import joblib

df = pd.read_csv('SourceCode/Problem4/player_values.csv', na_values= 'N/a')
df.fillna(0, inplace=True)

df['Values'] = df['Values'].str.replace('€', '').str.replace('M', '').astype(float)
df['Pos'] = df['Pos'].str.split(',').str[0]
df = pd.get_dummies(df, columns=['Pos'])
for col in df.columns:
    if df[col].dtype == 'object':
        if df[col].str.contains(',').any():
            df[col] = df[col].str.replace(',','').astype(float)

features = df.select_dtypes(include= 'number').drop(columns= 'Values').columns

x = df[features]
y = df['Values']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size= 0.2)

model = LinearRegression()
model.fit(x_train, y_train)

y_pred = model.predict(x_test)

print('RMSE:', mean_squared_error(y_test, y_pred))
print('r2 score:', r2_score(y_test, y_pred))
joblib.dump(model, 'SourceCode/Problem4/linear_model.pkl')

