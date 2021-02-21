from read_data import get_street_attractiveness, get_street_id, read_and_clean_apartment_data
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error

default_columns = ['price', 'fee', 'living_space', 'street_attractiveness']
default_y = default_columns[0]

def create_model(df, columns = default_columns, y_column=default_y):
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

    X = df.drop(y_column, axis=1)
    y = df[y_column]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, random_state=42)

    model = LinearRegression().fit(X_train, y_train)

    return model, X_train, X_test, y_train, y_test

def evaluate_model(df, columns = default_columns, y_column=default_y): 
    """
    Description: Creates a linear regression model to predict apartment prices, and evaluates the model using R squared and mean squared error.

    Arguments:
        df (DataFrame): dataframe containg apartment price data. 
        columns (list): column names to use for the regression. Default=['price', 'fee', 'living_space', 'street_attractiveness']
        y_column (list): column to predict. Default='price'

    Returns:
        float: R2-score
        float: Mean squared error
    """
    model, X_train, X_test, y_train, y_test = create_model(df, columns, y_column)

    y_pred = model.predict(X_test)

    return r2_score(y_test, y_pred), mean_squared_error(y_test, y_pred, squared=False)

def plot_regression(df, columns = default_columns, y_column=default_y):
    """
    Description: Creates a linear regression model to predict apartment prices, and plots training data and predicted testing data as a scatter plot.

    Arguments:
        df (DataFrame): dataframe containg apartment price data. 
        columns (list): column names to use for the regression. Default=['price', 'fee', 'living_space', 'street_attractiveness']
        y_column (list): column to predict. Default='price'

    Returns:
        float: R2-score
        float: Mean squared error
    """

    model, X_train, X_test, y_train, y_test = create_model(df, columns, y_column)

    y_pred = model.predict(X_test)

    xaxis = 'living_space'
    plt.scatter(X_train[xaxis], y_train, s=2)
    plt.scatter(X_test[xaxis], y_pred, label="Predictions", color="r", s=2)

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
