from datetime import datetime
from read_prices import read_prices
import pandas as pd
import matplotlib.pyplot as plt

apartments = read_prices()
apartments['datetime'] = pd.to_datetime(apartments['sale_date'])

covid = pd.read_csv(f'./datasets/owid-covid-data.csv')
covid = covid[covid.location.isin(['Sweden'])]
covid['datetime'] = pd.to_datetime(covid['date'])
covid = covid[covid.datetime > datetime(2020,3,10)]

fig, ax = plt.subplots(figsize=(8,4))

apartments.groupby(pd.Grouper(key='datetime', freq='Q')).price_per_area.mean().plot(x='datetime', y='price_per_area', style="b-", label='Price / m²')
covid.plot(x='datetime', y='total_deaths', ax=ax, label='Swedish covid deaths', secondary_y=True, style="r--", dashes=(1, 10), ylabel="Price / m² (SEK)")

plt.show()