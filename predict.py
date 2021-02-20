from read_data import get_street_attractiveness, get_street_id
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

default_columns = ['price', 'fee', 'living_space', 'street_attractiveness']

def create_model(df, columns = default_columns, y_column='price'):
    """
    Description: Creates a linear regression model from a dataframe containing apartment price data.

    Arguments:
        df (DataFrame): dataframe containg apartment price data. 
        columns (list): column names to use for the regression. Default=['price', 'fee', 'living_space', 'street_attractiveness']
        y_column (list): column to predict. Default='price'

    Returns:
        LinearRegression: The linear regression model.
        list: Train X-values from train-test split.
        list: Train Y-values from train-test split.
        list: Test X-values from train-test split.
        list: Test Y-values from train-test split.
    """

    df = df[columns]

    # There is 1 missing fee value, fill it with the mean
    df = df.apply(lambda col: col.fillna(col.mean()), axis=0)

    X = df.drop(y_column, axis=1)
    y = df[y_column]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3)

    model = LinearRegression().fit(X_train, y_train)

    return model, X_train, X_test, y_train, y_test

def plot_regression(df, columns = default_columns, y_column='price'):
    """
    Description: Creates a linear regression model to predict apartment prices, and plots training and testing data as a scatter plot.

    Arguments:
        df (DataFrame): dataframe containg apartment price data. 
        columns (list): column names to use for the regression. Default=['price', 'fee', 'living_space', 'street_attractiveness']
        y_column (list): column to predict. Default='price'

    Returns:
        None
    """

    model, X_train, X_test, y_train, y_test = create_model(df, columns, y_column)

    y_pred = model.predict(X_test)

    # print("Coefficients:", list(zip(columns[1:], [round(coefficient, 2) for coefficient in model.coef_])))
    print("R2-Score:", r2_score(y_test, y_pred))

    plt.scatter(X_train.living_space, y_train, s=2)
    plt.scatter(X_test.living_space, y_pred, label="Predictions", color="r", s=2)

    ax = plt.gca()
    ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    plt.xlabel('Size (m²)')
    plt.ylabel('Price (SEK)')

    plt.legend()
    plt.show()

def predict(df, address, square_meters, fee):
    """
    Description: Estimates an apartment's sale price.

    Arguments:
        df (DataFrame): dataframe containg apartment price data. 
        address (string): The apartment's street address.
        square_meters (float): Size of the apartment in square meters.
        fee (float): The fee of the apartment.

    Returns:
        int: Estimated price in SEK.
    """

    model, X_train, X_test, y_train, y_test = create_model(df)
    predicted_price = model.predict([[fee, square_meters, get_street_attractiveness(df, get_street_id(address))]])
    return int(predicted_price)
