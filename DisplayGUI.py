import tkinter as tk
import cv2


def show_color1():
    print("red")


def show_color2():
    print("orange")


def show_color3():
    print("yellow")


def show_color4():
    print("green")


def show_color5():
    print("blue")


def show_color6():
    print("purple")


def show_color7():
    print("black")


def show_color8():
    print("brown")


def show_color9():
    print("grey")


def show_color10():
    print("white")


def print_color(color_val):
    print(color_val)


def renderHeader(UI):
    headerFrame = tk.Frame(master=UI, width=1600, height=100, bg="red")
    titleLabel = tk.Label(headerFrame, text="Camera Color Conversion")
    titleLabel.pack()

    return headerFrame


def renderColorPallete(UI):
    palleteFrame = tk.Frame(master=UI, width=1600, height=200, bg="yellow")

    return palleteFrame


def renderButtons(color_pallete_frame, button_array):
    for button in button_array:
        temp_frame = tk.Frame(master=color_pallete_frame)
        temp_button = tk.Button(temp_frame, text=button, command=lambda:print_color(button))
        temp_button.pack(side=tk.LEFT)

        temp_frame.pack(side=tk.LEFT)


def main():
    UI = tk.Tk()

    customCameraTitleFrame = renderHeader(UI)

    colorPalletteFrame = renderColorPallete(UI)

    # colors_array = ["red", "orange", "yellow", "green", "blue", "purple", "black", "brown", "grey", "white"]
    # renderButtons(colorPalletteFrame, colors_array)

    color1 = tk.Button(colorPalletteFrame, text="red", command=show_color1)
    color1.pack(side=tk.LEFT)

    color2 = tk.Button(colorPalletteFrame, text="orange", command=show_color2)
    color2.pack(side=tk.LEFT)

    color3 = tk.Button(colorPalletteFrame, text="yellow", command=show_color3)
    color3.pack(side=tk.LEFT)

    color4 = tk.Button(colorPalletteFrame, text="green", command=show_color4)
    color4.pack(side=tk.LEFT)

    color5 = tk.Button(colorPalletteFrame, text="blue", command=show_color5)
    color5.pack(side=tk.LEFT)

    color6 = tk.Button(colorPalletteFrame, text="purple", command=show_color6)
    color6.pack(side=tk.LEFT)

    color7 = tk.Button(colorPalletteFrame, text="black", command=show_color7)
    color7.pack(side=tk.LEFT)

    color8 = tk.Button(colorPalletteFrame, text="brown", command=show_color8)
    color8.pack(side=tk.LEFT)

    color9 = tk.Button(colorPalletteFrame, text="grey", command=show_color9)
    color9.pack(side=tk.LEFT)

    color10 = tk.Button(colorPalletteFrame, text="white", command=show_color10)
    color10.pack(side=tk.LEFT)

    beforeColorChangeFrame = tk.Frame(master=UI, width=800, height=600, bg="blue")
    beforeColorChangeLabel = tk.Label(beforeColorChangeFrame, text="Video Before Color Changes")
    # BE SURE TO RUN THE VIDEO FRAME ON While True, or only one frame will be captured
    beforeColorChangeLabel.pack()

    afterColorChangeFrame = tk.Frame(master=UI, width=800, height=600, bg="green")
    afterColorChangeLabel = tk.Label(afterColorChangeFrame, text="Video After Color Changes")
    afterColorChangeLabel.pack()

    customCameraTitleFrame.pack(fill=tk.BOTH, side=tk.TOP)
    customCameraTitleFrame.pack_propagate(False)

    colorPalletteFrame.pack(fill=tk.BOTH, side=tk.BOTTOM)
    colorPalletteFrame.pack_propagate(False)

    beforeColorChangeFrame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
    beforeColorChangeFrame.pack_propagate(False)

    afterColorChangeFrame.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)
    afterColorChangeFrame.pack_propagate(False)

    UI.mainloop()


if __name__ == "__main__":
    main()

