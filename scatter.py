import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

df = pd.read_csv('./datasets/apartment-prices.csv')

df = df[['price', 'living_space']].dropna()
df = df[(df.price < 12000000) & (df.living_space < 120)]

ax = df.plot.scatter(x='living_space', y='price', s=2, xlabel="Size (m²)", ylabel="Price (SEK)")

ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

plt.show()
