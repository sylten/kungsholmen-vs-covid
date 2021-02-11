from read_prices import read_prices
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

apartments = read_prices()

apartments['datetime'] = pd.to_datetime(apartments['sale_date'])

fig, ax = plt.subplots(figsize=(8,4))
ax.set_ylabel("Price / m² (SEK)")
ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

for bounds in [(0, 25), (26, 50), (51, 150)]:
    df = apartments[(apartments['living_space'] >= bounds[0]) & (apartments['living_space'] <= bounds[1])]

    df = df.groupby(pd.Grouper(key='datetime', freq='Q')).price_per_area.mean()
    df.plot(x='datetime', y='price_per_area', ax=ax, label=f"{bounds[0]}-{bounds[1]} m²")

    first = df.iloc[0]
    last = df.iloc[len(df)-1]
    
    print(bounds, int(first), int(last), (last-first)/first)

plt.legend()
plt.show()
