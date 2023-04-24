import tkinter as tk
from ColorEditor import rgb_to_name

class ColorUIElement:
    def update_button(self):
        self.color_name = rgb_to_name(self.rgb)
        self.color_button.configure(bg=self.color_name, text=self.color_name)

    def set_r(self, new_val):
        self.rgb[0] = int(new_val)
        self.update_button()

    def set_g(self, new_val):
        self.rgb[1] = int(new_val)
        self.update_button()

    def set_b(self, new_val):
        self.rgb[2] = int(new_val)
        self.update_button()

    def __init__(self, master, rgb_val, height=18, width=6):
        self.color_name = rgb_to_name(rgb_val)
        self.frame = tk.Frame(master=master)

        self.height = height
        self.width = width

        self.org_rgb = rgb_val
        self.rgb = [0, 0, 0]

        self.r_scale = tk.Scale(self.frame, from_=0, to=255, orient='horizontal', command=lambda new_val:self.set_r(new_val))
        self.g_scale = tk.Scale(self.frame, from_=0, to=255, orient='horizontal', command=lambda new_val:self.set_g(new_val))
        self.b_scale = tk.Scale(self.frame, from_=0, to=255, orient='horizontal', command=lambda new_val:self.set_b(new_val))

        self.color_label = tk.Label(self.frame, width=20, height=2, bg=self.color_name, text=self.color_name)
        self.color_button = tk.Button(self.frame, height=2, width=20, bg=self.color_name, text=self.color_name)

        self.color_label.pack()
        self.r_scale.pack()
        self.g_scale.pack()
        self.b_scale.pack()
        self.color_button.pack()

        self.frame.pack(side=tk.LEFT)

    def set_button_command(self, new_command):
        self.color_button.configure(command=lambda a=self.org_rgb, b=self.rgb:new_command(a, b))
