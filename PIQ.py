'''
############################
## Name: Jack Robinson
## Title: PIQ.py => Predict Its Quality
## Description: Predict the quality of wine using Machine Learning
## Date Created: March 14, 2018
############################
'''

import pandas as pd
import matplotlib.pylab as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_predict

df = pd.read_csv('winequality-red.csv', sep=',')
X = df[list(df.columns)[:-1]]
x_count = 0

## Data being tested against
Y = df['quality']

## Breaks Data into Training and Testing datasets for X and Y
X_train, X_test, Y_train, Y_test = train_test_split(X, Y)

## Assigning imported model from sci-kit learn to variable
regressor = LinearRegression()

## Fit, Predict, then Score model
regressor.fit(X_train, Y_train) ## Fit with training data
y_predictions = regressor.predict(X_test) ## Predict Y with testing data from X
scores = cross_val_predict(regressor, X, Y, cv=5)

#print("Test: {}\nPrediction: {}".format(Y_test.iloc[1], y_predictions[1]))
print('Score Mean: {}\nScores: {}'.format(scores.mean(), scores))

count = 1
predicted_true = 0
while count < len(y_predictions):
    if int(y_predictions[count]) == Y_test.iloc[count]:
        predicted_true +=1
    count += 1
print("Number of Successful Predictions: {} out of 400 {}%".format(predicted_true, (predicted_true/len(y_predictions)) * 100))