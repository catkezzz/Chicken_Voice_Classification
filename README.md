# Chicken Voice Classification App

## Project Overview
In Indonesia, the consumption of chicken meat and eggs has been increasing year after year. This growth in demand requires the poultry industry to adjust chicken product output efficiently. However, the industry faces a significant challenge due to a shortage of skilled human resources. One crucial factor in ensuring high-quality chicken products is recognizing chicken behavior, which is closely related to their vocalizations. This project focuses on developing a deep learning-based application to recognize chicken vocalizations in real-time to aid the poultry industry.

The application integrates:
- **Deep Learning Models:** Recurrent Neural Networks (RNN) and their variants, including Long Short-Term Memory (LSTM), Bi-LSTM, and Conv2D-LSTM.
- **Mel-Frequency Cepstral Coefficient (MFCC):** For feature extraction from audio.
- **Android Application:** Built using Android Studio.
- **Backend:** Flask API for model inference.

---

## Features
- **Real-time Chicken Behavior Classification**: Recognizes specific chicken vocalizations to understand their behavior.
- **Audio Processing:** Utilizes MFCC for audio feature extraction.
- **Deep Learning Model Comparison:** Experimentation with different architectures and configurations to identify the best-performing model.

---

## Methodology

1. **Data Preparation:**
   - Audio data of chicken vocalizations was preprocessed using MFCC to extract feature characteristics.
   - The MFCC features were averaged and used as input for model training.

2. **Model Training:**
   - Three model types were tested: LSTM, Bi-LSTM, and Conv2D-LSTM.
   - The Conv2D-LSTM model underwent configuration optimization based on:
     - **Number of LSTM Neurons:** 64 vs. 128 units
     - **Activation Functions:** Tanh, Sigmoid, and ReLU
     - **Kernel Sizes:** 1x3, 1x5, and 1x7
     - **Optimization Methods:** Adam, Nadam, RMSProp
     - **Learning Rates:** 1.00×10⁻¹, 1.00×10⁻², 1.00×10⁻³, and 1.00×10⁻⁴

3. **Results:**
   - Two top-performing Conv2D-LSTM models were identified.
   - The best configuration achieved an accuracy of 78% and an F-1 score of 0.78, utilizing:
     - 64 LSTM units
     - Sigmoid activation function
     - RMSProp optimizer
     - 1x3 kernel size
     - Learning rate of 1.00×10⁻³

---

## Application Workflow

1. **Audio Recording:**
   - The Android application records audio in real-time using the WaveRecorder library.

2. **Backend Inference:**
   - The recorded audio which are then sent to the backend to extract MFCC features
   - The Flask API hosts the Conv2D-LSTM model to classify the audio into predefined chicken behaviors.

3. **Real-time Predictions:**
   - The application displays classification results in real-time, updated every 4 seconds.

---

## Application Visualization


## Technical Stack
### Frontend:
- **Language:** Kotlin
- **Platform:** Android Studio

### Backend:
- **Framework:** Flask API
- **Model Hosting:** Conv2D-LSTM trained models

### Libraries and Tools:
- **Audio Processing:** Librosa (MFCC extraction)
- **Machine Learning:** TensorFlow, Keras

---

## Challenges and Solutions
1. **Limited Data for Some Vocalizations:**
   - Addressed by experimenting with multiple model configurations to improve performance.

2. **Noise Handling:**
   - The model struggled with noise, leading to misclassifications. Future improvements include incorporating denoising techniques and augmenting the dataset.

---

## Future Enhancements
- Improve noise recognition and handling.
- Expand the dataset to include more diverse vocalization patterns.
- Add multilingual support and detailed usage instructions.
- Integrate additional behavior recognition beyond vocalizations.

---

## Installation and Usage
### Prerequisites:
- Android Studio installed for running the app.
- Python environment with Flask and dependencies installed for the backend.

### Steps:
1. **Backend Setup:**
   - Clone the repository.
   - Run the Flask API server, python file named app.py
     
2. **Frontend Setup:**
   - Open the Android project in Android Studio.
   - Change the IP to your own Wi-Fi IP
   - Build and run the application on an emulator or device.

3. **Usage:**
   - Record audio using the app.
   - The audio is sent to the backend, processed, and classified in real time.

---

## Contributors
- Catherine Kezia Wijaya (Lead Developer and Researcher)
- Hendry Setiawan, ST, M.Kom (Mentor)

---

## Acknowledgments
- Special thanks to Ma Chung University
---

## Contact
For inquiries or collaboration, please contact Catherine Kezia Wijaya at [catherinekeziaw@mail.com].


