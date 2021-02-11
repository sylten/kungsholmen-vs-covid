from read_prices import read_prices
import matplotlib.pyplot as plt
import matplotlib as mpl

df = read_prices()

df = df[(df.price < 12000000) & (df.living_space < 120)]

xaxis = 'living_space'
yaxis = 'price'
df = df[[xaxis, yaxis]].dropna()

ax = df.plot.scatter(x=xaxis, y=yaxis, s=2)

ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

plt.show()
