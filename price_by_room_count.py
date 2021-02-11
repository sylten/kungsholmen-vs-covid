from read_prices import read_prices
import matplotlib.pyplot as plt

df = read_prices()

df.groupby('rooms').price_per_area.mean().plot.bar(x='rooms', y='price_per_area', xlabel="Room count", ylabel="Mean price/m²")

plt.show()
