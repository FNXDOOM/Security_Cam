# Security Camera System

A comprehensive security camera system with motion detection, AI-powered object recognition, and alert management capabilities.

## Project Structure

- **Frontend**: Flask-based web interface for camera monitoring and control
- **Backend**: Django REST API for alert management and media storage

## Requirements

- Python 3.10+
- Dependencies listed in `requirements.txt`
- CUDA-compatible GPU (recommended for optimal performance)

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repository-url>
cd Security_cam
```

### 2. Set up virtual environment

```bash
python -m venv venv
```

#### Activate virtual environment

On Windows:
```bash
venv\Scripts\activate
```

On macOS/Linux:
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the Backend (Django)

```bash
cd Backend
python manage.py migrate
python manage.py runserver
```

The Django backend will be available at http://127.0.0.1:8000/

### 5. Start the Frontend (Flask)

Open a new terminal, activate the virtual environment, and run:

```bash
cd Frontend
python app.py
```

The Flask frontend will be available at http://127.0.0.1:5000/

## Features

- Real-time video monitoring
- Motion detection
- Object recognition using YOLO
- Video recording of security events
- Alert management system
- Web interface for monitoring and configuration

## Configuration

You can modify camera settings and detection parameters in the `Frontend/config.py` file.

## Note:

- Nivida RTX Gpu is necessary to run this project. 
- After git cloning the repo first install the cuda and tensort library for your specific gpu version then pip install for requirements.txt file.
- If don't have rtx gpu use .pt file and in config.py file make the changes in code to use .pt to run this project.
- Model used in this project is used to detect person and weapon.

