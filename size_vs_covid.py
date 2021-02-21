import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

def plot_price_timeline_for_apartment_sizes(apartments_df):
    """
    Description: Shows price development by quarter for different apartment sizes. Size groups: 0-25m², 26-50m² and 51-120m².

    Arguments:
        apartments_df (DataFrame): dataframe containg apartment price data.

    Returns:
        None
    """

    fig, ax = plt.subplots(figsize=(8,4))
    ax.set_ylabel("Price / m² (SEK)")
    ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    # Most of the apartments sold during the last 12 months were 1 or 2 room apartments
    # So splitting the larger apartments into more groups would not be reliable at all because of too few data points
    # Group apartments into 3 size categories and plot a line per group
    for bounds in [(0, 25), (26, 50), (51, 120)]:
        bounds_df = apartments_df[(apartments_df['living_space'] >= bounds[0]) & (apartments_df['living_space'] <= bounds[1])]

        # Group mean price by quarter
        bounds_df = bounds_df.groupby(pd.Grouper(key='sale_datetime', freq='Q')).price_per_area.mean()

        bounds_df.plot(x='sale_datetime', y='price_per_area', ax=ax, label=f"{bounds[0]}-{bounds[1]} m²")

        price_first_quarter = bounds_df.iloc[0]
        price_last_quarter = bounds_df.iloc[len(bounds_df)-1]
        
        print(bounds[0], "to", bounds[1], "m² -", "Price Q1 2020:", int(price_first_quarter), "SEK/m², Price Q1 2021:", int(price_last_quarter), "SEK/m², Change:", round(((price_last_quarter-price_first_quarter)/price_first_quarter)*100, 1), "%")

    plt.legend()
    plt.show()
