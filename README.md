# Action Recognition Web Application

A full-stack web application for recognizing human actions in videos using a CNN+LSTM deep learning model. The system classifies videos into 7 action classes: Walking, Running, Jumping, Boxing, Handclapping, Handwaving, and Jogging.

## Features

- 🎬 **Video Upload**: Upload videos in MP4, AVI, MOV, or MKV format
- 🔍 **Frame Extraction**: Automatically extracts evenly-spaced frames from uploaded videos
- 🤖 **AI Prediction**: Uses pre-trained CNN+LSTM model for action recognition
- 📊 **Real-time Results**: Displays action class, caption, and confidence score
- 🎨 **Modern UI**: Clean, responsive design with smooth animations
- 🚀 **Fast Processing**: Efficient video processing and model inference

## Project Structure

```
Frame2Action/
├── backend/                    # Backend application
│   ├── app.py                 # FastAPI main application
│   └── models_service.py      # Model loading and prediction service
├── frontend/                  # Frontend application
│   ├── index.html            # HTML structure
│   ├── styles.css            # CSS styling
│   └── script.js             # JavaScript for API communication
├── models/                    # Model storage directory
│   └── cnn_lstm_action.h5    # Pre-trained model file (place here)
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── run_server.bat           # Windows startup script
└── run_server.sh            # Linux/Mac startup script
```

## Prerequisites

- Python 3.8 or higher
- The pre-trained model file `cnn_lstm_action.h5` in the `models/` directory

## Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd Frame2Action
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Place the model file**:
   - Copy `cnn_lstm_action.h5` to the `models/` directory
   - The model should be trained on 7 action classes

## Running the Application

### Start the Backend Server

1. **Activate your virtual environment** (if not already activated):
   ```bash
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. **Navigate to the backend directory and run the FastAPI server**:
   ```bash
   cd backend
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```
   
   Or from the project root:
   ```bash
   uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
   ```

   The backend will start at `http://localhost:8000`

3. **Verify the server is running**:
   - Open `http://localhost:8000` in your browser - you should see the frontend
   - Open `http://localhost:8000/health` to check server health

### Open the Frontend

The frontend is automatically served by the FastAPI backend! Simply:

1. **Open your web browser** and navigate to:
   - **Primary**: `http://localhost:8000` (serves the frontend directly)
   - **Alternative**: `http://localhost:8000/static/index.html`

2. **Upload a video**:
   - Click the upload area or drag and drop a video file
   - Supported formats: MP4, AVI, MOV, MKV
   - Click "Upload & Analyze Video" button
   - Wait for the prediction result

**Note**: The frontend is automatically served by the backend, so no separate frontend server is needed.

## API Endpoints

### `POST /upload_video`
Upload a video file for action recognition.

**Request**:
- Method: POST
- Content-Type: multipart/form-data
- Body:
  - `file`: Video file (required)
  - `num_frames`: Number of frames to extract (optional, default: 5)

**Response**:
```json
{
  "status": "complete",
  "action": "Handclapping",
  "caption": "A person is Handclapping",
  "confidence": 0.9567
}
```

### `GET /`
Serves the frontend HTML page or returns API information.

### `GET /health`
Check server health and model loading status.

## How It Works

1. **Video Upload**: User uploads a video file through the frontend
2. **Frame Extraction**: Backend extracts N evenly-spaced frames (default: 5) from the video
3. **Preprocessing**: Frames are resized to 224x224 pixels and normalized to [0, 1] range
4. **Model Inference**: Preprocessed frame sequence is fed into the CNN+LSTM model via the model service
5. **Prediction**: Model predicts the action class with confidence score
6. **Response**: Frontend displays the predicted action and caption

## Architecture

### Backend (`backend/`)
- **app.py**: FastAPI application with video upload endpoint, frame extraction, and preprocessing
- **models_service.py**: Service module for model loading and prediction operations

### Frontend (`frontend/`)
- **index.html**: Single-page application structure
- **styles.css**: Responsive CSS styling
- **script.js**: JavaScript for video upload, API communication, and UI updates

### Models (`models/`)
- **cnn_lstm_action.h5**: Pre-trained CNN+LSTM model file (user must provide)

## Model Requirements

The model file `cnn_lstm_action.h5` should:
- Be a Keras/TensorFlow model
- Accept input shape: `(batch_size, num_frames, 224, 224, 3)`
- Output 7 classes corresponding to: Walking, Running, Jumping, Boxing, Handclapping, Handwaving, Jogging
- Be saved in H5 format using `model.save()`
- Be placed in the `models/` directory

## Troubleshooting

### Model Not Found Error
- Ensure `cnn_lstm_action.h5` is in the `models/` directory (not the project root)
- Check that the file name matches exactly (case-sensitive)

### CORS Errors
- The backend has CORS enabled for all origins by default
- If issues persist, check browser console for specific error messages

### Video Processing Errors
- Ensure video is long enough (at least 5 frames)
- Check that video format is supported (MP4, AVI, MOV, MKV)
- Verify video file is not corrupted

### Port Already in Use
- Change the port in the uvicorn command:
  ```bash
  uvicorn backend.app:app --reload --port 8001
  ```
- Update `API_BASE_URL` in `frontend/script.js` to match

### Import Errors
- Make sure you're running the server from the project root or backend directory
- Ensure all dependencies are installed: `pip install -r requirements.txt`

## Future Enhancements

- Support for more video formats
- Batch video processing
- Video playback with action timeline
- Export prediction results
- Support for more action classes
- Real-time webcam action recognition
- Model versioning system

## License

This project is provided as-is for educational and demonstration purposes.

## Contact

For questions or issues, please refer to the project documentation or create an issue in the repository.
