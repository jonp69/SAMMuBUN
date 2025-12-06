#!/usr/bin/env python3
"""
SAMMuBUN - Simple Video Meme Compositor
Main orchestration - connects the modular pieces
"""
import sys
import logging
from pathlib import Path

# Import our focused modules
from src.video_loader import load_video
from src.segmenter import Segmenter
from src.mask_utils import feather_mask
from src.background_extractor import BackgroundExtractor
from src.foreground_extractor import ForegroundExtractor
from src.file_utils import find_video, find_mask, load_mask, save_image, save_frames

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VideoMemeCompositor:
    """
    Main compositor - orchestrates the pipeline.
    Each step uses a focused module with single responsibility.
    """
    
    def __init__(self, ingest_dir: str = "INGEST", egest_dir: str = "EGEST"):
        self.ingest_dir = Path(ingest_dir)
        self.egest_dir = Path(egest_dir)
        
        # Initialize components (each has one clear job)
        self.segmenter = Segmenter(method='simple')
        self.bg_extractor = BackgroundExtractor(method='average')
        self.fg_extractor = ForegroundExtractor()
        
        logger.info("VideoMemeCompositor initialized")
    
    def process(self):
        """
        Main pipeline - each step is clear and focused.
        Working memory: one step at a time, easy to understand flow.
        """
        logger.info("=== Starting Pipeline ===")
        
        # Step 1: Find inputs
        video_path = find_video(self.ingest_dir)
        if not video_path:
            logger.error("No input video found")
            return
        
        mask_path = find_mask(self.ingest_dir)
        initial_mask = load_mask(mask_path) if mask_path else None
        
        if initial_mask is not None:
            logger.info(f"Using initial mask from {mask_path}")
        else:
            logger.warning("No initial mask - will use automatic segmentation")
        
        # Step 2: Load video
        logger.info("Loading video frames...")
        frames = load_video(str(video_path))
        if len(frames) == 0:
            logger.error("No frames loaded")
            return
        
        # Step 3: Generate masks
        logger.info("Generating masks...")
        masks = []
        for frame in frames:
            mask = self.segmenter.segment(frame, initial_mask)
            mask_feathered = feather_mask(mask, radius=12)
            masks.append(mask_feathered.astype('uint8'))
        
        # Step 4: Extract background
        logger.info("Extracting background...")
        background = self.bg_extractor.extract(frames, masks)
        save_image(background, self.egest_dir / "background.png")
        
        # Step 5: Extract wizard frames
        logger.info("Extracting wizard frames...")
        wizard_frames = self.fg_extractor.extract_all(frames, masks)
        save_frames(wizard_frames, self.egest_dir, prefix="wizard_frame")
        
        logger.info("=== Pipeline Complete ===")
        logger.info(f"Outputs saved to {self.egest_dir}")


if __name__ == "__main__":
    compositor = VideoMemeCompositor(ingest_dir="INGEST", egest_dir="EGEST")
    compositor.process()
