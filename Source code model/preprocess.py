import os
import numpy as np
import librosa
from librosa import feature
import pandas as pd

audio_dir = 'E:/Kezia/Kuliah/ta/Suara ayam/semua4detik'

data = []

# Loop
for filename in os.listdir(audio_dir):
    if filename.endswith(".wav"):

        file_path = os.path.join(audio_dir, filename)
        y, sr = librosa.load(file_path, sr=None)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_mean = np.mean(mfcc.T, axis=0)

        # label
        if 'betinakawinpanggiljantan' in filename:
            label = 'memanggil_jantan'
        elif 'suarasetelahbertelur' in filename:
            label = 'setelah_bertelur'
        elif 'ayambetinamarah' in filename:
            label = 'marah'
        elif 'ayamsuarabahaya' in filename:
            label = 'bahaya'
        else:
            continue

        # data list
        data.append([mfcc_mean.tolist(), label])

# DataFrame
df = pd.DataFrame(data, columns=['feature', 'label'])
print(df.to_string())
df.to_csv('audio_features.csv', index=False)
#df.to_excel('data.xlsx')
