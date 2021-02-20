from read_data import read_covid_data
import pandas as pd
import matplotlib.pyplot as plt

def plot_apartment_price_vs_covid_deaths(apartments_df):
    """
    Description: Plot's apartment prices and total covid death count as line plots. 

    Arguments:
        apartments_df (DataFrame): dataframe containg apartment price data. 

    Returns:
        None
    """

    covid_df = read_covid_data()

    fig, ax = plt.subplots(figsize=(8,4))

    # group apartment sales by quarter and plot mean price/square meter. Could also use month but quarter looks cleaner
    quarters = apartments_df.groupby(pd.Grouper(key='sale_datetime', freq='Q')).price_per_area.mean()
    quarters.plot(x='sale_datetime', y='price_per_area', style="b-")

    print("Price change:",int(((quarters.iloc[len(quarters) - 1] - quarters[0]) / quarters[0]) * 100), "%")

    # plot total deaths on the same timeline
    covid_df.plot(x='datetime', y='total_deaths', ax=ax, label='Swedish covid deaths', secondary_y=True, style="r--", dashes=(1, 10), ylabel="Price / m² (SEK)")

    plt.show()
