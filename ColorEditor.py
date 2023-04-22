import cv2
import numpy as np


def change_color(color_frame, find_rgb, new_rgb, changed_queue):
    artificial_bound = 30

    lower = []
    upper = []

    for a in range(len(find_rgb)):
        sub_val = find_rgb[a] - artificial_bound if find_rgb[a] - artificial_bound > 0 else 0
        add_val = find_rgb[a] + artificial_bound if find_rgb[a] + artificial_bound < 255 else 255

        lower.append(sub_val)
        upper.append(add_val)

    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    mask = cv2.inRange(color_frame, lower, upper)
    new_frame = cv2.bitwise_and(color_frame, color_frame, mask=mask)
    changed_queue.put(new_frame)

