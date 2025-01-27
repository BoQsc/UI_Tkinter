import tkinter as tk
import ctypes

def get_system_dpi():
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        hwnd = ctypes.windll.user32.GetDesktopWindow()
        return ctypes.windll.user32.GetDpiForWindow(hwnd)
    except:
        return 96

def toggle_fullscreen(event=None):
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    root.attributes('-fullscreen', is_fullscreen)
    if not is_fullscreen:
        root.geometry(f"{int(800*scaling_factor)}x{int(600*scaling_factor)}")
    update_layout()

def update_layout(event=None):
    # Get current canvas dimensions
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    
    # Dark blue rectangle (full width at bottom)
    dark_height = 80 * scaling_factor
    canvas.coords(dark_rect, 
                0, canvas_height - dark_height,
                canvas_width, canvas_height)
    
    # Light blue rectangle (70% width, same bottom)
    light_width = canvas_width * 0.7
    light_height = 50 * scaling_factor
    canvas.coords(light_rect,
                0,  # Start from left edge
                canvas_height - dark_height,  # Align with dark rectangle top
                light_width,
                canvas_height - (dark_height - light_height))  # Maintain height
    
    # Update info text
    canvas.itemconfig(info_text, text=f"DPI: {system_dpi} (Scale: {scaling_factor:.1f}x)\n"
                                    f"Window: {canvas_width}x{canvas_height}")
    canvas.coords(info_text, 10 * scaling_factor, canvas_height - dark_height + 10 * scaling_factor)

def main():
    global root, canvas, dark_rect, light_rect, info_text, scaling_factor, system_dpi, is_fullscreen

    root = tk.Tk()
    root.title("DPI Scaling Proof - Bottom Bars")
    is_fullscreen = False
    
    # DPI detection and scaling
    system_dpi = get_system_dpi()
    scaling_factor = system_dpi / 96.0
    root.tk.call('tk', 'scaling', scaling_factor * 72.0 / 96.0)

    # Create responsive canvas
    canvas = tk.Canvas(root, bg='white', width=800*scaling_factor, height=600*scaling_factor)
    canvas.pack(fill=tk.BOTH, expand=True)
    
    # Create rectangles (initial positions)
    dark_rect = canvas.create_rectangle(0, 0, 0, 0, fill='#1A5276', outline='')  # Dark blue
    light_rect = canvas.create_rectangle(0, 0, 0, 0, fill='#85C1E9', outline='')  # Light blue
    
    # Info text
    info_text = canvas.create_text(10, 10, anchor=tk.NW, fill='white',
                                 font=('Arial', int(12*scaling_factor)), text="")
    
    # Bindings
    canvas.bind("<Configure>", update_layout)
    root.bind("<F11>", toggle_fullscreen)
    root.bind("<Escape>", lambda e: root.attributes('-fullscreen', False))
    
    # Initial update
    update_layout()
    root.mainloop()

if __name__ == "__main__":
    main()