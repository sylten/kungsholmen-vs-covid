# kungsholmen-vs-covid
Analysis of apartment prices on Kungsholmen in Stockholm, Sweden during the year of covid-19, 2020.

## Dependencies
- Python 3
- Pandas
- Scikit Learn
- matplotlib

## Files
### kungsholmen-vs-covid.ipynb
Documents the analysis process and results.

### predict.py
Linear regression model that uses aprtment data to predict future apartment prices.

### price_vs_covid.py
Plots mean price and total covid deaths in Sweden during the last 12 months.

### read_data.py
Reads and cleans the datasets used in the analysis.

### scatter.py
Generic scatter plot function for pricing data.

### size_vs_covid.py
Plots timeline of price development for different apartment sizes.

## Summary
The conclusion of the analysis is that apartment prices on Kungsholmen were probably affected by the Covid-19 pandemic. The most obvious effect was a brief chock to prices during the initial phase of the spread of the virus. A closer look at different sized apartments suggests that very small apartments took a more severe hit as prices did not recover during 2020. Predicting the price of future apartments proves difficult considering the market volatility, but the regression model developed can at least help in giving a price indication.
