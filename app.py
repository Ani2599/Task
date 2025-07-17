import streamlit as st
import tempfile
import os
import json

from feature_extractor import analyze_video

st.title("Video Feature Extraction")

uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])
sample_rate = st.number_input("Frame sample rate (process every Nth frame)", min_value=1, value=10)

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.info("Processing video. This may take a while...")
    try:
        features = analyze_video(tmp_path, sample_rate)
        st.success("Analysis complete!")
        st.json(features)
    except Exception as e:
        st.error(f"Error during analysis: {e}")

    # Optionally, remove temp file after processing
    os.remove(tmp_path)