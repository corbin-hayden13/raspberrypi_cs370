"""
Source 1 - https://www.tutorialspoint.com/how-to-get-the-screen-size-in-tkinter#:~:text=In%20order%20to%20get%20the,of%20the%20screen%20in%20pixels. 
Source 2 - https://www.tutorialspoint.com/how-can-i-prevent-a-window-from-being-resized-with-tkinter. 
Source 3 - https://www.plus2net.com/python/tkinter-rowconfigure.php. 
"""

import tkinter as tk
from RealtimeVideo import run_video, add_frame_to_label
from ColorEditor import change_color, rgb_to_name, set_artificial_bound
from ColorUIElement import ColorUIElement
import threading
from queue import Queue


master_bgr_dict = {}


def renderHeader(UI, screen_width, screen_height):
    headerFrame = tk.Frame(master=UI, width=int(screen_width), height=int(screen_height/16), bg="red")
    
    temp_button = tk.Button(headerFrame, height=1, width=18, bg="white", text="Refresh Frame")
    temp_button.pack(fill=tk.BOTH, side=tk.RIGHT)

    scale = tk.Scale(master=headerFrame, from_=0, to=255, orient=tk.HORIZONTAL, length=200,
                     command=lambda new_val:set_artificial_bound(new_val))
    scale.pack(fill=tk.BOTH, side=tk.LEFT)
    scale.set(30)

    return headerFrame


def renderColorPalette(UI, screen_width, screen_height):
    paletteFrame = tk.Frame(master=UI, width=int(screen_width), height=int(screen_height/6), bg="yellow")
    return paletteFrame


def print_color(color_val):
    print(color_val)


def set_global_rgb_vals(color_ui_element):
    global master_bgr_dict
    master_bgr_dict[color_ui_element.color_name] = (color_ui_element.org_bgr, color_ui_element.bgr)


def renderButtons(color_palette_frame, button_array, button_label_width, button_label_height):
    for button in button_array:
        new_element = ColorUIElement(color_palette_frame, button, button_label_width, button_label_height)
        new_element.set_button_command(lambda a: set_global_rgb_vals(a))


def main():
    UI = tk.Tk()
    UI.resizable(width=False, height=False)     # Used from Tutorials Point
    
    screen_width = UI.winfo_screenwidth() - int((UI.winfo_screenwidth()) / 24)     # Adapted from Tutorials Point
    screen_height = UI.winfo_screenheight() - int((UI.winfo_screenheight()) / 8)     # Adapted from Tutorials Point
    UI.geometry("%dx%d" % (screen_width, screen_height))     # Used from Tutorials Point
    
    frame_queue = Queue(300)
    rgb_queue = Queue(2)
    changed_frames_queue = Queue(300)

    customCameraTitleFrame = renderHeader(UI, screen_width, screen_height)

    beforeColorChangeFrame = tk.Frame(master=UI, width=int(screen_width), height=int(screen_height / 2) +
                                                                                 int(screen_height / 8), bg="blue")
    video_label = tk.Label(master=beforeColorChangeFrame)
    video_label.pack(fill=tk.BOTH, side=tk.LEFT)
    second_video = tk.Label(master=beforeColorChangeFrame)
    second_video.pack(fill=tk.BOTH, side=tk.RIGHT)

    colorPalletteFrame = renderColorPalette(UI, screen_width, screen_width)
    
    UI.rowconfigure(0, weight=2)     # Adapted from plus2net
    UI.rowconfigure(1, weight=1)     # Adapted from plus2net
    UI.rowconfigure(2, weight=2)     # Adapted from plus2net
    
    UI.columnconfigure(0, weight=1)     # Adapted from plus2net
    UI.columnconfigure(1, weight=1)     # Adapted from plus2net
    
    customCameraTitleFrame.grid(row=0, column=0)

    beforeColorChangeFrame.grid(row=1, column=0)
    
    colorPalletteFrame.grid(row=2, column=0)

    video_input_thread = threading.Thread(target=run_video, args=(frame_queue, rgb_queue, screen_width, screen_height))
    video_input_thread.start()

    # Input colors as BGR
    while True:
        global master_bgr_dict
        color_frame = frame_queue.get()
        color_change_thread = threading.Thread(target=change_color, args=(color_frame, master_bgr_dict,
                                                                          changed_frames_queue))
        color_change_thread.start()

        add_frame_to_label(video_label, color_frame)

        color_change_thread.join()
        changed_frame = changed_frames_queue.get()
        add_frame_to_label(second_video, changed_frame)

        if rgb_queue.qsize() > 0:
            rgb_array = rgb_queue.get()
            colorPalletteFrame.destroy()
            colorPalletteFrame = renderColorPalette(UI, screen_width, screen_width)
            colorPalletteFrame.grid(row=2, column=0)

            if len(rgb_array) > 0 and rgb_array is not None:
                renderButtons(colorPalletteFrame, rgb_array, int(screen_width / 77), 2)

        # Goes after all updates
        UI.update()

    video_input_thread.join()


if __name__ == "__main__":
    main()
