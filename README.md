# Video Feature Extraction Tool

##  Features

- **Shot Cut Detection**: Automatically identifies hard cuts between scenes using frame difference analysis
- **Text Presence Analysis**: Detects and extracts text from video frames using OCR (Optical Character Recognition)
- **Object vs Person Dominance**: Analyzes video content using YOLO object detection to determine scene composition
- **Multiple Interfaces**: Command-line tool, Streamlit web app, and FastAPI backend
- **JSON Export**: Export analysis results in structured JSON format

## Prerequisites

### System Requirements
- Python 3.7 or higher
- Tesseract OCR engine
- Sufficient RAM for video processing (recommended: 8GB+)
- GPU support optional but recommended for faster processing

### Tesseract OCR Installation

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install tesseract-ocr
```

**Windows:**
1. Download the installer from [Tesseract GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)
2. Run the installer and follow the setup wizard
3. Add Tesseract to your system PATH

**Verify Installation:**
```bash
tesseract --version
```

## 🛠️ Installation

1. **Create a virtual environment (recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

##  Dependencies

The tool requires the following Python packages (included in requirements.txt):

```
opencv-python
pytesseract
ultralytics
numpy
pandas
streamlit
fastapi
uvicorn
pillow
matplotlib
scipy
```

##  Usage

### Command Line Interface

Extract features from a video file:

```bash
python feature_extractor.py "path/to/your/video.mp4" -o results.json
```

**Parameters:**
- `video_path`: Path to the input video file
- `-o, --output`: Output JSON file path (optional, defaults to `results.json`)

**Example:**
```bash
python feature_extractor.py "D:\computervision\180301_06_B_CityRoam_01.mp4" -o analysis_results.json
```

### Streamlit Web Application

Launch the interactive web interface:

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501` to access the web interface.

**Features:**
- Upload video files through web interface
- Real-time processing visualization
- Interactive results display
- Download results as JSON

### FastAPI Backend

Start the API server:

```bash
uvicorn app1:app --reload
```

The API will be available at `http://localhost:8000`

**API Endpoints:**
- `POST /analyze`: Upload and analyze video files
- `GET /docs`: Interactive API documentation
- `GET /health`: Health check endpoint

## Output Format

The tool generates a JSON file containing:

```json
{
    "height": 1080,
    "height": 1080,
    "fps": 25.0,
    "fps": 25.0,
    "fps": 25.0,
    "frame_count": 359,
    "fps": 25.0,
  },
  },
  "shot_cuts": 0,
  "text_present_ratio": 0.0,
  "object_analysis": {
    "person_count": 414,
    "object_count": 54,
    "person_ratio": 0.8846153846153846,
    "object_ratio": 0.11538461538461539,
    "dominance": "person"
  }
}
```

## Configuration

### Adjusting Detection Sensitivity

You can modify detection parameters in the script:

```python
# Shot cut detection threshold
SHOT_CUT_THRESHOLD = 0.3

# Text detection confidence
TEXT_CONFIDENCE_THRESHOLD = 0.6

# YOLO detection confidence
YOLO_CONFIDENCE_THRESHOLD = 0.5
```

### Supported Video Formats

- MP4 (recommended)
- AVI
- MOV
- WMV
- FLV
- MKV



##  Project Structure

```
video-feature-extraction/
├── feature_extractor.py    # Main CLI script
├── app.py                  # Streamlit web application
├── app1.py                 # FastAPI backend
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── results/               # Output directory for results
```

