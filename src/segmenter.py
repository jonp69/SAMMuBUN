"""
Segmenter - Generates masks from frames.
Responsibility: Frame → mask (can use simple or AI methods)
"""
import cv2
import numpy as np
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class Segmenter:
    """Generates segmentation masks from frames."""
    
    def __init__(self, method: str = 'simple'):
        """
        Args:
            method: 'simple' for threshold, 'sam' for Segment Anything (future)
        """
        self.method = method
        self._sam_model = None  # Lazy load when needed
        
    def segment(self, frame: np.ndarray, initial_mask: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Generate segmentation mask for a frame.
        
        Args:
            frame: Input frame (BGR)
            initial_mask: Optional pre-existing mask to use/refine
            
        Returns:
            Binary mask (0 or 255)
        """
        if initial_mask is not None:
            # Use provided mask (resize if needed)
            if initial_mask.shape[:2] != frame.shape[:2]:
                from .mask_utils import resize_mask
                return resize_mask(initial_mask, frame.shape[1], frame.shape[0])
            return initial_mask
        
        # Fallback to simple segmentation
        if self.method == 'simple':
            return self._simple_segment(frame)
        elif self.method == 'sam':
            return self._sam_segment(frame)
        else:
            raise ValueError(f"Unknown segmentation method: {self.method}")
    
    def _simple_segment(self, frame: np.ndarray) -> np.ndarray:
        """Simple threshold-based segmentation."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        return mask
    
    def _sam_segment(self, frame: np.ndarray) -> np.ndarray:
        """SAM-based segmentation (placeholder for future)."""
        if self._sam_model is None:
            logger.warning("SAM not loaded, falling back to simple segmentation")
            return self._simple_segment(frame)
        
        # TODO: Implement SAM segmentation
        # from segment_anything import SamPredictor
        # mask = self._sam_model.predict(frame)
        raise NotImplementedError("SAM segmentation not yet implemented")
