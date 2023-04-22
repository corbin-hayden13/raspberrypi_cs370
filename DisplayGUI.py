import tkinter as tk
from RealtimeVideo import run_video, add_frame_to_label
from ColorEditor import change_color, rgb_to_name
import threading
from queue import Queue


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
    beforeColorChangeFrame.pack_propagate(False)

    afterColorChangeFrame.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)
    afterColorChangeFrame.pack_propagate(False)

    video_input_thread = threading.Thread(target=run_video, args=(frame_queue, rgb_queue))
    video_input_thread.start()

    while True:
        color_frame = frame_queue.get()
        color_change_thread = threading.Thread(target=change_color, args=(color_frame, [255, 255, 255], [100, 100, 100], changed_frames_queue))
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
                buttons = []
                for rgb_val in rgb_array:
                    buttons.append(rgb_to_name(rgb_val))

                renderButtons(colorPalletteFrame, buttons)

        # Goes after all updates
        UI.update()

    video_input_thread.join()


if __name__ == "__main__":
    main()
