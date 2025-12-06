"""
Video Loader - Handles reading video files into frames.
Responsibility: Load video → return frames
"""
import cv2
import numpy as np
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


def load_video(video_path: str, max_frames: Optional[int] = None) -> List[np.ndarray]:
    """
    Load video frames into memory.
    
    Args:
        video_path: Path to video file
        max_frames: Optional limit on frames to load
        
    Returns:
        List of frames as numpy arrays
    """
    cap = cv2.VideoCapture(video_path)
    frames = []
    count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
        count += 1
        if max_frames and count >= max_frames:
            break
    
    cap.release()
    logger.info(f"Loaded {len(frames)} frames from {video_path}")
    return frames


def get_video_info(video_path: str) -> dict:
    """Get video metadata without loading frames."""
    cap = cv2.VideoCapture(video_path)
    info = {
        'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        'fps': cap.get(cv2.CAP_PROP_FPS),
        'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    }
    cap.release()
    return info
