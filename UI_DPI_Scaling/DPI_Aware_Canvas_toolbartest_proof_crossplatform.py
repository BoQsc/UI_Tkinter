import tkinter as tk
import sys
import math

def get_scaling_factor():
    """Cross-platform scaling with integer rounding"""
    root = tk.Tk()
    root.withdraw()
    
    # Windows: Get actual monitor scaling
    if sys.platform == 'win32':
        import ctypes
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
            hdc = ctypes.windll.user32.GetDC(0)
            dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)  # LOGPIXELSX
            ctypes.windll.user32.ReleaseDC(0, hdc)
            return round(dpi / 96, 2)
        except:
            return round(root.winfo_fpixels('1i') / 96, 2)
    
    # macOS: Handle Retina displays
    elif sys.platform == 'darwin':
        return round(root.tk.call('tk', 'scaling') / 72 * 96 / 96, 2)
    
    # Linux: X11 scaling
    else:
        return round(root.winfo_fpixels('1i') / 96, 2)

def toggle_fullscreen(event=None):
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    root.attributes('-fullscreen', is_fullscreen)
    if not is_fullscreen:
        root.geometry(f"{base_width}x{base_height}")
    root.after(10, crisp_redraw)  # Force redraw after resize

def crisp_redraw():
    """Ensure integer pixel coordinates for all elements"""
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    
    # Dark blue rectangle (bottom-aligned, integer height)
    dark_height = math.floor(80 * scaling_factor)
    canvas.coords(dark_rect, 
                0, canvas_height - dark_height,
                math.ceil(canvas_width),
                math.ceil(canvas_height))
    
    # Light blue rectangle (70% width with integer dimensions)
    light_width = math.floor(canvas_width * 0.7)
    light_height = math.floor(50 * scaling_factor)
    canvas.coords(light_rect,
                0,
                canvas_height - dark_height,
                light_width,
                canvas_height - dark_height + light_height)
    
    # Crisp text rendering
    canvas.itemconfig(info_text, 
        text=f"System: {sys.platform}\nScale: {scaling_factor}x\n"
             f"Canvas: {canvas_width}x{canvas_height}",
        font=('Arial', math.floor(12 * scaling_factor))
    )
    canvas.coords(info_text, 
        math.floor(10 * scaling_factor), 
        canvas_height - dark_height + math.floor(10 * scaling_factor)
    )

def main():
    global root, canvas, dark_rect, light_rect, info_text, scaling_factor
    global base_width, base_height, is_fullscreen
    
    root = tk.Tk()
    root.title("Crisp Cross-Platform DPI")
    is_fullscreen = False
    
    # High DPI initialization
    if sys.platform == 'win32':
        root.tk.call('tk', 'scaling', 1.0)  # Disable Tk's automatic scaling
    elif sys.platform == 'darwin':
        root.tk.call('tk', 'scaling', 2.0 if 'Retina' in root.tk.call('tk', 'windowingsystem') else 1.0)
    
    # Get physical scaling factor
    scaling_factor = get_scaling_factor()
    
    # Base dimensions at 1x scale
    base_width = 800
    base_height = 600
    
    # Set up canvas with integer scaling
    canvas = tk.Canvas(root, bg='white', 
        width=math.floor(base_width * scaling_factor),
        height=math.floor(base_height * scaling_factor),
        highlightthickness=0  # Remove anti-aliased border
    )
    canvas.pack(fill=tk.BOTH, expand=True)
    
    # Create elements with initial crisp coordinates
    dark_rect = canvas.create_rectangle(0, 0, 0, 0, fill='#1A5276', outline='')
    light_rect = canvas.create_rectangle(0, 0, 0, 0, fill='#85C1E9', outline='')
    info_text = canvas.create_text(0, 0, anchor=tk.NW, fill='white', text="")
    
    # Bindings
    root.bind("<F11>", toggle_fullscreen)
    root.bind("<Configure>", lambda e: root.after(10, crisp_redraw))
    root.bind("<Escape>", lambda e: root.attributes('-fullscreen', False))
    
    crisp_redraw()
    root.mainloop()

if __name__ == "__main__":
    main()