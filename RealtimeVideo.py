import numpy as np
import cv2
import math


def get_video_frames(capture_obj, width, height):
    width_by_height = (width, height)
    ret, frame = capture_obj.read()
    if not ret:
        print("Failed to read stream? exiting")
        exit(1)

    frame = cv2.resize(frame, width_by_height)

    colorFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    return frame, colorFrame


def main():
    width = 960
    height = 540

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to get from camera, exiting")
        exit(1)

    while True:
        frame, colorFrame = get_video_frames(cap, width, height)

        cv2.imshow('frame', frame)

        # cv2 requries this key to output properly
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cv2.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

