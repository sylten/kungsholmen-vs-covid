from read_prices import read_prices
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

p = read_prices()

columns = ['price', 'fee', 'living_space', 'supplemental_area', 'floor', 'street_attractiveness', 'latitude', 'longitude']
df = p[columns]
df = df[(df.price < 12000000) & (df.living_space < 120)] # There are very few values for the largest and most expensive apartments

df = df.apply(lambda col: col.fillna(col.mean()), axis=0) # There is 1 missing fee value, fill it with the mean

# category_columns = ['location_part']

# for column in category_columns:
#     df = pd.concat([df.drop(column, axis=1), pd.get_dummies(df[column], prefix=column, prefix_sep='_')], axis=1)

X = df.drop('price', axis=1)
y = df['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3)

model = LinearRegression().fit(X_train, y_train)

y_pred = model.predict(X_test)
score = r2_score(y_test, y_pred)

print("Coefficients:", list(zip(columns[1:], [round(coefficient, 2) for coefficient in model.coef_])))

print("R2-Score:", score)

def predict(fee, square_meters, supplemental_area, floor, attractiveness, latitude, longitude):
    predicton = model.predict([[fee, square_meters, supplemental_area, floor, attractiveness, latitude, longitude]])
    return (int(predicton), int(predicton/square_meters))

def get_street_attractiveness(street_id):
    return p[p.street_id == street_id].street_attractiveness.iloc[0]

# trying on a few recent prices not included in the data :)
print("Pipersgatan 18", predict(3062, 37.5, 0, 3, get_street_attractiveness('pipersgatan'), 59.33077979355131, 18.04613709033011))
print("John Bergs plan 3", predict(2331, 36, 0, 1, get_street_attractiveness('johnbergsplan'), 59.33660760344284, 18.02240339102813))
print("Pontonjärgatan 21", predict(1386, 37, 0, 2, get_street_attractiveness('pontonjrgatan'), 59.3287096941292, 18.03357154798916))
print("Kungsholmsgatan 11", predict(3355, 42, 0, 5, get_street_attractiveness('kungsholmsgatan'), 59.330794867459694, 18.04856538283224))

plt.scatter(X.living_space, y, s=2)
plt.scatter(X_test.living_space, y_pred, label="Predictions", color="r", s=2)

ax = plt.gca()
ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

plt.xlabel('Size (m²)')
plt.ylabel('Price (SEK)')

plt.legend()
plt.show()
