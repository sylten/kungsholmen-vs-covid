import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('./datasets/apartment-prices.csv')
df['datetime'] = pd.to_datetime(df['sale_date'])

print(df.groupby('rooms').price_per_area.mean())
print(df.groupby('rooms').living_space.mean())
print(df.groupby('street_id').price_per_area.mean().astype(int).sort_values(ascending=False).head())

# print(df.rooms.value_counts())

# df.groupby(pd.Grouper(key='datetime', freq='M')).price_per_area.mean().plot(x='datetime', y='price_per_area', label='Date')

# plt.show()
