from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

apartments = pd.read_csv('./datasets/apartment-prices.csv')

apartments['datetime'] = pd.to_datetime(apartments['sale_date'])

fig, ax = plt.subplots(figsize=(8,4))
ax.set_ylabel("Price / m²")

# for rooms in [1,2,3,4]:
#     df = apartments[apartments.rooms == rooms].groupby(pd.Grouper(key='datetime', freq='Q')).price_per_area.mean()
#     print(rooms, df.head())    
#     df.plot(x='datetime', y='price_per_area', ax=ax, label=f"{rooms} rooms")

for bounds in [(0, 25), (26, 50), (51, 150)]:
    df = apartments[(apartments['living_space'] >= bounds[0]) & (apartments['living_space'] <= bounds[1])]

    df = df.groupby(pd.Grouper(key='datetime', freq='Q')).price_per_area.mean()
    df.plot(x='datetime', y='price_per_area', ax=ax, label=f"{bounds[0]}-{bounds[1]} m²")

    first = df.iloc[0]
    last = df.iloc[len(df)-1]
    print(bounds, int(first), int(last), (last-first)/first)

# for loc in ['Kungsholmen', 'Kristineberg', 'Fredhäll']:
#     df = apartments[apartments.location_name == loc + ', Stockholm'].groupby(pd.Grouper(key='datetime', freq='Q')).price_per_area.mean()
#     print(loc, df.head())    
#     df.plot(x='datetime', y='price_per_area', ax=ax, label=f"{loc}")

# print(apartments.groupby(pd.Grouper(key='datetime', freq='M')).price_per_area.mean().head())

# fig, ax = plt.subplots(figsize=(18,6))

# apartments.groupby(pd.Grouper(key='datetime', freq='M')).price_per_area.mean().plot(x='datetime', y='price_per_area', style="b-", label='Mean price/m²')

# for name, group in apartments.groupby('rooms'):
#     group.plot(x='datetime', y='total_deaths', ax=ax, label=name)

plt.legend()
plt.show()
