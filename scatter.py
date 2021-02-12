import matplotlib.pyplot as plt
import matplotlib as mpl

def price_scatter_plot(apartments_df, xaxis, yaxis, xlabel=False, ylabel=False):
    df = apartments_df[[xaxis, yaxis]].dropna()

    ax = df.plot.scatter(x=xaxis, y=yaxis, s=2, xlabel=xlabel or xaxis, ylabel=ylabel or yaxis)

    ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    plt.show()
