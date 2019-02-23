import numpy as np
import pandas as pd
from sklearn import preprocessing, svm
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn import tree
import matplotlib.pyplot as plt
from matplotlib import style
import datetime
import math
from sklearn.model_selection import cross_val_score
import ExtractKittyData

def handle_non_numerical_data(df):
    columns = df.columns.values
    for column in columns:
        text_digit_vals = {}
        def convert_to_int(val):
            return text_digit_vals[val]

        if df[column].dtype != np.int64 and df[column].dtype != np.float64:
            column_contents = df[column].values.tolist()
            unique_elements = set(column_contents)
            x = 0
            for unique in unique_elements:
                if unique not in text_digit_vals:
                    text_digit_vals[unique] = x
                    x+=1

            df[column] = list(map(convert_to_int, df[column]))

    return df

def predictCatPrice(cat):
    ExtractKittyData.writeBasicCatRow(cat, "catstest.csv")
    print(cat)
    catID = cat['id']
    df = pd.read_csv("catstest.csv")
    #df = df.drop(['ID'], axis=1)
    print(df)
    
    
    df.fillna(value=-99999, inplace=True)

    handle_non_numerical_data(df)
    
    forecast_col = 'Price'
    #df.dropna(inplace=True)

    forecast_out = int(math.ceil(0.01 * len(df)))

    predictCat = df.tail(1)
    df = df.drop(df.index[-1])
    print(df)
    X = np.array(df.drop(['Price'], 1))
    y = np.array(df['Price'])
    

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.0)

    y_train = (y_train * 100000)
    y_test = (y_test * 100000)

    for i in range(len(y_train)):
        y_train[i] = (int)(y_train[i])
        
    for i in range(len(y_test)):
        y_test[i] = (int)(y_test[i])
          
    clf = RandomForestRegressor(n_estimators=15)
    clf.fit(X_train, y_train)

    actualPrice = predictCat['Price'].values[0]

    predictCat = predictCat.drop(['Price'], 1)
    predict_me = np.array(predictCat)

    predict_me = predict_me.reshape(-1, len(cat))
    predictPrice = clf.predict(predict_me)
    
    diff = predictPrice - actualPrice
    
    print ("Cat: " + str(catID) + " is " + str((diff / actualPrice)*100) + "% off")
    print("It is being sold for: " + str(actualPrice) + " but should be " + str(predictPrice/100000))


"""
clf = RandomForestRegressor(n_estimators=15)
clf.fit(X_train, y_train)
print(clf.score(X_test, y_test))
"""
