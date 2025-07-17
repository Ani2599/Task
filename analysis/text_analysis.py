import pytesseract
from PIL import Image
import cv2
import numpy as np
from typing import List

MIN_CONFIDENCE = 60.0

def preprocess_frame(frame: np.ndarray) -> Image:
    """Convert and enhance frame for better OCR results"""
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb_frame)
    # Simple contrast enhancement - helps with OCR
    return pil_img.point(lambda x: 0 if x < 50 else 255 if x > 200 else x)

def analyze_frames(frames: List[np.ndarray], min_confidence: float = MIN_CONFIDENCE) -> float:
    """Function for calculating ratio of frames containing detectable text"""
    text_frames = 0

    for frame in frames:
        try:
            processed_img = preprocess_frame(frame)
            data = pytesseract.image_to_data(
                processed_img,
                output_type=pytesseract.Output.DICT
            )
            # Check if any text detection meets confidence threshold
            confidences = [float(c) for c in data['conf'] if c != '-1']
            if any(c >= min_confidence for c in confidences):
                text_frames += 1
        except Exception:
            continue

    return text_frames / len(frames) if frames else 0.0