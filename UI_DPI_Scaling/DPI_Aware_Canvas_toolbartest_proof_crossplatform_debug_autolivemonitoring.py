import tkinter as tk
import sys
import math
from tkinter import font

class DynamicDPIApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.setup_bindings()
        self.last_metrics = self.get_current_metrics()  # Initialize metrics first
        self.update_ui(force=True)

    def setup_ui(self):
        self.canvas = tk.Canvas(self.root, bg='white', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.debug_font = font.Font(family='Consolas', size=9)
        self.debug_text = self.canvas.create_text(
            10, 10, anchor=tk.NW, fill='#333', 
            font=self.debug_font, text="Initializing metrics..."
        )
        
        self.dark_rect = self.canvas.create_rectangle(0,0,0,0, fill='#1A5276')
        self.light_rect = self.canvas.create_rectangle(0,0,0,0, fill='#85C1E9')

    def setup_bindings(self):
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Configure>", self.on_window_change)
        self.root.bind("<Motion>", self.update_debug)

    def get_current_metrics(self):
        """Safe metric collection with fallbacks"""
        try:
            return {
                'dpi_scaling': self.get_scaling_factor(),
                'screen_width': self.root.winfo_screenwidth(),
                'screen_height': self.root.winfo_screenheight(),
                'window_width': self.root.winfo_width(),
                'window_height': self.root.winfo_height(),
                'physical_dpi': self.estimate_physical_dpi(),
                'light_width_pct': self.calculate_width_percentage()
            }
        except Exception as e:
            return {
                'dpi_scaling': 1.0,
                'screen_width': 1920,
                'screen_height': 1080,
                'window_width': 800,
                'window_height': 600,
                'physical_dpi': 96,
                'light_width_pct': 70
            }

    def get_scaling_factor(self):
        """Safe scaling factor detection"""
        try:
            return self.canvas.winfo_fpixels('1i') / 96
        except:
            return 1.0

    def estimate_physical_dpi(self):
        """Safer DPI estimation"""
        try:
            mm_width = self.root.winfo_screenmmwidth()
            if mm_width <= 0:  # Handle invalid millimeter measurements
                return 96
            return int(self.root.winfo_screenwidth() / (mm_width / 25.4))
        except:
            return 96

    def calculate_width_percentage(self):
        """Width calculation with fallback"""
        try:
            window_width = self.root.winfo_width()
            scaling = self.get_scaling_factor()
            physical_dpi = self.estimate_physical_dpi()
            
            if (window_width < 800 * scaling) or (physical_dpi > 150):
                return 50
            return 70
        except:
            return 70

    def on_window_change(self, event):
        try:
            current = self.get_current_metrics()
            if current != self.last_metrics:
                self.last_metrics = current
                self.update_ui()
        except Exception as e:
            print(f"Update error: {str(e)}")

    def update_ui(self, force=False):
        """Safe UI update"""
        try:
            m = self.last_metrics
            dark_height = math.floor(80 * m['dpi_scaling'])
            self.canvas.coords(self.dark_rect,
                0, m['window_height'] - dark_height,
                m['window_width'], m['window_height']
            )
            
            light_width = math.floor(m['window_width'] * m['light_width_pct'] / 100)
            light_height = math.floor(50 * m['dpi_scaling'])
            self.canvas.coords(self.light_rect,
                0, m['window_height'] - dark_height,
                light_width, m['window_height'] - dark_height + light_height
            )
            
            self.debug_font.configure(size=max(6, int(9 * m['dpi_scaling'])))
        except KeyError as e:
            print(f"Missing metric: {str(e)}")
        except Exception as e:
            print(f"UI update failed: {str(e)}")

    def update_debug(self, event=None):
        try:
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
            self.canvas.tag_raise(self.debug_text)
        except Exception as e:
            print(f"Debug update error: {str(e)}")

    def toggle_fullscreen(self, event=None):
        try:
            self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))
            self.root.after(100, self.on_window_change, None)
        except Exception as e:
            print(f"Fullscreen error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Fixed DPI Monitor")
    root.geometry("1000x800")
    
    # Windows DPI awareness
    if sys.platform == 'win32':
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass
    
    app = DynamicDPIApp(root)
    root.mainloop()