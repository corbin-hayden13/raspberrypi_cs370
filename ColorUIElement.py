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

    def __init__(self, master, rgb_val, width, height,):
        self.color_name = rgb_to_name(rgb_val)
        self.frame = tk.Frame(master=master)

        self.width = width
        self.height = height

        self.org_rgb = rgb_val
        self.rgb = [0, 0, 0]

        self.r_scale = tk.Scale(self.frame, from_=0, to=255, orient='horizontal', command=lambda new_val:self.set_r(new_val))
        self.g_scale = tk.Scale(self.frame, from_=0, to=255, orient='horizontal', command=lambda new_val:self.set_g(new_val))
        self.b_scale = tk.Scale(self.frame, from_=0, to=255, orient='horizontal', command=lambda new_val:self.set_b(new_val))

        self.color_label = tk.Label(self.frame, width=19, height=2, bg=self.color_name, text=self.color_name)
        self.color_button = tk.Button(self.frame, width=19, height=2, bg=self.color_name, text=self.color_name)

        self.color_label.pack(fill=tk.BOTH)
        self.r_scale.pack(fill=tk.BOTH)
        self.g_scale.pack(fill=tk.BOTH)
        self.b_scale.pack(fill=tk.BOTH)
        self.color_button.pack(fill=tk.BOTH)

        self.frame.pack(fill=tk.BOTH, side=tk.LEFT)

    def set_button_command(self, new_command):
        self.color_button.configure(command=lambda a=self.org_rgb, b=self.rgb:new_command(a, b))
