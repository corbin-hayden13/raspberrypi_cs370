"""
Source 1 - https://www.plus2net.com/python/tkinter-colors.php#google_vignette
"""

import cv2
import numpy as np
import pandas as pd


curr_new_rgb = [0, 0, 0]
new_frame_mask = []

artificial_bound = 0


def set_artificial_bound(new_val):
    global artificial_bound
    artificial_bound = int(new_val)


def make_rgb_list(color_table):
    rgb_list = []

    red_list = color_table['Red'].values.tolist()
    green_list = color_table['Green'].values.tolist()
    blue_list = color_table['Blue'].values.tolist()

    for a in range(len(red_list)):
        rgb_list.append([red_list[a], green_list[a], blue_list[a]])

    return rgb_list


color_table = pd.read_excel('tables/tk-colours.xlsx')  # Source 1
color_dict = {}

names = color_table["Name"].values.tolist()
rgb_list = make_rgb_list(color_table)

for a in range(len(names)):
    color_dict[str(rgb_list[a])] = names[a]


def make_color_mask(color_frame, new_rgb):
    new_row = [new_rgb for pixel in range(len(color_frame[0]))]
    ret_mask = [new_row for row in range(len(color_frame))]

    return ret_mask


def change_color(color_frame, find_rgb, new_rgb, changed_queue):
    global curr_new_rgb, new_frame_mask, artificial_bound
    if curr_new_rgb != new_rgb or new_frame_mask == []:
        curr_new_rgb = new_rgb
        new_frame_mask = make_color_mask(color_frame, new_rgb)
        new_frame_mask = np.array(new_frame_mask, dtype="uint8")

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
    new_frame = cv2.bitwise_and(color_frame, new_frame_mask, mask=mask)
    mask = cv2.bitwise_not(mask)
    new_frame = cv2.bitwise_not(color_frame, new_frame, mask=mask)
    new_frame = cv2.bitwise_not(new_frame)
    changed_queue.put(new_frame)


def rgb_to_name(rgb_val):
    try:
        color_name = color_dict[str(rgb_val)]
        return color_name

    except KeyError:
        min_diff = 255 * 3 + 1
        found_ind = 0
        for a in range(len(rgb_list)):
            temp_diff = abs(sum(rgb_list[a]) - sum(rgb_val))
            if temp_diff < min_diff:
                min_diff = temp_diff
                found_ind = a

        color_name = color_dict[str(rgb_list[found_ind])]
        return color_name
