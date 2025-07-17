import cv2
import numpy as np
from typing import List, Tuple

def get_video_properties(video_path: str) -> dict:
    """used for getting basic video properties using OpenCV"""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video file: {video_path}")
    
    props = {
        'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        'fps': cap.get(cv2.CAP_PROP_FPS),
        'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        'duration': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / cap.get(cv2.CAP_PROP_FPS)
    }
    cap.release()
    return props

def extract_key_frames(video_path: str, sample_rate: int = 10) -> Tuple[List[np.ndarray], dict]:
    """
    it extracts frames from video at specified sample rate and returns frames and video properties
    """
    props = get_video_properties(video_path)
    cap = cv2.VideoCapture(video_path)
    frames = []
    frame_idx = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        if frame_idx % sample_rate == 0:
            frames.append(frame.copy())  # Avoid reference issues
        
        frame_idx += 1
    
    cap.release()
    
    if not frames:
        raise ValueError(f"No frames extracted from {video_path}")
    
    return frames, props