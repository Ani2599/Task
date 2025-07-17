import argparse
import json
import logging
from datetime import datetime
from pathlib import Path

from video_utils import extract_key_frames, get_video_properties
from analysis.shot_detection import detect_cuts
from analysis.text_analysis import analyze_frames as analyze_text_frames
from analysis.object_detection import analyze_frames as analyze_object_frames

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def analyze_video(video_path: str, sample_rate: int = 10) -> dict:
    """This is Main function to analyze video and extract features"""
    logger.info(f"Starting analysis of {video_path}")
    
    # Verify video exists
    if not Path(video_path).exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")
    
    try:
        # Extract frames and basic properties
        frames, props = extract_key_frames(video_path, sample_rate)
        logger.info(f"Extracted {len(frames)} frames from {props['frame_count']} total frames")
        
        # Perform analyses using functions
        features = {
            'metadata': {
                'file_path': str(Path(video_path).absolute()),
                'timestamp': datetime.now().isoformat(),
                'sample_rate': sample_rate,
                **props
            },
            'shot_cuts': detect_cuts(frames, threshold=25.0),
            'text_present_ratio': analyze_text_frames(frames, min_confidence=60.0),
            'object_analysis': analyze_object_frames(frames, model_size='n')
        }
        
        logger.info("Analysis completed successfully")
        return features
    
    except Exception as e:
        logger.error(f"Error analyzing video: {str(e)}")
        raise

def save_results(results: dict, output_path: str = None) -> None:
    """Save results to JSON file"""
    if output_path is None:
        output_path = f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"Results saved to {output_path}")

def main():
    """Command line interface"""
    parser = argparse.ArgumentParser(
        description="Video Feature Extraction Tool",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('video_path', help="Path to video file")
    parser.add_argument('-s', '--sample-rate', type=int, default=10,
                       help="Frame sampling rate (process every Nth frame)")
    parser.add_argument('-o', '--output', help="Output JSON file path")
    
    args = parser.parse_args()
    
    try:
        results = analyze_video(args.video_path, args.sample_rate)
        save_results(results, args.output)
        print(json.dumps(results, indent=2))
    except Exception as e:
        logger.error(f"Failed to process video: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()