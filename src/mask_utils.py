"""
Mask Utilities - Simple mask operations.
Responsibility: Mask manipulation (feather, resize, combine)
"""
import cv2
import numpy as np


def feather_mask(mask: np.ndarray, radius: int = 12) -> np.ndarray:
    """Smooth mask edges with Gaussian blur."""
    return cv2.GaussianBlur(mask.astype(np.float32), (0, 0), radius)


def resize_mask(mask: np.ndarray, width: int, height: int) -> np.ndarray:
    """Resize mask to target dimensions."""
    return cv2.resize(mask, (width, height), interpolation=cv2.INTER_NEAREST)


def invert_mask(mask: np.ndarray) -> np.ndarray:
    """Invert a binary mask."""
    return 255 - mask


def combine_masks(masks: list, operation: str = 'union') -> np.ndarray:
    """
    Combine multiple masks.
    
    Args:
        masks: List of binary masks
        operation: 'union' (OR) or 'intersection' (AND)
    """
    if not masks:
        raise ValueError("No masks provided")
    
    result = masks[0].copy()
    for mask in masks[1:]:
        if operation == 'union':
            result = cv2.bitwise_or(result, mask)
        elif operation == 'intersection':
            result = cv2.bitwise_and(result, mask)
    
    return result
