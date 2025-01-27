import tkinter as tk
import ctypes

def get_system_dpi():
    """Retrieves the system DPI setting with fallback to 96 if unavailable."""
    try:
        # Enable DPI awareness (Windows)
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        hwnd = ctypes.windll.user32.GetDesktopWindow()
        dpi = ctypes.windll.user32.GetDpiForWindow(hwnd)
        return dpi
    except:
        return 96  # Fallback for non-Windows or errors

def main():
    root = tk.Tk()
    root.title("DPI-Aware Tkinter Canvas")
    
    # Get system DPI and calculate scaling
    system_dpi = get_system_dpi()
    scaling_factor = system_dpi / 96.0  # Scale relative to 96 DPI
    
    # Set Tkinter's scaling for fonts/widgets using points/inches
    root.tk.call('tk', 'scaling', scaling_factor * 72.0 / 96.0)
    
    # Create scaled canvas (base size 800x600 at 96 DPI)
    canvas_width = int(800 * scaling_factor)
    canvas_height = int(600 * scaling_factor)
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='white')
    canvas.pack(padx=10, pady=10)
    
    # Draw scaled elements (base coordinates at 96 DPI)
    rect = canvas.create_rectangle(
        50 * scaling_factor,
        50 * scaling_factor,
        250 * scaling_factor,
        150 * scaling_factor,
        fill='blue',
        outline=''
    )
    
    circle = canvas.create_oval(
        300 * scaling_factor,
        100 * scaling_factor,
        500 * scaling_factor,
        300 * scaling_factor,
        fill='red',
        outline=''
    )
    
    text = canvas.create_text(
        400 * scaling_factor,
        400 * scaling_factor,
        text=f"System DPI: {system_dpi} (Scale: {scaling_factor:.2f}x)",
        font=('Arial', int(12 * scaling_factor))
    )
    
    root.mainloop()

if __name__ == "__main__":
    main()