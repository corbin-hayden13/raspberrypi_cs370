"""
1 - https://stackoverflow.com/questions/48364168/flickering-video-in-opencv-tkinter-integration
"""

import tkinter as tk
import cv2
from RealtimeVideo import run_video, get_Common_RGB_Array
import threading

def renderHeader(UI):
    headerFrame = tk.Label(master=UI, width=1600, height=100, bg="red")
    titleLabel = tk.Label(headerFrame, text="Camera Color Conversion")
    titleLabel.pack()
    
    temp_button = tk.Button(headerFrame, height=1, width=18, bg="white", text="Refresh Frame")
    temp_button.pack(side=tk.RIGHT)

    return headerFrame


def renderColorPallete(UI):
    palleteFrame = tk.Frame(master=UI, width=1600, height=200, bg="yellow")

    return palleteFrame


def print_color(color_val):
    print(color_val)


def renderButtons(color_pallete_frame, button_array):
    width = 18
    height = 6
    for button in button_array:
        temp_frame = tk.Frame(master=color_pallete_frame)
        
        temp_color_hex_input_field_G = tk.Text(temp_frame, height=3, width=width)
        temp_color_hex_input_field_G.insert("1.0", button + " 3")
        temp_color_hex_input_field_G.pack(side=tk.BOTTOM)
        
        temp_color_hex_input_field_B = tk.Text(temp_frame, height=3, width=width)
        temp_color_hex_input_field_B.insert("1.0", button + " 2")
        temp_color_hex_input_field_B.pack(side=tk.BOTTOM)
        
        temp_color_hex_input_field_R = tk.Text(temp_frame, height=3, width=width)
        temp_color_hex_input_field_R.insert("1.0", button + " 1")
        temp_color_hex_input_field_R.pack(side=tk.BOTTOM)
        
        temp_button = tk.Button(temp_frame, height=height, width=width, bg=button, text=button, command=lambda color=button:print_color(color))
        temp_button.pack(side=tk.LEFT)

        temp_frame.pack(side=tk.LEFT)


def main():
    UI = tk.Tk()

    customCameraTitleFrame = renderHeader(UI)

    colorPalletteFrame = renderColorPallete(UI)

    colors_array = get_Common_RGB_Array()
    renderButtons(colorPalletteFrame, colors_array)

    beforeColorChangeFrame = tk.Frame(master=UI, width=800, height=600, bg="black")
    video_label = tk.Label(master=beforeColorChangeFrame)
    video_label.pack()

    afterColorChangeFrame = tk.Frame(master=UI, width=800, height=600, bg="black")
    afterColorChangeLabel = tk.Label(afterColorChangeFrame, text="Video After Color Changes")
    afterColorChangeLabel.pack()
    
    customCameraTitleFrame.pack(fill=tk.BOTH, side=tk.TOP)

    colorPalletteFrame.pack(fill=tk.BOTH, side=tk.BOTTOM)
    colorPalletteFrame.pack_propagate(False)

    beforeColorChangeFrame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
    beforeColorChangeFrame.pack_propagate(False)

    afterColorChangeFrame.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)
    afterColorChangeFrame.pack_propagate(False)

    video_input_thread = threading.Thread(target=run_video, args=(video_label,))
    video_input_thread.start()

    # UI.update()
    UI.mainloop()

    video_input_thread.join()


if __name__ == "__main__":
    main()
