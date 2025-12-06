"""
Foreground Extractor - Extracts wizard/subject from frames.
Responsibility: Frame + mask → foreground cutout
"""
import cv2
import numpy as np
from typing import List
import logging

logger = logging.getLogger(__name__)


class ForegroundExtractor:
    """Extracts foreground (wizard) from frames using masks."""
    
    def extract_frame(self, frame: np.ndarray, mask: np.ndarray) -> np.ndarray:
        """
        Extract foreground from single frame.
        
        Args:
            frame: Input frame
            mask: Binary mask (255 = foreground)
            
        Returns:
            Foreground with background zeroed
        """
        return cv2.bitwise_and(frame, frame, mask=mask)
    
    def extract_all(self, frames: List[np.ndarray], masks: List[np.ndarray]) -> List[np.ndarray]:
        """
        Extract foreground from all frames.
        
        Args:
            frames: List of video frames
            masks: Corresponding foreground masks
            
        Returns:
            List of foreground-only frames
        """
        if len(frames) != len(masks):
            raise ValueError("Frame and mask counts must match")
        
        foregrounds = []
        for frame, mask in zip(frames, masks):
            fg = self.extract_frame(frame, mask)
            foregrounds.append(fg)
        
        logger.info(f"Extracted foreground from {len(foregrounds)} frames")
        return foregrounds
