import numpy
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
from sklearn.model_selection import train_test_split
import pickle
if __name__ == "__main__":
    df = pd.read_csv('../data/edited_data.csv')
    companies = ["INTC", "MSFT", "GOOGL", "AIZ", "DE", "AMZN", "AAPL", "TSLA", "NVDA"]
    model_list = []
    print(df)
    for company in companies:
        temp_df = df[df["Symbol"]==company]


        temp_X = temp_df.drop("y", axis=1)
        temp_y = temp_df.y;
        temp_X.drop("Symbol", axis=1, inplace=True)
        temp_X.drop("Unnamed: 0", axis=1, inplace=True)

        temp_X = temp_X.iloc[1:,:]
        temp_y = temp_y.iloc[1:]

        X_train = temp_X.iloc[:-1]
        X_test = temp_X.iloc[-1]
        y_train = temp_y.iloc[:-1]
        y_test = temp_y.iloc[-1]
        temp_model = ARIMA(numpy.array(y_train).astype(float), order=(5, 7, 5), exog=numpy.array(X_train).astype(float)).fit()
        temp_model.save(company+".pkl")
        test_data = numpy.append(X_test, y_test)
        with open(company+"_test.pkl","wb") as f:
            pickle.dump(test_data, f)
        print(company + " model trained ")
    print("Model training done")
