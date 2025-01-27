import tkinter as tk
import sys
import math
from tkinter import font

class DPIMonitor:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.setup_metrics()
        self.update_metrics()
        
    def setup_ui(self):
        self.canvas = tk.Canvas(self.root, bg='white', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Debug overlay
        self.debug_text = self.canvas.create_text(
            10, 10, anchor=tk.NW, fill='#333',
            font=font.Font(family='Consolas', size=9),
            text="Initializing metrics...\n"
        )
        
        # Rectangles
        self.dark_rect = self.canvas.create_rectangle(0,0,0,0, fill='#1A5276', outline='')
        self.light_rect = self.canvas.create_rectangle(0,0,0,0, fill='#85C1E9', outline='')
        
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Configure>", self.on_resize)
        
    def setup_metrics(self):
        self.scaling_factor = self.get_scaling_factor()
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.physical_dpi = self.calculate_physical_dpi()
        self.last_metrics = {}
        
    def calculate_physical_dpi(self):
        # Estimate physical DPI based on common screen sizes
        diagonal_pixels = math.hypot(self.screen_width, self.screen_height)
        common_sizes = {
            # Diagonal inches: (width, height) mm
            13: (294, 165),
            15: (331, 207),
            24: (527, 296),
            27: (596, 336)
        }
        closest_size = min(common_sizes.items(), 
                          key=lambda x: abs(x[1][0] - diagonal_pixels/self.scaling_factor*25.4/96))
        diag_inches, (width_mm, height_mm) = closest_size
        return int(diagonal_pixels / diag_inches)
        
    def get_scaling_factor(self):
        root = tk.Tk()
        root.withdraw()
        if sys.platform == 'win32':
            return root.winfo_fpixels('1i') / 96
        elif sys.platform == 'darwin':
            return root.tk.call('tk', 'scaling') / 1.333
        else:
            return root.winfo_fpixels('1i') / 96
        
    def update_metrics(self):
        new_metrics = {
            'screen_width': self.root.winfo_screenwidth(),
            'screen_height': self.root.winfo_screenheight(),
            'window_width': self.root.winfo_width(),
            'window_height': self.root.winfo_height(),
            'scaling_factor': self.scaling_factor,
            'physical_dpi': self.physical_dpi,
            'light_width_pct': 70  # Default
        }
        
        # Dynamic width adjustment rules
        if self.physical_dpi > 150 or self.screen_width < 1920:
            new_metrics['light_width_pct'] = 50
            
        if new_metrics != self.last_metrics:
            self.last_metrics = new_metrics
            self.update_debug_overlay()
            
    def update_debug_overlay(self):
        text = (
            f"System: {sys.platform}\n"
            f"Screen: {self.screen_width}x{self.screen_height}\n"
            f"DPI (calc): {self.physical_dpi}\n"
            f"Scaling Factor: {self.scaling_factor:.2f}x\n"
            f"Light Width: {self.last_metrics['light_width_pct']}%\n"
            f"Window: {self.root.winfo_width()}x{self.root.winfo_height()}"
        )
        self.canvas.itemconfig(self.debug_text, text=text)
        
    def on_resize(self, event):
        self.crisp_redraw()
        self.update_metrics()
        
    def crisp_redraw(self):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Dark rectangle (bottom 80px physical height)
        dark_height = math.floor(80 * self.scaling_factor)
        self.canvas.coords(self.dark_rect,
            0, canvas_height - dark_height,
            math.ceil(canvas_width),
            math.ceil(canvas_height)
        )
        
        # Light rectangle (dynamic percentage)
        light_width_pct = self.last_metrics.get('light_width_pct', 70)
        light_width = math.floor(canvas_width * light_width_pct / 100)
        light_height = math.floor(50 * self.scaling_factor)
        self.canvas.coords(self.light_rect,
            0, canvas_height - dark_height,
            light_width,
            canvas_height - dark_height + light_height
        )
        
    def toggle_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))
        self.root.after(100, self.crisp_redraw)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Adaptive DPI/Screen Size Demo")
    root.geometry("800x600")
    app = DPIMonitor(root)
    root.mainloop()