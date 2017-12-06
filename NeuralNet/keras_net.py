"""Radial Basis Function Network for aproximating non-linear functions
for stewart platform forward kinematics"""

from keras.models import Sequential
from keras.layers import Dense
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import numpy as np
import pickle

f = open("../LUT.txt", "rb")
dataset = pickle.load(f)
f.close()
data_size = len(dataset)
# training set
X1 = np.array(dataset[:int(data_size * .9)][:6])
Y1 = np.array(dataset[:int(data_size * .9)][6:])
# validation/testing set
X2 = np.array(dataset[int(data_size * .9):][:6])
Y2 = np.array(dataset[int(data_size * .9):][6:])

# create model
model = Sequential()
model.add(Dense(20, input_dim=6, init='uniform', activation='tanh'))
model.add(Dense(1, init='uniform', activation='linear'))

# Compile model
model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])

# Fit the model
model.fit(X1, Y1, nb_epoch=5000, batch_size=10,  verbose=2)

# Calculate predictions
PredTestSet = model.predict(X1)
PredValSet = model.predict(X2)

# Save predictions
np.savetxt("trainresults.csv", PredTestSet, delimiter=",")
np.savetxt("valresults.csv", PredValSet, delimiter=",")