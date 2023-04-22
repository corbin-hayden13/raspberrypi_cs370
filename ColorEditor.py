import cv2
import numpy as np
import pandas as pd


color_table = pd.read_excel('tables/tk-colours.xlsx')
color_dict = {}

names = color_table["Name"].values.tolist()
hex_vals = color_table["hex"].values.tolist()

for a in range(len(names)):
    color_dict[hex_vals[a]] = names[a]


def hex_to_name(hex_val):
    return color_dict[hex_val]


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


def rgb_to_hex(rgb_val):
    r = int(rgb_val[0])
    g = int(rgb_val[1])
    b = int(rgb_val[2])
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def rgb_to_name(rgb_val):
    return hex_to_name(rgb_to_hex(rgb_val))

