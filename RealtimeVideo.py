from PIL import Image, ImageTk
import cv2
import numpy as np


def get_video_frames(capture_obj, width, height):
    width_by_height = (width, height)
    ret, frame = capture_obj.read()
    if not ret:
        print("Failed to read stream? exiting")
        exit(1)

    frame = cv2.resize(frame, width_by_height)

    colorFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    return frame, colorFrame


def add_frame_to_label(video_label, color_frame):
    img = Image.fromarray(color_frame)
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.config(image=imgtk)
    video_label.image = imgtk  # 1 - This one line stops flickering


# Color range should be BGR

# ([0, 0, 0], [255, 255, 255])
def change_frame_color(color_frame, old_color_range, new_color):
    lower = np.array(old_color_range[0], dtype="uint8")
    upper = np.array(old_color_range[1], dtype="unit8")

    mask = cv2.inRange(color_frame, lower, upper)


def run_video(video_label):
    width = 960
    height = 540

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to get from camera, exiting")
        exit(1)

    while True:
        frame, color_frame = get_video_frames(cap, width, height)
        add_frame_to_label(video_label, color_frame)

    cap.release()
    cv2.destoryAllWindows()

