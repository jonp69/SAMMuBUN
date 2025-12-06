"""
Background Extractor - Creates background image from video.
Responsibility: Frames + masks → background image
"""
import cv2
import numpy as np
from typing import List
import logging

logger = logging.getLogger(__name__)


class BackgroundExtractor:
    """Extracts clean background from video using masks."""
    
    def __init__(self, method: str = 'average'):
        """
        Args:
            method: 'average', 'median', or 'inpaint' (AI-based, future)
        """
        self.method = method
    
    def extract(self, frames: List[np.ndarray], masks: List[np.ndarray]) -> np.ndarray:
        """
        Extract background from frames using masks.
        
        Args:
            frames: List of video frames
            masks: Corresponding foreground masks (255 = foreground, 0 = background)
            
        Returns:
            Background image
        """
        if len(frames) == 0:
            raise ValueError("No frames provided")
        
        if len(frames) != len(masks):
            raise ValueError("Frame and mask counts must match")
        
        if self.method == 'average':
            return self._average_background(frames, masks)
        elif self.method == 'median':
            return self._median_background(frames, masks)
        else:
            raise ValueError(f"Unknown method: {self.method}")
    
    def _average_background(self, frames: List[np.ndarray], masks: List[np.ndarray]) -> np.ndarray:
        """Average non-masked pixels across frames."""
        h, w = frames[0].shape[:2]
        bg_accum = np.zeros((h, w, 3), dtype=np.float32)
        count_accum = np.zeros((h, w), dtype=np.float32)
        
        for frame, mask in zip(frames, masks):
            # Background is where mask is 0
            bg_region = (mask < 128)
            bg_accum[bg_region] += frame[bg_region].astype(np.float32)
            count_accum[bg_region] += 1
        
        # Avoid division by zero
        count_accum = np.maximum(count_accum, 1)
        background = (bg_accum / count_accum[..., None]).astype(np.uint8)
        
        logger.info("Background extracted via averaging")
        return background
    
    def _median_background(self, frames: List[np.ndarray], masks: List[np.ndarray]) -> np.ndarray:
        """Median of non-masked pixels (more robust to outliers)."""
        # TODO: Implement median extraction
        logger.warning("Median method not yet implemented, using average")
        return self._average_background(frames, masks)
