import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# import the dataset
dataset = pd.read_csv('bouts_out_new.csv')
X = dataset.iloc[ : , 8].values # age column
Y = dataset.iloc[ : , 16].values # blood pressure column

# handle missing data
from sklearn.preprocessing import Imputer
imputer = Imputer() # Use imputer to replace all the missing values with the mean of the columns
X = imputer.fit_transform(X.reshape(-1,1))
Y = imputer.fit_transform(Y.reshape(-1,1))

# split into training and testing
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X.reshape(-1,1), Y.reshape(-1,1), test_size = 0.2)

# Fit the simple linear regression model to training set
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor = regressor.fit(X_train, Y_train)

# Visualize train results
print('Visualize')
plt.scatter(X_train, Y_train, color = 'red')
plt.plot(X_train, regressor.predict(X_train), color = 'blue')
plt.show()

# Visualize the test results
plt.scatter(X_test, Y_test, color = 'red')
plt.plot(X_test, regressor.predict(X_test), color = 'blue')
plt.show()