import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def read_prices():
    df = pd.read_csv('./datasets/apartment-prices.csv')

    # There's a few outliers among the largest and most expensive apartments, so exclude them
    df = df[(df.price < 12000000) & (df.living_space < 120)]

    # There's an interesting outlying price of around 130 000 SEK/m² on a street with an attractiveness of less than .2, remove it
    df = df[df.id != 1229419]

    df['sale_datetime'] = pd.to_datetime(df['sale_date'])
    df['fee_per_area'] = df['fee'] / df['living_space']

    street_mean = df.groupby('street_id').price_per_area.transform('mean') # get each street's mean price per square meter
    df['street_attractiveness'] = MinMaxScaler().fit_transform(street_mean.values.reshape(-1,1)) # define street attractivenes as the normalized mean price per square meter

    return df

def get_street_attractiveness(df, street_id):
    return df[df.street_id == street_id].street_attractiveness.iloc[0]