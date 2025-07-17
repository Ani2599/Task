import cv2
import numpy as np
from typing import List

def frame_to_hist(frame: np.ndarray) -> np.ndarray:
    """Convert frame to normalized histogram"""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    return cv2.normalize(hist, hist).flatten()

def detect_cuts(frames: List[np.ndarray], threshold: float = 30.0) -> int:
    """For Detecting number of hard cuts in video frames"""
    cut_count = 0
    prev_hist = None

    for frame in frames:
        curr_hist = frame_to_hist(frame)

        if prev_hist is not None:
            # Using correlation method which works well for shot detection
            diff = cv2.compareHist(prev_hist, curr_hist, cv2.HISTCMP_CORREL)

            # Convert similarity to difference score
            diff_score = (1 - diff) * 100

            if diff_score > threshold:
                cut_count += 1

        prev_hist = curr_hist

    return cut_count