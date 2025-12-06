"""
File Utilities - Find and save files.
Responsibility: File I/O operations
"""
import cv2
import numpy as np
from pathlib import Path
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)


def find_video(directory: Path) -> Optional[Path]:
    """Find first video file in directory."""
    for ext in [".mp4", ".mkv", ".avi", ".mov"]:
        path = directory / f"input{ext}"
        if path.exists():
            return path
    return None


def find_mask(directory: Path, name: str = "wizard_mask.png") -> Optional[Path]:
    """Find mask file in directory."""
    path = directory / name
    return path if path.exists() else None


def save_image(image: np.ndarray, path: Path):
    """Save single image."""
    path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path), image)
    logger.info(f"Saved image to {path}")


def save_frames(frames: List[np.ndarray], output_dir: Path, prefix: str = "frame"):
    """Save multiple frames with sequential naming."""
    output_dir.mkdir(parents=True, exist_ok=True)
    for idx, frame in enumerate(frames):
        path = output_dir / f"{prefix}_{idx:04d}.png"
        cv2.imwrite(str(path), frame)
    logger.info(f"Saved {len(frames)} frames to {output_dir}")


def load_mask(path: Path) -> np.ndarray:
    """Load grayscale mask from file."""
    return cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
