from read_prices import read_prices
import pandas as pd

df = read_prices()
df['datetime'] = pd.to_datetime(df['sale_date'])

print(df.groupby('rooms').price_per_area.mean().astype(int))
print(df.groupby('rooms').living_space.mean().astype(int))

print(df.groupby('street_id').price_per_area.mean().astype(int).sort_values(ascending=True).head())

print(df[df.street_id == 'sysslomansgatan'].street_attractiveness.iloc[0])

print(df[(df.street_attractiveness < .2) & (df.price_per_area > 120000)].head())