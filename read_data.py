from datetime import datetime
import pandas as pd
import re
from sklearn.preprocessing import MinMaxScaler

def extract_number(text):
    if text != text:
        return None
    
    return float(re.sub(r"[^0-9,]", "", text).replace(',','.'))

def get_street_id(address):
    first_number = re.search(r"\d", address)
    return re.sub(r"[^A-z]", "", address[:(first_number.start() if first_number != None else len(address))]).lower()

def get_street_attractiveness(df, street_id):
    return df[df.street_id == street_id].street_attractiveness.iloc[0]

def read_and_clean_apartment_data():
    df = pd.read_csv('./datasets/hemnet-data.csv')
    
    # One listing has a missing size, let's just drop it since it's only 1
    df = df[df.living_space.notnull()]

    # Prices are formatted to be displayed on a website so we need to remove non-digits
    df.price_per_area = df.price_per_area.apply(extract_number)
    df.asked_price = df.asked_price.apply(extract_number)
    df.price = df.price.apply(extract_number)
    df.fee = df.fee.apply(extract_number)
    

    # Sizes are in square meters and also need some cleaning
    df.living_space = df.living_space.apply(extract_number)
    df.supplemental_area = df.supplemental_area.apply(extract_number)
    df.rooms = df.rooms.apply(extract_number)
    df['fee_per_area'] = df.fee / df.living_space

    df['street_id'] = df.address.apply(get_street_id)

    # Get datetime from sale date
    # The sale date is also formatted so the first 5 chars are always "Såld " ("Sold " in Swedish)
    df['sale_datetime'] = pd.to_datetime(df.sale_date.str[5:])

    # There's a few outliers among the largest and most expensive apartments, so exclude them
    df = df[(df.price < 12000000) & (df.living_space < 120)]

    # There's an interesting outlying price of around 130 000 SEK/m² on a street with an attractiveness of less than .2, remove it
    # I moved it up here so it wouldnät influence the attractiveness calculation
    df = df[df.id != 1229419]

    # Get each street's mean price per square meter
    street_mean = df.groupby('street_id').price_per_area.transform('mean')

    # Define street attractivenes as the normalized mean price per square meter
    df['street_attractiveness'] = MinMaxScaler().fit_transform(street_mean.values.reshape(-1,1))

    return df

def read_covid_data():
    covid_df = pd.read_csv(f'./datasets/owid-covid-data.csv')
    covid_df['datetime'] = pd.to_datetime(covid_df['date'])

    # remove other countries than sweden
    covid_df = covid_df[covid_df.location.isin(['Sweden'])]

    # there's some weirdness going on in the beginning of the pandemic, total deaths decreases a few times
    # there's prety much no deaths yet before March 10, 2020 anyway so lets just remove it
    covid_df = covid_df[covid_df.datetime > datetime(2020,3,10)]
    
    return covid_df