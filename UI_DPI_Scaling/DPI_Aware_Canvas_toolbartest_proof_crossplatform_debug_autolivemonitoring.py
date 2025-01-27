import tkinter as tk
import sys
import math
from tkinter import font

class DynamicDPIApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.setup_bindings()
        self.last_metrics = {}
        self.update_ui(force=True)  # Initial setup
        
    def setup_ui(self):
        # Main canvas
        self.canvas = tk.Canvas(self.root, bg='white', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Debug overlay
        self.debug_font = font.Font(family='Consolas', size=9)
        self.debug_text = self.canvas.create_text(
            10, 10, anchor=tk.NW, fill='#333', 
            font=self.debug_font, text="Initializing..."
        )
        
        # Graphical elements
        self.dark_rect = self.canvas.create_rectangle(0,0,0,0, fill='#1A5276')
        self.light_rect = self.canvas.create_rectangle(0,0,0,0, fill='#85C1E9')
        
    def setup_bindings(self):
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Configure>", self.on_window_change)
        self.root.bind("<Motion>", self.update_debug)  # Continuous updates
        
    def get_current_metrics(self):
        """Get all relevant metrics in real-time"""
        return {
            'dpi_scaling': self.get_scaling_factor(),
            'screen_width': self.root.winfo_screenwidth(),
            'screen_height': self.root.winfo_screenheight(),
            'window_width': self.root.winfo_width(),
            'window_height': self.root.winfo_height(),
            'physical_dpi': self.estimate_physical_dpi(),
            'light_width_pct': self.calculate_width_percentage()
        }
    
    def get_scaling_factor(self):
        """Real-time scaling factor detection"""
        return self.canvas.winfo_fpixels('1i') / 96
    
    def estimate_physical_dpi(self):
        """Approximate physical screen DPI"""
        return int(math.hypot(
            self.root.winfo_screenwidth(), 
            self.root.winfo_screenheight()
        ) / (self.root.winfo_screenmmwidth()/25.4))
    
    def calculate_width_percentage(self):
        """Dynamic width adjustment logic"""
        window_width = self.root.winfo_width()
        scaling = self.get_scaling_factor()
        
        # Switch to 50% if either condition met
        if (window_width < 800 * scaling) or (self.estimate_physical_dpi() > 150):
            return 50
        return 70
    
    def on_window_change(self, event):
        """Handle all window/config changes"""
        current = self.get_current_metrics()
        
        # Only update if metrics actually changed
        if current != self.last_metrics:
            self.last_metrics = current
            self.update_ui()
            
    def update_ui(self, force=False):
        """Pixel-perfect UI updates"""
        m = self.last_metrics
        
        # Dark background (bottom-aligned)
        dark_height = math.floor(80 * m['dpi_scaling'])
        self.canvas.coords(self.dark_rect,
            0, m['window_height'] - dark_height,
            m['window_width'], m['window_height']
        )
        
        # Light foreground (dynamic width)
        light_width = math.floor(m['window_width'] * m['light_width_pct'] / 100)
        light_height = math.floor(50 * m['dpi_scaling'])
        self.canvas.coords(self.light_rect,
            0, m['window_height'] - dark_height,
            light_width, m['window_height'] - dark_height + light_height
        )
        
        # Update debug text font
        self.debug_font.configure(size=int(9 * m['dpi_scaling']))
    
    def update_debug(self, event=None):
        """Live debug information"""
        if not self.last_metrics:
            return
            
        m = self.last_metrics
        text = (
            f"DPI Scaling: {m['dpi_scaling']:.2f}x\n"
            f"Physical DPI: ~{m['physical_dpi']}\n"
            f"Window: {m['window_width']}x{m['window_height']}\n"
            f"Light Width: {m['light_width_pct']}%\n"
            f"Screen: {m['screen_width']}x{m['screen_height']}\n"
            f"Platform: {sys.platform}"
        )
        self.canvas.itemconfig(self.debug_text, text=text)
        self.canvas.tag_raise(self.debug_text)  # Keep on top
        
    def toggle_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', 
            not self.root.attributes('-fullscreen'))
        self.root.after(100, self.on_window_change, None)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Real-Time DPI/Size Monitor")
    root.geometry("1000x800")
    
    # DPI awareness initialization
    if sys.platform == 'win32':
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    
    app = DynamicDPIApp(root)
    root.mainloop()