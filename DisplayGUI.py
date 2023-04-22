import tkinter as tk
from RealtimeVideo import run_video, add_frame_to_label
from ColorEditor import change_color, rgb_to_name, set_artificial_bound
from ColorUIElement import ColorUIElement
import threading
from queue import Queue
import numpy as np


find_bgr = [0, 0, 0]
new_bgr = [0, 0, 0]


def renderHeader(UI):
    headerFrame = tk.Label(master=UI, width=1600, height=100, bg="red")
    titleLabel = tk.Label(headerFrame, text="Camera Color Conversion")
    titleLabel.pack()
    
    temp_button = tk.Button(headerFrame, height=1, width=18, bg="white", text="Refresh Frame")
    temp_button.pack(side=tk.RIGHT)

    scale = tk.Scale(master=headerFrame, from_=0, to=255, orient=tk.HORIZONTAL, length=200,
                     command=lambda new_val:set_artificial_bound(new_val))
    scale.pack(side=tk.LEFT)
    scale.set(30)

    return headerFrame


def renderColorPallete(UI):
    palleteFrame = tk.Frame(master=UI, width=1600, height=200, bg="yellow")

    return palleteFrame


def print_color(color_val):
    print(color_val)


def set_global_rgb_vals(rgb_to_find, set_as_rgb):
    global find_bgr, new_bgr
    find_bgr = rgb_to_find
    find_bgr[0], find_bgr[2] = find_bgr[2], find_bgr[0]
    new_bgr = set_as_rgb
    new_bgr[0], new_bgr[2] = new_bgr[2], new_bgr[0]


def renderButtons(color_pallete_frame, button_array):
    for button in button_array:
        new_element = ColorUIElement(color_pallete_frame, button)
        new_element.set_button_command(lambda a, b:set_global_rgb_vals(a, b))


def main():
    UI = tk.Tk()
    frame_queue = Queue(300)
    rgb_queue = Queue(2)
    changed_frames_queue = Queue(300)

    master_pallette_frame = renderColorPallete(UI)
    master_pallette_frame.pack(fill=tk.BOTH, side=tk.BOTTOM)
    colorPalletteFrame = renderColorPallete(master_pallette_frame)
    colorPalletteFrame.pack(fill=tk.BOTH, side=tk.BOTTOM)

    customCameraTitleFrame = renderHeader(UI)

    beforeColorChangeFrame = tk.Frame(master=UI, width=800, height=600, bg="black")
    video_label = tk.Label(master=beforeColorChangeFrame)
    video_label.pack()

    afterColorChangeFrame = tk.Frame(master=UI, width=800, height=600, bg="black")
    second_video = tk.Label(master=afterColorChangeFrame)
    second_video.pack()
    
    customCameraTitleFrame.pack(fill=tk.BOTH, side=tk.TOP)

    beforeColorChangeFrame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
    # beforeColorChangeFrame.pack_propagate(False)

    afterColorChangeFrame.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)
    # afterColorChangeFrame.pack_propagate(False)

    video_input_thread = threading.Thread(target=run_video, args=(frame_queue, rgb_queue))
    video_input_thread.start()

    # Input colors as BGR
    while True:
        global find_bgr, new_bgr
        color_frame = frame_queue.get()
        color_change_thread = threading.Thread(target=change_color, args=(color_frame, find_bgr, new_bgr, changed_frames_queue))
        color_change_thread.start()

        add_frame_to_label(video_label, color_frame)

        color_change_thread.join()
        changed_frame = changed_frames_queue.get()
        add_frame_to_label(second_video, changed_frame)

        if rgb_queue.qsize() > 0:
            rgb_array = rgb_queue.get()
            colorPalletteFrame.destroy()
            colorPalletteFrame = renderColorPallete(master_pallette_frame)
            colorPalletteFrame.pack(fill=tk.BOTH)

            if len(rgb_array) > 0 and rgb_array is not None:
                renderButtons(colorPalletteFrame, rgb_array)

        # Goes after all updates
        UI.update()

    video_input_thread.join()


if __name__ == "__main__":
    main()
