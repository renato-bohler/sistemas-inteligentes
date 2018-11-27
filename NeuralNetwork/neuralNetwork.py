import random
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.neural_network.multilayer_perceptron import MLPRegressor
import pickle

## Load and prepare data
data = pd.read_csv('robot_walk.csv')
sensors = data.iloc[:, [0, 1, 2, 3]]
orientation = data.iloc[:, [4]]
labels = data.iloc[:, [5, 6]]

## Scale data to better results
sensors_values = sensors.values
min_max_sensors_scaler = preprocessing.MinMaxScaler()
x_sensors_scaled = min_max_sensors_scaler.fit_transform(sensors_values)

orientation_values = orientation.values
min_max_orientation_scaler = preprocessing.MinMaxScaler()
x_orientation_scaled = min_max_orientation_scaler.fit_transform(orientation_values)

labels_values = labels.values
min_max_labels_scaler = preprocessing.MinMaxScaler()
labels_scaled = min_max_labels_scaler.fit_transform(labels_values)

## Group inputs
X = np.c_[x_sensors_scaled, x_orientation_scaled]

## Split to have some validation data
X_train, X_validation, y_train, y_validation = train_test_split(X, labels_scaled, test_size=0.2)


neural_network = MLPRegressor(activation='relu', solver='lbfgs', early_stopping=True)

params = {
	"hidden_layer_sizes": [(random.randint(0, 100), random.randint(0, 100)) for k in range(10)]
	}

## Try many hyperparameters combination to try find the best
grid_search = GridSearchCV(neural_network, param_grid=params, cv=5, return_train_score=True, n_jobs=1, verbose=2)

scores = grid_search.fit(X_train, y_train)

print(scores.best_estimator_)
print(scores.best_score_)


## Save model
pickle.dump(grid_search, open('model.sav', 'wb'))

## Save scalers
pickle.dump(min_max_labels_scaler, open('labels_scaler', 'wb'))
pickle.dump(min_max_orientation_scaler, open('orientation_scaler', 'wb'))
pickle.dump(min_max_sensors_scaler, open('sensors_scaler', 'wb'))