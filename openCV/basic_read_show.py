import cv2
import os
import numpy as np

def solve_error(filename):
    file_name = os.path.join(os.path.dirname(__file__), os.path.join('sampleDATA', filename))
    assert os.path.exists(file_name)
    return file_name

def show_image(filename):
    file_name = solve_error(filename)
    img = cv2.imread(file_name)
    cv2.imshow("img", img)
    cv2.waitKey(0)

def read_image(filename):
    file_name = solve_error(filename)
    img = cv2.imread(file_name)
    return img

def play_video(filepath):
    file_name_vid = solve_error(filepath)
    cap = cv2.VideoCapture(file_name_vid)
    while(True):
        isTrue, frame = cap.read()
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Closes when we press "q"
            break

# Only run these when the file is executed directly, not when imported
if __name__ == "__main__":
    show_image("image.png")
    play_video("luffy1.mp4")
