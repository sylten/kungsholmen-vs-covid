from read_prices import get_street_attractiveness, read_prices
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

default_columns = ['price', 'fee', 'living_space', 'floor', 'street_attractiveness']

def create_model(df, columns = default_columns):
    df = df[columns]
    df = df[(df.price < 12000000) & (df.living_space < 120)] # There are very few values for the largest and most expensive apartments

    df = df.apply(lambda col: col.fillna(col.mean()), axis=0) # There is 1 missing fee value, fill it with the mean

    X = df.drop('price', axis=1)
    y = df['price']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3)

    model = LinearRegression().fit(X_train, y_train)

    return model, X_train, X_test, y_train, y_test

def plot_regression(df, columns = default_columns):
    model, X_train, X_test, y_train, y_test = create_model(df, columns)

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

def predict(df, fee, square_meters, floor, street_id):
    model, X_train, X_test, y_train, y_test = create_model(df)
    predicton = model.predict([[fee, square_meters, floor, get_street_attractiveness(df, street_id)]])
    return int(predicton)
