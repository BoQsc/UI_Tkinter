import tkinter as tk
import sys
import math

def get_scaling_factor():
    root = tk.Tk()
    root.withdraw()
    
    if sys.platform == 'win32':
        import ctypes
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
            hdc = ctypes.windll.user32.GetDC(0)
            dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)
            ctypes.windll.user32.ReleaseDC(0, hdc)
            return round(dpi / 96, 2)
        except:
            return round(root.winfo_fpixels('1i') / 96, 2)
    elif sys.platform == 'darwin':
        return round(root.tk.call('tk', 'scaling') / 72 * 96 / 96, 2)
    else:
        return round(root.winfo_fpixels('1i') / 96, 2)

def toggle_fullscreen(event=None):
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    root.attributes('-fullscreen', is_fullscreen)
    root.after(10, update_layout)

def update_layout(event=None):
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    
    # Calculate breakpoint (600px at 96dpi equivalent)
    breakpoint_width = 600 * scaling_factor
    
    # Determine width percentage based on screen size
    if canvas_width <= breakpoint_width:
        width_percent = 0.5  # 50% for small screens
        color = '#FF6B6B'    # Different color for visual feedback
    else:
        width_percent = 0.7  # 70% for larger screens
        color = '#85C1E9'
    
    # Dark blue rectangle
    dark_height = math.floor(80 * scaling_factor)
    canvas.coords(dark_rect, 
                0, canvas_height - dark_height,
                math.ceil(canvas_width),
                math.ceil(canvas_height))
    
    # Light blue rectangle with dynamic width
    light_width = math.floor(canvas_width * width_percent)
    light_height = math.floor(50 * scaling_factor)
    canvas.coords(light_rect,
                0,
                canvas_height - dark_height,
                light_width,
                canvas_height - dark_height + light_height)
    canvas.itemconfig(light_rect, fill=color)
    
    # Update info text
    canvas.itemconfig(info_text, 
        text=f"System: {sys.platform}\n"
             f"Scale: {scaling_factor}x\n"
             f"Mode: {'Small Screen' if canvas_width <= breakpoint_width else 'Large Screen'}\n"
             f"Width: {width_percent*100:.0f}%",
        font=('Arial', math.floor(12 * scaling_factor))
    )
    canvas.coords(info_text, 
        math.floor(10 * scaling_factor), 
        canvas_height - dark_height + math.floor(10 * scaling_factor)
    )

def main():
    global root, canvas, dark_rect, light_rect, info_text, scaling_factor
    
    root = tk.Tk()
    root.title("Adaptive DPI Scaling")
    
    # High DPI initialization
    scaling_factor = get_scaling_factor()
    if sys.platform == 'win32':
        root.tk.call('tk', 'scaling', 1.0)
    
    # Set up canvas
    canvas = tk.Canvas(root, bg='white', 
        width=math.floor(800 * scaling_factor),
        height=math.floor(600 * scaling_factor),
        highlightthickness=0
    )
    canvas.pack(fill=tk.BOTH, expand=True)
    
    # Create elements
    dark_rect = canvas.create_rectangle(0, 0, 0, 0, fill='#1A5276', outline='')
    light_rect = canvas.create_rectangle(0, 0, 0, 0, fill='#85C1E9', outline='')
    info_text = canvas.create_text(0, 0, anchor=tk.NW, fill='white', text="")
    
    # Bindings
    root.bind("<F11>", toggle_fullscreen)
    root.bind("<Configure>", lambda e: root.after(10, update_layout))
    root.bind("<Escape>", lambda e: root.attributes('-fullscreen', False))
    
    update_layout()
    root.mainloop()

if __name__ == "__main__":
    main()