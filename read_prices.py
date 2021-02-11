import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def read_prices():
    df = pd.read_csv('./datasets/apartment-prices.csv')

    street_mean = df.groupby('street_id').price_per_area.transform('mean')
    df['street_attractiveness'] = MinMaxScaler().fit_transform(street_mean.values.reshape(-1,1))
    
    return df
