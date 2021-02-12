from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

def read_covid_data():
    covid_df = pd.read_csv(f'./datasets/owid-covid-data.csv')
    covid_df['datetime'] = pd.to_datetime(covid_df['date'])

    # remove other countries than sweden
    covid_df = covid_df[covid_df.location.isin(['Sweden'])]

    # there's some weirdness going on in the beginning of the pandemic, total deaths decreases a few times
    # there's prety much no deaths yet before March 10, 2020 anyway so lets just remove it
    covid_df = covid_df[covid_df.datetime > datetime(2020,3,10)]
    
    return covid_df

def plot_apartment_price_vs_covid_deaths(apartments_df):
    covid_df = read_covid_data()

    fig, ax = plt.subplots(figsize=(8,4))

    # group apartment sales by quarter and plot mean price/square meter. Could also use month but quarter looks cleaner
    quarters = apartments_df.groupby(pd.Grouper(key='sale_datetime', freq='Q')).price_per_area.mean()
    quarters.plot(x='sale_datetime', y='price_per_area', style="b-")

    print("Price change:",int(((quarters.iloc[len(quarters) - 1] - quarters[0]) / quarters[0]) * 100), "%")

    # plot total deaths on the same timeline
    covid_df.plot(x='datetime', y='total_deaths', ax=ax, label='Swedish covid deaths', secondary_y=True, style="r--", dashes=(1, 10), ylabel="Price / m² (SEK)")

    plt.show()
