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

df = pd.read_csv("catstest.csv")
#df = df.drop(['ID'], axis=1)


df.fillna(value=-99999, inplace=True)
handle_non_numerical_data(df)
print(df)
forecast_col = 'Price'
#df.dropna(inplace=True)

forecast_out = int(math.ceil(0.01 * len(df)))

X = np.array(df.drop(['Price'], 1))
y = np.array(df['Price'])
print(X)

"""
# prepare configuration for cross validation test harness
seed = 7
# prepare models
models = []

models.append(('NB', LinearRegression()))
models.append(('Forest', RandomForestRegressor(n_estimators=15)))
models.append(('Ridge', linear_model.Ridge(alpha=.5)))
models.append(('RidgeCV', linear_model.RidgeCV(alphas=[0.1, 1.0, 10.0], cv=3)))
models.append(('Lasso', linear_model.Lasso(alpha=0.1)))
models.append(('SGD', linear_model.SGDRegressor(max_iter=1000,tol=None)))
numTests = 1

for name, model in models:
    average = 0
    for i in range(numTests):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        y_train = (y_train * 100000)
        y_test = (y_test * 100000)

        for i in range(len(y_train)):
            y_train[i] = (int)(y_train[i])
            
        for i in range(len(y_test)):
            y_test[i] = (int)(y_test[i])
            
        clf = model
        clf.fit(X_train, y_train)
        score = clf.score(X_test, y_test)
        average += score
    print("Confidence: " + name + ": " + str(average/numTests))
"""
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

y_train = (y_train * 100000)
y_test = (y_test * 100000)

for i in range(len(y_train)):
    y_train[i] = (int)(y_train[i])
    
for i in range(len(y_test)):
    y_test[i] = (int)(y_test[i])
      

for i in range(len(X_test)):
  
    clf = RandomForestRegressor(n_estimators=15)
    clf.fit(X_train, y_train)
    predict_me = np.array(X_test[i])
    predict_me = predict_me.reshape(-1, len(predict_me))
    predictPrice = clf.predict(predict_me)
    actualPrice = y_test[i]+.0018
    diff = predictPrice - actualPrice
    if ((diff / actualPrice)*100 > 800):
        print ("Cat: " + str(X_test[i][0]) + " is " + str((diff / actualPrice)*100) + "% off")
        print("It is being sold for: " + str(actualPrice/100000) + " but should be " + str(predictPrice/100000))
"""
clf = RandomForestRegressor(n_estimators=15)
clf.fit(X_train, y_train)
print(clf.score(X_test, y_test))
"""
