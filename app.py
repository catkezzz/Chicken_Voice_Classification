from flask import Flask, request, jsonify
import librosa
import librosa.feature
import numpy as np
from keras import models

app = Flask(__name__)

with open('modelconvlstm64,13sigrms001.json', 'r') as json_file:
    model_json = json_file.read()
model = models.model_from_json(model_json)
model.load_weights('modelconvlstm64,13sigrms001.weights.h5')

label = ["Suara ayam pertanda bahaya", "Suara ayam betina marah", "Suara ayam betina memanggil jantan untuk kawin", "Suara ayam betina setelah bertelur"]

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    filepath = 'audio.wav'
    file.save(filepath)

    y, sr = librosa.load(filepath, sr=None)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = np.mean(mfcc.T, axis=0)
    mfcc_mean = mfcc_mean.reshape((1, 1, 1, 13, 1))

    prediksi = model.predict(mfcc_mean)
    index = np.argmax(prediksi)
    confidence = prediksi[0][index] * 100

    result = {
        'prediction': label[index],
        'confidence': confidence
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
