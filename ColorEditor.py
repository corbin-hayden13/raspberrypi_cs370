import cv2
import numpy as np
import pandas as pd


def make_rgb_list(color_table):
    rgb_list = []

    red_list = color_table['Red'].values.tolist()
    green_list = color_table['Green'].values.tolist()
    blue_list = color_table['Blue'].values.tolist()

    for a in range(len(red_list)):
        rgb_list.append([red_list[a], green_list[a], blue_list[a]])

    return rgb_list

color_table = pd.read_excel('tables/tk-colours.xlsx')
color_dict = {}

names = color_table["Name"].values.tolist()
rgb_list = make_rgb_list(color_table)

for a in range(len(names)):
    color_dict[str(rgb_list[a])] = names[a]


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

