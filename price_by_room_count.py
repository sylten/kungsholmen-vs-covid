import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('./datasets/apartment-prices.csv')

df.groupby('rooms').price_per_area.mean().plot.bar(x='rooms', y='price_per_area', xlabel="Room count", ylabel="Mean price/m²")

plt.show()
