# Hand Tracing Project using Python

This project uses your webcam to detect and trace hand landmarks in real time using MediaPipe and OpenCV.

## 📦 Requirements

- **Python 3.7+**: The programming language used for this project.
- **OpenCV (`opencv-python`)**: For capturing webcam video, image processing, and displaying results.
- **MediaPipe (`mediapipe`)**: For detecting and tracking hand and face landmarks.

Install all dependencies with:
```bash
pip install -r requirements.txt
```

## 🛠 Installation

```bash
python -m venv venv
# Activate the virtual environment:
# On PowerShell:
.\venv\Scripts\Activate.ps1
# On CMD:
venv\Scripts\activate.bat

pip install -r requirements.txt
```

Press **Esc** to exit.

## 📸 Features

- **Live webcam detection**: Real-time hand and face detection using your webcam.
- **Finger count**: Counts and displays the number of fingers shown, both on screen and in the terminal.
- **Face detection notice**: Alerts when a face is detected in the frame.
- **Hand landmark tracing**: Visualizes hand landmarks and connections for each detected hand.
- **Extensible utilities**: Placeholder for saving hand trace data for further analysis.

## 📦 Why these packages?

- **OpenCV**: Handles all video capture, frame manipulation, and display tasks.
- **MediaPipe**: Provides robust, real-time hand and face landmark