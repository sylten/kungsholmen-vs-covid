import matplotlib.pyplot as plt
import matplotlib as mpl

def price_scatter_plot(apartments_df, xaxis, yaxis, title=None, xlabel=False, ylabel=False):
    """
    Description: Shows a scatter plot from data in a dataframe.

    Arguments:
        apartments_df (DataFrame): dataframe containg apartment price data. 
        xaxis (string): Column to use for x-axis.
        yaxis (string): Column to use for y-axis.
        xlabel (string): Label for x-axis. If unspecified, the column name will be used.
        ylabel (string): Label for y-axis. If unspecified, the column name will be used.

    Returns:
        None
    """
    df = apartments_df[[xaxis, yaxis]].dropna()

    ax = df.plot.scatter(x=xaxis, y=yaxis, s=2, title=title, xlabel=xlabel or xaxis, ylabel=ylabel or yaxis)

    ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    plt.show()
