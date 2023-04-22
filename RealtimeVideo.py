"""
Source 1 - https://stackoverflow.com/questions/48364168/flickering-video-in-opencv-tkinter-integration
"""

from PIL import Image, ImageTk
from sklearn.cluster import KMeans
from collections import Counter
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
    video_label.image = imgtk  # Source 1 - This one line stops flickering


def print_Common_RGB_Values(k_cluster):
    width = 300
    palette = np.zeros((50, width, 3), np.uint8)
    
    n_pixels = len(k_cluster.labels_)
    counter = Counter(k_cluster.labels_) # count how many pixels per cluster
    perc = {}
    for i in counter:
        perc[i] = np.round(counter[i]/n_pixels, 2)
    perc = dict(sorted(perc.items()))
    
    step = 0
    
    for idx, centers in enumerate(k_cluster.cluster_centers_): 
        palette[:, step:int(step + perc[idx]*width+1), :] = centers
        step += int(perc[idx]*width+1)

    return k_cluster.cluster_centers_


def run_video(frame_queue, rgb_queue):
    width = 960
    height = 540

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to get from camera, exiting")
        exit(1)

    frame, color_frame = get_video_frames(cap, width, height)
    frame_queue.put(color_frame)
    
    most_common_colors = KMeans(n_clusters=10)     # Used and adapted from a website
    most_common_colors.fit(color_frame.reshape(-1, 3))     # Used and adapted from a website
    if rgb_queue.qsize() <= 0:
        rgb_queue.put(print_Common_RGB_Values(most_common_colors))

    while True:
        frame, color_frame = get_video_frames(cap, width, height)
        frame_queue.put(color_frame)

    cap.release()
    cv2.destoryAllWindows()
