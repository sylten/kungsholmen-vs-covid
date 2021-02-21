from datetime import datetime
import math
import pandas as pd
import re
from sklearn.preprocessing import MinMaxScaler

def extract_number(text):
    """
    Description: Removes all non-numeric characters and returns all numbers found as a floating point number. Converts , decimal separator to .

    Arguments:
        text (string): Text to extract number from.

    Returns:
        float: Extracted number with . as decimal point.
    """
    if text != text:
        return None
    
    return float(re.sub(r"[^0-9,]", "", text).replace(',','.'))

def get_street_id(address):
    """
    Description: Removes street number and any additional information from address and returns a unique identifier for streets.

    Arguments:
        address (string): A street address to create id for.

    Returns:
        string: Street identifier.
    """

    first_number = re.search(r"\d", address)
    return re.sub(r"[^A-z]", "", address[:(first_number.start() if first_number != None else len(address))]).lower()

def get_street_attractiveness(df, street_id):
    """
    Description: Finds street attractiveness for a street id.

    Arguments:
        df (DataFrame): dataframe containg apartment price data, including street attractiveness. 
        street_id (string): Street id to look for

    Returns:
        float: Street attractiveness.
    """

    return df[df.street_id == street_id].street_attractiveness.iloc[0]

def clean_outliers(df):
    """
    Description: Remove apartments over a certain price point, or under or over a certain sizes.

    Arguments:
        df (DataFrame): dataframe containg apartment price data.

    Returns:
        DataFrame: Cleaned apartment data.
    """

    # Remove extreme prices per area
    df = df[(df.price_per_area > 60000) & (df.price_per_area < 120000)]

    # Remove extreme final prices
    df = df[(df.price <= 12000000)]

    # Remove extremely small and very large apartments
    df = df[(df.living_space >= 15) & (df.living_space <= 120)]

    return df

def read_and_clean_apartment_data(remove_outliers = True):
    """
    Description: Read's apartment data from a csv file containing apartment data from Hemnet. 
    Skips data rows with no specified size or size > 120 square meters or sale price over 12 million SEK.
    Adds columns fee_per_area= Fee divided by square meters, street_id= Unique street id, street_attractiveness: estimated attractiveness of the apartment's street.

    Arguments:
        remove_outliers (boolean): Whether or not to remove identified outliers.

    Returns:
        DataFrame: DataFrame containing cleaned apartment data.
    """

    df = pd.read_csv('./datasets/hemnet-data.csv')

    # Prices are formatted to be displayed on a website so we need to remove non-digits
    df.price_per_area = df.price_per_area.apply(extract_number)
    df.asked_price = df.asked_price.apply(extract_number)
    df.price = df.price.apply(extract_number)
    df.fee = df.fee.apply(extract_number)

    # Sizes are in square meters and also need some cleaning
    df.living_space = df.living_space.apply(extract_number)
    df.supplemental_area = df.supplemental_area.apply(extract_number)
    df.rooms = df.rooms.apply(extract_number).apply(lambda r: math.floor(r))
    df['fee_per_area'] = df.fee / df.living_space

    df['street_id'] = df.address.apply(get_street_id)

    # Get datetime from sale date
    # The sale date is also formatted so the first 5 chars are always "Såld " ("Sold " in Swedish)
    df['sale_datetime'] = pd.to_datetime(df.sale_date.str[5:])

    if remove_outliers:
        df = clean_outliers(df)

    # Get each street's mean price per square meter
    street_mean = df.groupby('street_id').price_per_area.transform('mean')

    # Define street attractivenes as the normalized mean price per square meter
    df['street_attractiveness'] = MinMaxScaler().fit_transform(street_mean.values.reshape(-1,1))

    return df

def read_covid_data():
    """
    Description: Read's Swedish covid data per date from Our World in Data.

    Returns:
        DataFrame: Dataframe containing swedish covid data after 2020-03-10.
    """

    covid_df = pd.read_csv(f'./datasets/owid-covid-data.csv')
    covid_df['datetime'] = pd.to_datetime(covid_df['date'])

    # remove other countries than sweden
    covid_df = covid_df[covid_df.location.isin(['Sweden'])]

    # there's some weirdness going on in the beginning of the pandemic, total deaths decreases a few times
    # there's prety much no deaths yet before March 10, 2020 anyway so lets just remove it
    covid_df = covid_df[covid_df.datetime > datetime(2020,3,10)]
    
    return covid_df