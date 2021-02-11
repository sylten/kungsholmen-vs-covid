from read_prices import read_prices
import matplotlib.pyplot as plt
import matplotlib as mpl

df = read_prices()

df = df[(df.price < 12000000) & (df.living_space < 120)]

xaxis = 'street_attractiveness'
yaxis = 'price_per_area'
df = df[[xaxis, yaxis]].dropna()

ax = df.plot.scatter(x=xaxis, y=yaxis, s=1, xlabel="Street attractiveness (normalized mean price / m²)", ylabel="Price / m² (SEK)")

ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

plt.show()
