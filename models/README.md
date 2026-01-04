# Models Directory

This directory contains the pre-trained model files for the Action Recognition system.

## Model File

Place your pre-trained CNN+LSTM model file here:

- **File name**: `cnn_lstm_action.h5`
- **Format**: Keras H5 format
- **Classes**: 7 action classes (Walking, Running, Jumping, Boxing, Handclapping, Handwaving, Jogging)
- **Input shape**: `(batch_size, num_frames, 224, 224, 3)`
- **Output shape**: `(batch_size, 7)` - 7 class probabilities

## Model Requirements

The model should be:
- A Keras/TensorFlow model saved in H5 format
- Trained to recognize 7 action classes
- Accept input sequences of frames with shape `(num_frames, 224, 224, 3)`
- Output softmax probabilities for each of the 7 classes

## Usage

The model is automatically loaded by the backend service (`backend/models_service.py`) when the FastAPI application starts.

## Note

Make sure to place the `cnn_lstm_action.h5` file in this directory before running the application.

