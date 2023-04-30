"""
Source 1 - https://stackoverflow.com/questions/48364168/flickering-video-in-opencv-tkinter-integration
Source 2 - https://towardsdatascience.com/finding-most-common-colors-in-python-47ea0767a06a
"""

from EventHandler import EventHandler
from PIL import Image, ImageTk
from sklearn.cluster import KMeans
from collections import Counter
import cv2
import numpy as np


running_video = True


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
    video_label.image = imgtk  # Source 1 - This one line stops flickering

# The following method is adapted from M. Rake Linggar A. on the website Towards Data Science
def get_Common_RGB_Values(color_cluster):
    color_pixels = len(color_cluster.labels_)
    color_cluster_counter = Counter(color_cluster.labels_) # count how many pixels per cluster
    percent_of_color = {}
    for i in color_cluster_counter:
        percent_of_color[i] = np.round(color_cluster_counter[i]/color_pixels, 2)
    percent_of_color = dict(sorted(percent_of_color.items()))

    return color_cluster.cluster_centers_


def get_common_colors(arg_list):
    color_frame, rgb_queue = arg_list
    most_common_colors = KMeans(n_clusters=6)  # Used and adapted from a website
    most_common_colors.fit(color_frame.reshape(-1, 3))  # Used and adapted from a website
    if rgb_queue.qsize() <= 0:
        rgb_queue.put(get_Common_RGB_Values(most_common_colors))


def run_video(frame_queue, rgb_queue, event_queue, screen_width, screen_height):
    global running_video

    handler = EventHandler()
    handler.add_event("get_common_colors", get_common_colors)

    width = int(screen_width / 2)
    height = int(screen_height / 2) + int(screen_height / 8)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to get from camera, exiting")
        exit(1)

    """frame, color_frame = get_video_frames(cap, width, height)
    frame_queue.put(color_frame)

    get_common_colors((color_frame, rgb_queue))"""

    while running_video:
        frame, color_frame = get_video_frames(cap, width, height)
        frame_queue.put(color_frame)

        while event_queue.qsize() > 0:
            handler.handle_event((event_queue.get(), [color_frame, rgb_queue]))

    cap.release()
    cv2.destoryAllWindows()
