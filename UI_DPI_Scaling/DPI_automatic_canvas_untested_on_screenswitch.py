import tkinter as tk
import sys
import math
from tkinter import font

class DynamicDPIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fixed DPI Monitor")
        self.canvas = tk.Canvas(root, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Base (design) values in our virtual coordinate system.
        # These values are what you’d use for a baseline 96 DPI display.
        self.design_dark_height = 80
        self.design_light_height = 50

        # We'll create our canvas items during each update_ui call.
        self.setup_bindings()
        self.update_ui(force=True)

    def setup_bindings(self):
        self.root.bind("<Configure>", self.on_window_change)
        self.root.bind("<Motion>", self.update_debug)
        self.root.bind("<F11>", self.toggle_fullscreen)

    def get_scaling_factor(self):
        try:
            # Number of pixels per inch on this screen divided by 96 (baseline)
            return self.canvas.winfo_fpixels("1i") / 96
        except Exception:
            return 1.0

    def estimate_physical_dpi(self):
        try:
            mm_width = self.root.winfo_screenmmwidth()
            if mm_width <= 0:
                return 96
            return int(self.root.winfo_screenwidth() / (mm_width / 25.4))
        except Exception:
            return 96

    def calculate_light_width_pct(self, design_width, scaling):
        physical_dpi = self.estimate_physical_dpi()
        # In our design coordinates, if the width is small or DPI is high, use 50%
        if design_width < 800 or physical_dpi > 150:
            return 50
        return 70

    def update_ui(self, force=False):
        scaling = self.get_scaling_factor()
        # Compute our "design" dimensions by dividing the current window size by the scaling factor.
        design_width = self.root.winfo_width() / scaling
        design_height = self.root.winfo_height() / scaling
        
        light_pct = self.calculate_light_width_pct(design_width, scaling)
        
        # Clear all canvas items
        self.canvas.delete("all")
        
        # DARK RECTANGLE:
        # In our design coordinate system, we want the dark rectangle to span the full width
        # and have a fixed height (design_dark_height) at the bottom.
        dark_y = design_height - self.design_dark_height
        self.canvas.create_rectangle(0, dark_y, design_width, design_height, fill="#1A5276")
        
        # LIGHT RECTANGLE:
        # Its width is a percentage of the design width.
        light_width = design_width * (light_pct / 100)
        self.canvas.create_rectangle(0, dark_y, light_width, dark_y + self.design_light_height, fill="#85C1E9")
        
        # DEBUG TEXT:
        debug_text = (
            f"DPI Scaling: {scaling:.2f}x\n"
            f"Physical DPI: ~{self.estimate_physical_dpi()}\n"
            f"Window: {self.root.winfo_width()}x{self.root.winfo_height()}\n"
            f"Light Width: {light_pct}%\n"
            f"Screen: {self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}\n"
            f"Platform: {sys.platform}"
        )
        # We design the text with a baseline font size (9) multiplied by scaling.
        font_size = max(6, int(9 * scaling))
        self.canvas.create_text(10, 10, anchor="nw", text=debug_text,
                                 fill="#333", font=("Consolas", font_size), tags="debug")
        
        # Now apply a uniform scaling to map our design coordinates to actual pixels.
        # This scales every item (identified by tag "all") by the factor "scaling".
        self.canvas.scale("all", 0, 0, scaling, scaling)

    def update_debug(self, event=None):
        scaling = self.get_scaling_factor()
        design_width = self.root.winfo_width() / scaling
        light_pct = self.calculate_light_width_pct(design_width, scaling)
        debug_text = (
            f"DPI Scaling: {scaling:.2f}x\n"
            f"Physical DPI: ~{self.estimate_physical_dpi()}\n"
            f"Window: {self.root.winfo_width()}x{self.root.winfo_height()}\n"
            f"Light Width: {light_pct}%\n"
            f"Screen: {self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}\n"
            f"Platform: {sys.platform}"
        )
        self.canvas.itemconfig("debug", text=debug_text)

    def on_window_change(self, event):
        self.update_ui()

    def toggle_fullscreen(self, event=None):
        is_full = self.root.attributes("-fullscreen")
        self.root.attributes("-fullscreen", not is_full)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x800")
    
    # On Windows, set process DPI awareness for better scaling
    if sys.platform == "win32":
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

    app = DynamicDPIApp(root)
    root.mainloop()
