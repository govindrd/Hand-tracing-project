import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_face = mp.solutions.face_detection
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
        self.face_detector = self.mp_face.FaceDetection(min_detection_confidence=0.7)
        self.FINGER_TIPS = [8, 12, 16, 20]

    def count_fingers(self, hand_landmarks):
        fingers_up = 0
        if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
            fingers_up += 1
        for tip in self.FINGER_TIPS:
            if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
                fingers_up += 1
        return fingers_up

    def process(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_results = self.face_detector.process(rgb)
        hand_results = self.hands.process(rgb)

        face_detected = bool(face_results.detections)
        total_fingers = 0

        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                total_fingers += self.count_fingers(hand_landmarks)

        return frame, total_fingers, face_detected
