import pandas as pd

data = pd.read_csv('data.csv')
average_price = data['price'].mean()
print(average_price)