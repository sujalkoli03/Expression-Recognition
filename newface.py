import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array

def load_emotion_model(model_path='./Emotion_Detection.h5'):
    return load_model(model_path)

def detect_emotions(frame, face_classifier, emotion_model, class_labels):
    labels = []
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

        if np.sum([roi_gray]) != 0:
            roi = roi_gray.astype('float') / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            preds = emotion_model.predict(roi)[0]
            label = class_labels[preds.argmax()]
            label_position = (x, y)
            cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        else:
            cv2.putText(frame, 'No Face Found', (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

def main():
    face_classifier = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
    emotion_model = load_emotion_model()
    class_labels = ['(R)Angry', 'Happy', 'Neutral(sadha)', 'Sad', 'Surprise']

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        detect_emotions(frame, face_classifier, emotion_model, class_labels)
        cv2.imshow('Emotion Detector', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
