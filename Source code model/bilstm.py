from keras import models
from keras import optimizers
from keras import layers
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score, f1_score
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from keras import callbacks
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv('audio_features.csv')
#print(df.to_string())
df['feature'] = df['feature'].apply(eval)
# Split features and labels
X = np.array(df['feature'].tolist())
y = df['label']

# Encode labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Split data into training and test sets
X = X.reshape((X.shape[0], 1, X.shape[1]))
#X = X.reshape((X.shape[0], 1, 1, X.shape[1], 1))
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
X_train, X_validation, y_train, y_validation = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

print('X_train: ', X_train.shape)
print('X_validation: ', X_validation.shape)
print('X_test', X_test.shape)
#print("input shape = ", X_train.shape[1], ",", X_train.shape[3])

# Membuat model LSTM
model = models.Sequential()
model.add(layers.Bidirectional(layers.LSTM(128, return_sequences=True,input_shape=(X_train.shape[1], X_train.shape[2]))))
model.add(layers.Bidirectional(layers.LSTM(128)))
# dense layer
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dropout(0.3))
model.add(layers.Dense(4, activation='softmax'))

model.compile(optimizer=optimizers.Nadam(learning_rate=0.0001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
# Train model
callback = callbacks.EarlyStopping(monitor='loss', patience=3)
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_validation, y_validation))

model.summary()
# Evaluate model on test set
y_train_pred = model.predict(X_train)
y_train_pred_classes = np.argmax(y_train_pred, axis=1)
train_accuracy = accuracy_score(y_train, y_train_pred_classes)

y_val_pred = model.predict(X_validation)
y_val_pred_classes = np.argmax(y_val_pred, axis=1)
validation_accuracy = accuracy_score(y_validation, y_val_pred_classes)

# Evaluate model on test set
y_test_pred = model.predict(X_test)
y_test_pred_classes = np.argmax(y_test_pred, axis=1)
test_accuracy = accuracy_score(y_test, y_test_pred_classes)

train_f1 = f1_score(y_train, y_train_pred_classes, average='weighted')
validation_f1 = f1_score(y_validation, y_val_pred_classes, average='weighted')
test_f1 = f1_score(y_test, y_test_pred_classes, average='weighted')

# Print accuracies
print(f'Train Accuracy: {train_accuracy * 100:.2f}%')
print(f'Validation Accuracy: {validation_accuracy * 100:.2f}%')
print(f'Test Accuracy: {test_accuracy * 100:.2f}%')
print(f'Train F-1: {train_f1:.2f}')
print(f'Validation F-1: {validation_f1:.2f}')
print(f'Test F-1: {test_f1:.2f}')

model_json = model.to_json()
with open("modelbilstm.json", "w") as json_file:
    json_file.write(model_json)
model.save_weights("modelbilstm.weights.h5")
print("model saved")

cm = confusion_matrix(y_test, y_test_pred_classes)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=label_encoder.classes_)

# Plot confusion matrix
disp.plot(cmap=plt.cm.Blues)
plt.show()

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')

# Plot training & validation loss values
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')

plt.show()