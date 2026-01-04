"""
Model Service Module
Handles model loading and prediction logic for the Action Recognition system
"""

import os
from pathlib import Path
import tensorflow as tf
from tensorflow import keras
import numpy as np


# Action classes mapping (7 classes)
ACTION_CLASSES = [
    "Walking",
    "Running",
    "Jumping",
    "Boxing",
    "Handclapping",
    "Handwaving",
    "Jogging"
]


class ModelService:
    """
    Service class for managing CNN+LSTM model operations.
    Handles model loading, initialization, and prediction.
    """
    
    def __init__(self, model_path: str = None):
        """
        Initialize the Model Service.
        
        Args:
            model_path: Path to the model file. If None, uses default path.
        """
        self.model = None
        
        # Set default model path (in models/ directory)
        if model_path is None:
            # Get the project root directory (parent of backend/)
            project_root = Path(__file__).parent.parent
            model_path = project_root / "models" / "cnn_lstm_action.h5"
        
        self.model_path = Path(model_path)
    
    def load_model(self):
        """
        Load the pre-trained CNN+LSTM model from disk.
        
        Raises:
            FileNotFoundError: If model file is not found
            RuntimeError: If model loading fails
        """
        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model file '{self.model_path}' not found. "
                f"Please ensure the model file is in the models/ directory."
            )
        
        try:
            self.model = keras.models.load_model(str(self.model_path))
            print(f"Model loaded successfully from {self.model_path}")
            print(f"Model input shape: {self.model.input_shape}")
            print(f"Model output shape: {self.model.output_shape}")
        except Exception as e:
            raise RuntimeError(f"Error loading model: {str(e)}")
    
    def predict(self, sequence: np.ndarray) -> tuple:
        """
        Predict action class from a sequence of preprocessed frames.
        
        Args:
            sequence: Preprocessed frame sequence with shape (1, num_frames, 224, 224, 3)
        
        Returns:
            Tuple of (predicted_action: str, confidence_score: float)
        
        Raises:
            RuntimeError: If model is not loaded
        """
        if self.model is None:
            raise RuntimeError("Model is not loaded. Call load_model() first.")
        
        # Run model inference
        predictions = self.model.predict(sequence, verbose=0)
        
        # Get predicted class index (highest probability)
        predicted_idx = np.argmax(predictions[0])
        
        # Get confidence score
        confidence = float(predictions[0][predicted_idx])
        
        # Map index to action class name
        predicted_action = ACTION_CLASSES[predicted_idx]
        
        return predicted_action, confidence
    
    def is_loaded(self) -> bool:
        """
        Check if model is loaded.
        
        Returns:
            True if model is loaded, False otherwise
        """
        return self.model is not None


# Global model service instance
_model_service = None


def get_model_service(model_path: str = None) -> ModelService:
    """
    Get or create the global model service instance.
    
    Args:
        model_path: Optional path to model file
    
    Returns:
        ModelService instance
    """
    global _model_service
    if _model_service is None:
        _model_service = ModelService(model_path)
    return _model_service


def get_action_classes() -> list:
    """
    Get the list of action classes.
    
    Returns:
        List of action class names
    """
    return ACTION_CLASSES.copy()

