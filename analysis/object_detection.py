from ultralytics import YOLO
import cv2
import numpy as np
from typing import List, Dict

def analyze_frames(frames: List[np.ndarray], model_size: str = 'n') -> Dict[str, float]:
    """This function is for analyzing frames for person vs object dominance"""
    model = YOLO(f'yolov8{model_size}.pt')
    person_class = 0 
    person_count = 0
    object_count = 0

    # defining the batch size
    batch_size = 8
    for i in range(0, len(frames), batch_size):
        batch = frames[i:i + batch_size]
        
        results = model(batch, verbose=False)

        for result in results:
            for box in result.boxes:
                cls = int(box.cls[0])
                if cls == person_class:
                    person_count += 1
                else:
                    object_count += 1

    total = person_count + object_count
    return {
        'person_count': person_count,
        'object_count': object_count,
        'person_ratio': person_count / total if total > 0 else 0,
        'object_ratio': object_count / total if total > 0 else 0,
        'dominance': 'person' if person_count > object_count else 'object'
    }