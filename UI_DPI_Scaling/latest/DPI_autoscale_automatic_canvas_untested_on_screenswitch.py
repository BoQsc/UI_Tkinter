import tkinter as tk
import sys
import math

class AutoScaleCanvas(tk.Canvas):
    def __init__(self, master, base_dpi=96, **kwargs):
        super().__init__(master, **kwargs)
        self.base_dpi = base_dpi
        # Compute scaling factor once at startup.
        self.scale_factor = self.winfo_fpixels("1i") / self.base_dpi
        # We only want to apply scaling once per redraw.
        self.scaled = False
        # Bind a configure event to trigger a redraw.
        self.bind("<Configure>", lambda e: self.event_generate("<<Redraw>>"))

class DPIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DPI Scaling Demo")
        self.canvas = AutoScaleCanvas(root, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Design parameters (as if at 96 DPI)
        self.design_dark_height = 80
        self.design_light_height = 50
        self.debug_tag = "debug"
        
        # Bind custom and standard events.
        self.canvas.bind("<<Redraw>>", lambda e: self.update_ui())
        self.root.bind("<Motion>", lambda e: self.update_debug())
        self.root.bind("<F11>", lambda e: self.toggle_fullscreen())
        
        # Initial draw.
        self.update_ui()

    def estimate_physical_dpi(self):
        try:
            mm_width = self.root.winfo_screenmmwidth()
            if mm_width <= 0:
                return 96
            return int(self.root.winfo_screenwidth() / (mm_width / 25.4))
        except Exception:
            return 96

    def calculate_light_width_pct(self, design_width):
        physical_dpi = self.estimate_physical_dpi()
        return 50 if design_width < 800 or physical_dpi > 150 else 70

    def update_ui(self):
        # Get the current scaling factor from our custom canvas.
        scaling = self.canvas.scale_factor
        
        # Compute the window's design dimensions.
        design_width = self.root.winfo_width() / scaling
        design_height = self.root.winfo_height() / scaling
        light_pct = self.calculate_light_width_pct(design_width)
        
        # Clear the canvas.
        self.canvas.delete("all")
        
        # Draw dark rectangle at the bottom.
        dark_y = design_height - self.design_dark_height
        self.canvas.create_rectangle(0, dark_y, design_width, design_height,
                                     fill="#1A5276", tags="all")
        
        # Draw light rectangle (width as percentage).
        light_width = design_width * (light_pct / 100)
        self.canvas.create_rectangle(0, dark_y, light_width, dark_y + self.design_light_height,
                                     fill="#85C1E9", tags="all")
        
        # Draw debug text.
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
        
        # Apply uniform scaling to all drawn items.
        # (Since our items were created in design coordinates, this maps them to actual pixels.)
        self.canvas.scale("all", 0, 0, scaling, scaling)
        # Mark as scaled so we don't reapply repeatedly.
        self.canvas.scaled = True

    def update_debug(self):
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

    def toggle_fullscreen(self):
        is_full = self.root.attributes("-fullscreen")
        self.root.attributes("-fullscreen", not is_full)

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
