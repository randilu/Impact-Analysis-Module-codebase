from sklearn.metrics import confusion_matrix, precision_score
from sklearn.model_selection import train_test_split
from keras.layers import Dense, Dropout
from keras.models import Sequential
from keras.regularizers import l2
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# file='/home/randilu/python_pojects/stock-analysis/data/stock-trend/stock_trend_formated_plantations_from_2013_to_2017.csv'
# data = pd.read_csv(file, sep='\,', encoding='utf-8')
file = '/home/randilu/python_pojects/fyp/iam_model/data/processed/kelani_valley_output.csv'
data = pd.read_csv(file, sep='\,', encoding='utf-8')
print(data.head())

x = data.drop(columns=['isImpacted', 'date', 'close', 'close_1', 'impact'])
# y = data['isImpacted']
y = data['isImpacted']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.30, random_state=0)
print(x_train.shape, y_train.shape, x_test.shape, y_test.shape)

# define a sequential Model
model = Sequential()

# randomly some selected neurons were ignored i.e ‘dropped-out’
# Hidden Layer-1
# 'relu' is used for the hidden layer as it provides better performance than the ‘tanh’
model.add(Dense(100, activation='relu', input_dim=2, kernel_regularizer=l2(0.01)))
model.add(Dropout(0.3, noise_shape=None, seed=None))

# Hidden Layer-2
model.add(Dense(100, activation='relu', kernel_regularizer=l2(0.01)))
model.add(Dropout(0.3, noise_shape=None, seed=None))

# sigmoid is used for the output layer as this is a binary classification.
# Output layer
model.add(Dense(1, activation='sigmoid'))

# binary_crossentropy (loss function)is used since only 2 target clased are available
# Other optimizers maintain a single learning rate through out the training process, where as Adam adopts the learning
# rate as the training progresses (adaptive learning rates)
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

model.summary()

# Train the model
# batch_size determines the number of training examples utilized in one iteration(random-ideally 10-124)
model_output = model.fit(x_train, y_train, epochs=600, batch_size=20, verbose=1, validation_data=(x_test, y_test), )
print('Training Accuracy : ', np.mean(model_output.history["acc"]))
print('Validation Accuracy : ', np.mean(model_output.history["val_acc"]))

# Plot training & validation accuracy values
plt.plot(model_output.history['acc'])
plt.plot(model_output.history['val_acc'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

# Plot training & validation loss values
plt.plot(model_output.history['loss'])
plt.plot(model_output.history['val_loss'])
plt.title('model_output loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

# prediction
y_pred = model.predict(x_test)
rounded = [round(x[0]) for x in y_pred]
y_pred1 = np.array(rounded, dtype='int64')

print(confusion_matrix(y_test, y_pred1))

print('Precision : ', precision_score(y_test, y_pred1))

# save the model

# model.save("Calssifier.h5")
