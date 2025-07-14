from flask import Flask, render_template, Response, jsonify
import cv2
import mediapipe as mp

app = Flask(__name__)

# Globals to store status
face_status = "No face detected"
finger_count = 0

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_face = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
face_detector = mp_face.FaceDetection(min_detection_confidence=0.7)

FINGER_TIPS = [8, 12, 16, 20]

def count_fingers(hand_landmarks):
    fingers_up = 0
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers_up += 1
    for tip in FINGER_TIPS:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers_up += 1
    return fingers_up

def generate_frames():
    global face_status, finger_count
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_results = face_detector.process(rgb)
        hand_results = hands.process(rgb)

        # Face detection
        if face_results.detections:
            face_status = "✅ Face detected"
        else:
            face_status = "No face detected"

        # Hand detection
        finger_count = 0
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                finger_count += count_fingers(hand_landmarks)

        # Print to terminal
        print(f"{face_status} | 🖐️ Fingers: {finger_count}")

        # Draw overlay
        cv2.putText(frame, face_status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        cv2.putText(frame, f"🖐️ Fingers: {finger_count}", (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/status')
def status():
    return jsonify({
        "face_status": face_status,
        "finger_count": finger_count
    })

if __name__ == '__main__':
    app.run(debug=True)
