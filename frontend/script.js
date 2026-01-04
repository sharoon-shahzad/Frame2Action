/**
 * Frontend JavaScript for Action Recognition Web Application
 * Handles video upload, API communication, and UI updates
 */

// API endpoint configuration
const API_BASE_URL = 'http://localhost:8000';
const UPLOAD_ENDPOINT = `${API_BASE_URL}/upload_video`;

// DOM elements
const videoInput = document.getElementById('videoInput');
const uploadBox = document.getElementById('uploadBox');
const videoPreview = document.getElementById('videoPreview');
const videoPlayer = document.getElementById('videoPlayer');
const removeVideoBtn = document.getElementById('removeVideo');
const uploadBtn = document.getElementById('uploadBtn');
const progressSection = document.getElementById('progressSection');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');
const actionValue = document.getElementById('actionValue');
const captionValue = document.getElementById('captionValue');
const confidenceValue = document.getElementById('confidenceValue');
const errorMessage = document.getElementById('errorMessage');
const resetBtn = document.getElementById('resetBtn');

// Selected video file
let selectedFile = null;

/**
 * Initialize event listeners when page loads
 */
document.addEventListener('DOMContentLoaded', () => {
    // File input change event
    videoInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop events
    uploadBox.addEventListener('dragover', handleDragOver);
    uploadBox.addEventListener('dragleave', handleDragLeave);
    uploadBox.addEventListener('drop', handleDrop);
    
    // Upload button click
    uploadBtn.addEventListener('click', handleUpload);
    
    // Remove video button
    removeVideoBtn.addEventListener('click', resetUpload);
    
    // Reset button
    resetBtn.addEventListener('click', resetAll);
    
    // Click on upload box to trigger file input
    uploadBox.addEventListener('click', () => {
        if (!selectedFile) {
            videoInput.click();
        }
    });
});

/**
 * Handle file selection from input
 */
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        validateAndPreviewVideo(file);
    }
}

/**
 * Handle drag over event
 */
function handleDragOver(event) {
    event.preventDefault();
    event.stopPropagation();
    uploadBox.classList.add('dragover');
}

/**
 * Handle drag leave event
 */
function handleDragLeave(event) {
    event.preventDefault();
    event.stopPropagation();
    uploadBox.classList.remove('dragover');
}

/**
 * Handle drop event
 */
function handleDrop(event) {
    event.preventDefault();
    event.stopPropagation();
    uploadBox.classList.remove('dragover');
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        validateAndPreviewVideo(files[0]);
    }
}

/**
 * Validate video file and show preview
 */
function validateAndPreviewVideo(file) {
    // Validate file type
    const allowedTypes = ['video/mp4', 'video/avi', 'video/quicktime', 'video/x-msvideo'];
    const fileExtension = file.name.split('.').pop().toLowerCase();
    const allowedExtensions = ['mp4', 'avi', 'mov', 'mkv'];
    
    if (!allowedExtensions.includes(fileExtension)) {
        showError('Please select a valid video file (MP4, AVI, MOV, or MKV)');
        return;
    }
    
    // Store selected file
    selectedFile = file;
    
    // Create video preview URL
    const videoURL = URL.createObjectURL(file);
    videoPlayer.src = videoURL;
    
    // Show video preview and hide upload box
    uploadBox.style.display = 'none';
    videoPreview.style.display = 'block';
    
    // Enable upload button
    uploadBtn.disabled = false;
    
    // Hide any previous errors or results
    hideError();
    hideResults();
}

/**
 * Handle video upload and API call
 */
async function handleUpload() {
    if (!selectedFile) {
        showError('Please select a video file first');
        return;
    }
    
    // Hide previous results and errors
    hideResults();
    hideError();
    
    // Show progress indicator
    showProgress();
    
    // Disable upload button during processing
    uploadBtn.disabled = true;
    
    try {
        // Create FormData to send file
        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('num_frames', '5'); // Default: 5 frames
        
        // Send POST request to backend API
        const response = await fetch(UPLOAD_ENDPOINT, {
            method: 'POST',
            body: formData
        });
        
        // Parse JSON response
        const data = await response.json();
        
        // Check if request was successful
        if (!response.ok) {
            throw new Error(data.detail || 'Failed to process video');
        }
        
        // Hide progress and show results
        hideProgress();
        showResults(data);
        
    } catch (error) {
        // Handle errors
        hideProgress();
        showError(error.message || 'An error occurred while processing the video. Please try again.');
        uploadBtn.disabled = false;
    }
}

/**
 * Display prediction results in UI
 */
function showResults(data) {
    // Update result elements with prediction data
    actionValue.textContent = data.action || 'Unknown';
    captionValue.textContent = data.caption || 'No caption available';
    
    // Display confidence if available
    if (data.confidence !== undefined) {
        const confidencePercent = (data.confidence * 100).toFixed(2);
        confidenceValue.textContent = `${confidencePercent}%`;
    } else {
        confidenceValue.textContent = 'N/A';
    }
    
    // Show results section with animation
    resultsSection.style.display = 'block';
}

/**
 * Show progress indicator
 */
function showProgress() {
    progressSection.style.display = 'block';
}

/**
 * Hide progress indicator
 */
function hideProgress() {
    progressSection.style.display = 'none';
}

/**
 * Show error message
 */
function showError(message) {
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
}

/**
 * Hide error message
 */
function hideError() {
    errorSection.style.display = 'none';
}

/**
 * Hide results section
 */
function hideResults() {
    resultsSection.style.display = 'none';
}

/**
 * Reset upload (remove video preview)
 */
function resetUpload() {
    selectedFile = null;
    videoInput.value = '';
    videoPlayer.src = '';
    videoPreview.style.display = 'none';
    uploadBox.style.display = 'block';
    uploadBtn.disabled = true;
    hideError();
    hideResults();
}

/**
 * Reset everything (for "Analyze Another Video" button)
 */
function resetAll() {
    resetUpload();
    hideProgress();
}

