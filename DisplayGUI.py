"""
1 - https://stackoverflow.com/questions/48364168/flickering-video-in-opencv-tkinter-integration
"""

import tkinter as tk
import cv2
from RealtimeVideo import get_video_frames
import threading
from PIL import Image, ImageTk


def run_video(video_label):
    width = 960
    height = 540

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to get from camera, exiting")
        exit(1)

    while True:
        frame, colorFrame = get_video_frames(cap, width, height)
        img = Image.fromarray(colorFrame)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.config(image=imgtk)
        video_label.image = imgtk  # 1 - This one line stops flickering

    cap.release()
    cv2.destoryAllWindows()


def renderHeader(UI):
    headerFrame = tk.Label(master=UI, width=1600, height=100, bg="red")
    titleLabel = tk.Label(headerFrame, text="Camera Color Conversion")
    titleLabel.pack()

    return headerFrame


def renderColorPallete(UI):
    palleteFrame = tk.Frame(master=UI, width=1600, height=200, bg="yellow")

    return palleteFrame


def print_color(color_val):
    print(color_val)


def renderButtons(color_pallete_frame, button_array):
    width = 20
    height = width // 2
    for button in button_array:
        temp_frame = tk.Frame(master=color_pallete_frame)
        temp_button = tk.Button(temp_frame, height=height, width=width, bg=button, text=button, command=lambda color=button:print_color(color))
        temp_button.pack(side=tk.LEFT)

        temp_frame.pack(side=tk.LEFT)


def main():
    UI = tk.Tk()

    # customCameraTitleFrame = renderHeader(UI)

    colorPalletteFrame = renderColorPallete(UI)

    colors_array = ["red", "orange", "yellow", "green", "blue", "purple", "black", "brown", "grey", "white"]
    renderButtons(colorPalletteFrame, colors_array)

    beforeColorChangeFrame = tk.Frame(master=UI, width=800, height=600, bg="blue")
    beforeColorChangeLabel = tk.Label(beforeColorChangeFrame, text="Video Before Color Changes")
    video_label = tk.Label(master=beforeColorChangeFrame)
    video_label.pack()
    beforeColorChangeLabel.pack()

    afterColorChangeFrame = tk.Frame(master=UI, width=800, height=600, bg="green")
    afterColorChangeLabel = tk.Label(afterColorChangeFrame, text="Video After Color Changes")
    afterColorChangeLabel.pack()

    # customCameraTitleFrame.pack(fill=tk.BOTH, side=tk.TOP)
    # customCameraTitleFrame.pack_propagate(False)

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

