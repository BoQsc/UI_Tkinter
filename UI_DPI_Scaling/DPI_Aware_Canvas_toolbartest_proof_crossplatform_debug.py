import tkinter as tk
import sys
import math
import time
import platform

class DPIMonitor:
    def __init__(self):
        self.scaling_history = []
        self.last_update = 0
        self.update_interval = 0.5  # Seconds between DPI checks
        
    def get_scaling_factor(self):
        """Cross-platform scaling factor with refresh rate limit"""
        now = time.time()
        if now - self.last_update < self.update_interval:
            return self.scaling_history[-1]["factor"] if self.scaling_history else 1.0
        
        factor = self._calculate_scaling()
        dpi = round(factor * 96)
        self.scaling_history.append({
            "time": now,
            "factor": factor,
            "dpi": dpi,
            "platform": platform.platform()
        })
        self.last_update = now
        return factor
        
    def _calculate_scaling(self):
        root = tk.Tk()
        root.withdraw()
        
        if sys.platform == 'win32':
            try:
                import ctypes
                ctypes.windll.shcore.SetProcessDpiAwareness(2)
                hdc = ctypes.windll.user32.GetDC(0)
                dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)
                ctypes.windll.user32.ReleaseDC(0, hdc)
                return dpi / 96
            except:
                return root.winfo_fpixels('1i') / 96
        
        elif sys.platform == 'darwin':
            return root.tk.call('tk', 'scaling') / 72 * 96 / 96
        
        else:  # Linux
            return root.winfo_fpixels('1i') / 96

class AdaptiveGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.dpi_monitor = DPIMonitor()
        self.configure_window()
        self.create_widgets()
        self.setup_bindings()
        
    def configure_window(self):
        self.root.title("Adaptive DPI Demo")
        self.root.geometry("1000x600")
        self.is_fullscreen = False
        self.dpi_threshold = 144  # Switch to 50% width above this DPI (1.5x scaling)
        
    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, bg='white', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Graphical elements
        self.dark_rect = self.canvas.create_rectangle(0,0,0,0, fill='#1A5276', outline='')
        self.light_rect = self.canvas.create_rectangle(0,0,0,0, fill='#85C1E9', outline='')
        
        # Debug information
        self.debug_text = self.canvas.create_text(0,0, anchor=tk.NW, fill='white',
                                                font=('Consolas', 10), text="")
        
    def setup_bindings(self):
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Configure>", self.on_resize)
        self.root.bind("<Escape>", lambda e: self.root.attributes('-fullscreen', False))
        self.root.after(100, self.update_display)
        
    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes('-fullscreen', self.is_fullscreen)
        self.update_display()
        
    def on_resize(self, event=None):
        self.root.after(10, self.update_display)
        
    def calculate_dimensions(self):
        current_factor = self.dpi_monitor.get_scaling_factor()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Determine width percentage based on DPI
        width_percent = 0.5 if (current_factor * 96) > self.dpi_threshold else 0.7
        
        return {
            "dark_height": math.floor(80 * current_factor),
            "light_width": math.floor(canvas_width * width_percent),
            "light_height": math.floor(50 * current_factor),
            "width_percent": width_percent,
            "current_factor": current_factor,
            "canvas_size": (canvas_width, canvas_height)
        }
        
    def update_display(self):
        dims = self.calculate_dimensions()
        cw, ch = dims["canvas_size"]
        
        # Update dark toolbar
        self.canvas.coords(self.dark_rect,
                          0, ch - dims["dark_height"],
                          cw, ch)
        
        # Update light rectangle
        self.canvas.coords(self.light_rect,
                          0, ch - dims["dark_height"],
                          dims["light_width"], 
                          ch - dims["dark_height"] + dims["light_height"])
        
        # Update debug info
        debug_content = [
            f"DPI: {round(dims['current_factor'] * 96)} ({dims['current_factor']:.2f}x)",
            f"Width: {dims['width_percent']*100:.0f}% of {cw}px",
            f"Threshold: {self.dpi_threshold} DPI",
            f"Platform: {platform.platform()}",
            "--- History ---"
        ]
        
        # Show last 3 DPI changes
        for entry in self.dpi_monitor.scaling_history[-3:]:
            debug_content.append(
                f"{time.strftime('%H:%M:%S', time.localtime(entry['time']))} "
                f"- {entry['dpi']} DPI ({entry['factor']:.2f}x)"
            )
            
        self.canvas.itemconfig(self.debug_text, 
                             text="\n".join(debug_content),
                             font=('Consolas', math.floor(10 * dims['current_factor'])))
        self.canvas.coords(self.debug_text,
                         math.floor(10 * dims['current_factor']),
                         math.floor(10 * dims['current_factor']))
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AdaptiveGUI()
    app.run()