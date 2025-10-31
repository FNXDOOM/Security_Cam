# Weapon Detection System

A real-time weapon detection system using YOLO (You Only Look Once) object detection to identify weapons and potential security threats.

## Overview

This application uses computer vision and deep learning to detect weapons in video streams. When a weapon is detected in proximity to a person, the system logs this as a violation, records video evidence, and provides detailed descriptions of the incident.

## Features

- Real-time weapon detection using YOLO
- Person-weapon proximity analysis for violation detection
- Video recording of violation events
- Optional advanced violation descriptions using SmolVLM2 (Vision Language Model)
- Web interface for monitoring and configuration
- WebSocket-based real-time updates

## Requirements

- Python 3.10+
- PyTorch
- Ultralytics YOLO
- Flask
- Flask-SocketIO
- OpenCV
- Transformers (optional, for advanced descriptions)

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Activate the virtual environment:
   ```
   venv\Scripts\activate  # On Windows
   ```

2. Run the application:
   ```
   python app.py
   ```

3. Open a web browser and navigate to `http://localhost:5000`

## Configuration

Configuration settings can be modified in `config.py`, including:

- Detection model path
- Class IDs for person and weapon detection
- Confidence thresholds
- Video recording settings

## Project Structure

- `app.py`: Main application entry point
- `core.py`: Core Flask and SocketIO setup
- `detection_loop.py`: YOLO detection processing loop
- `camera.py`: Camera and video stream handling
- `violation_processor.py`: Processing and recording of violations
- `vlm.py`: Vision Language Model for advanced descriptions
- `views.py`: Web interface routes
- `events.py`: WebSocket event handlers
- `state.py`: Application state management

## License

[MIT License](LICENSE)