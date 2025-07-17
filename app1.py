from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import shutil
import tempfile
import os
import json
import logging
from feature_extractor import analyze_video, save_results

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/analyze-video/")
async def analyze_video_endpoint(
    file: UploadFile = File(...),
    sample_rate: int = Form(10),
    save_json: bool = Form(False)
):
    """
    Upload a video file and extract features.
    """
    try:
        
        temp_dir = tempfile.mkdtemp()
        video_path = os.path.join(temp_dir, file.filename)
        
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"Received file: {file.filename}")

        # Run analysis
        results = analyze_video(video_path, sample_rate=sample_rate)
        
        # Save results if requested
        if save_json:
            output_path = os.path.join(temp_dir, f"result_{file.filename}.json")
            save_results(results, output_path)
            with open(output_path, "r") as f:
                return JSONResponse(content=json.load(f))
        
        return JSONResponse(content=results)
    
    except Exception as e:
        logger.error(f"Error processing video: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})