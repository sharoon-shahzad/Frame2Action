"""
FastAPI Backend for Action Recognition using CNN+LSTM Model
Handles video upload, frame extraction, preprocessing, and model inference
"""

import os
import shutil
import tempfile
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

# Import model service
from models_service import get_model_service, get_action_classes

# Initialize FastAPI application
app = FastAPI(title="Action Recognition API", version="1.0.0")

# Enable CORS to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get project root directory (parent of backend/)
project_root = Path(__file__).parent.parent

# Mount frontend static files directory
frontend_dir = project_root / "frontend"
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

# Get model service instance
model_service = get_model_service()


@app.on_event("startup")
async def startup_event():
    """
    Initialize the model when the FastAPI application starts.
    """
    model_service.load_model()


def extract_frames(video_path: str, num_frames: int = 5) -> np.ndarray:
    """
    Extract N evenly spaced frames from a video file.
    
    Args:
        video_path: Path to the video file
        num_frames: Number of frames to extract (default: 5)
    
    Returns:
        Array of extracted frames with shape (num_frames, height, width, channels)
    
    Raises:
        ValueError: If video is too short or cannot be read
    """
    # Open video file
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        raise ValueError(f"Cannot open video file: {video_path}")
    
    # Get total number of frames and fps
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    if total_frames < num_frames:
        cap.release()
        raise ValueError(
            f"Video too short: has {total_frames} frames, but {num_frames} frames required. "
            f"Please upload a longer video."
        )
    
    if fps <= 0:
        cap.release()
        raise ValueError("Invalid video: cannot determine frame rate")
    
    # Calculate frame indices to extract (evenly spaced)
    frame_indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)
    
    frames = []
    
    # Extract frames at specified indices
    for idx in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        
        if not ret:
            cap.release()
            raise ValueError(f"Failed to read frame at index {idx}")
        
        frames.append(frame)
    
    cap.release()
    
    # Convert list to numpy array
    frames_array = np.array(frames)
    
    return frames_array


def preprocess_frames(frames: np.ndarray, target_size: tuple = (224, 224)) -> np.ndarray:
    """
    Preprocess frames: resize to target size and normalize to [0, 1].
    
    Args:
        frames: Array of frames with shape (num_frames, height, width, channels)
        target_size: Target size for resizing (default: (224, 224))
    
    Returns:
        Preprocessed frames array with shape (1, num_frames, 224, 224, 3)
    """
    processed_frames = []
    
    for frame in frames:
        # Resize frame to target size (224x224)
        resized = cv2.resize(frame, target_size)
        
        # Convert BGR to RGB (OpenCV uses BGR by default)
        rgb_frame = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        
        # Normalize pixel values to [0, 1] range
        normalized = rgb_frame.astype(np.float32) / 255.0
        
        processed_frames.append(normalized)
    
    # Convert to numpy array and add batch dimension
    # Shape: (num_frames, 224, 224, 3) -> (1, num_frames, 224, 224, 3)
    processed_array = np.array(processed_frames)
    processed_array = np.expand_dims(processed_array, axis=0)
    
    return processed_array


@app.post("/upload_video")
async def upload_video(
    file: UploadFile = File(...),
    num_frames: int = 5
):
    """
    REST API endpoint to handle video upload and action recognition.
    
    Args:
        file: Uploaded video file (form-data)
        num_frames: Number of frames to extract (default: 5)
    
    Returns:
        JSON response with status, action, and caption
    
    Raises:
        HTTPException: For various error conditions
    """
    # Validate file type
    allowed_extensions = {".mp4", ".avi", ".mov", ".mkv"}
    file_extension = Path(file.filename).suffix.lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed formats: {', '.join(allowed_extensions)}"
        )
    
    # Create temporary directory for video file
    temp_dir = tempfile.mkdtemp()
    temp_video_path = os.path.join(temp_dir, file.filename)
    
    try:
        # Save uploaded video to temporary location
        with open(temp_video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Extract frames from video
        frames = extract_frames(temp_video_path, num_frames=num_frames)
        
        # Preprocess frames: resize and normalize
        processed_sequence = preprocess_frames(frames, target_size=(224, 224))
        
        # Run model prediction using model service
        predicted_action, confidence = model_service.predict(processed_sequence)
        
        # Generate caption
        caption = f"A person is {predicted_action}"
        
        # Return JSON response
        return JSONResponse(
            status_code=200,
            content={
                "status": "complete",
                "action": predicted_action,
                "caption": caption,
                "confidence": round(confidence, 4)
            }
        )
    
    except ValueError as e:
        # Handle video processing errors (too short, invalid format, etc.)
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Error processing video: {str(e)}"
        )
    
    finally:
        # Clean up temporary video file
        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)
        if os.path.exists(temp_dir):
            try:
                os.rmdir(temp_dir)
            except:
                pass


@app.get("/")
async def root():
    """
    Serve the frontend HTML page.
    """
    index_path = frontend_dir / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {
        "message": "Action Recognition API is running",
        "endpoints": {
            "upload_video": "/upload_video (POST)",
            "health": "/health (GET)",
            "frontend": "/static/index.html (GET)"
        }
    }


@app.get("/health")
async def health():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "model_loaded": model_service.is_loaded()
    }

