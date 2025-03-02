import tkinter as tk
import sys

class AutoScaleCanvas(tk.Canvas):
    def __init__(self, master, base_dpi=96, **kwargs):
        super().__init__(master, **kwargs)
        self.base_dpi = base_dpi
        # Compute the scaling factor once at startup.
        self.scale_factor = self.winfo_fpixels("1i") / self.base_dpi
        # When resized, trigger a redraw.
        self.bind("<Configure>", lambda e: self.event_generate("<<Redraw>>"))

class DPIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DPI Scaling Demo")
        self.canvas = AutoScaleCanvas(root, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Design parameters (in virtual coordinates assuming 96 DPI)
        self.design_dark_height = 80
        self.design_light_height = 50
        self.debug_tag = "debug"
        
        # Bind events
        self.canvas.bind("<<Redraw>>", self.update_ui)
        self.root.bind("<Motion>", self.update_debug)
        self.root.bind("<F11>", self.toggle_fullscreen)
        
        # Initial draw.
        self.update_ui()

    def estimate_physical_dpi(self):
        try:
            mm_width = self.root.winfo_screenmmwidth()
            return int(self.root.winfo_screenwidth() / (mm_width / 25.4)) if mm_width > 0 else 96
        except Exception:
            return 96

    def calculate_light_width_pct(self, design_width):
        physical_dpi = self.estimate_physical_dpi()
        return 50 if design_width < 800 or physical_dpi > 150 else 70

    def draw_debug_text(self, scaling, light_pct):
        debug_text = (
            f"DPI Scaling: {scaling:.2f}x\n"
            f"Physical DPI: ~{self.estimate_physical_dpi()}\n"
            f"Window: {self.root.winfo_width()}x{self.root.winfo_height()}\n"
            f"Light Width: {light_pct}%\n"
            f"Screen: {self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}\n"
            f"Platform: {sys.platform}"
        )
        font_size = max(6, int(9 * scaling))
        self.canvas.create_text(10, 10, anchor="nw", text=debug_text,
                                 fill="#333", font=("Consolas", font_size),
                                 tags=(self.debug_tag, "all"))

    def update_ui(self, event=None):
        scaling = self.canvas.scale_factor
        design_width = self.root.winfo_width() / scaling
        design_height = self.root.winfo_height() / scaling
        light_pct = self.calculate_light_width_pct(design_width)
        
        # Clear the canvas and redraw everything in design coordinates.
        self.canvas.delete("all")
        dark_y = design_height - self.design_dark_height
        self.canvas.create_rectangle(0, dark_y, design_width, design_height,
                                     fill="#1A5276", tags="all")
        light_width = design_width * (light_pct / 100)
        self.canvas.create_rectangle(0, dark_y, light_width, dark_y + self.design_light_height,
                                     fill="#85C1E9", tags="all")
        self.draw_debug_text(scaling, light_pct)
        
        # Scale all items uniformly from design coordinates to actual pixels.
        self.canvas.scale("all", 0, 0, scaling, scaling)

    def update_debug(self, event=None):
        # Update the debug text in place.
        scaling = self.canvas.scale_factor
        design_width = self.root.winfo_width() / scaling
        light_pct = self.calculate_light_width_pct(design_width)
        debug_text = (
            f"DPI Scaling: {scaling:.2f}x\n"
            f"Physical DPI: ~{self.estimate_physical_dpi()}\n"
            f"Window: {self.root.winfo_width()}x{self.root.winfo_height()}\n"
            f"Light Width: {light_pct}%\n"
            f"Screen: {self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}\n"
            f"Platform: {sys.platform}"
        )
        self.canvas.itemconfig(self.debug_tag, text=debug_text)

    def toggle_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x800")
    if sys.platform == "win32":
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass
    app = DPIApp(root)
    root.mainloop()
