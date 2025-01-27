import tkinter as tk
import ctypes

def get_system_dpi():
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        hwnd = ctypes.windll.user32.GetDesktopWindow()
        return ctypes.windll.user32.GetDpiForWindow(hwnd)
    except:
        return 96

def update_rectangles(event):
    # Dynamic scaling when window resizes
    canvas.coords(blue_toolbar, 0, canvas.winfo_height() - toolbar_height, 
                canvas.winfo_width(), canvas.winfo_height())
    
    # Keep red rectangle centered in toolbar
    toolbar_top = canvas.winfo_height() - toolbar_height
    red_width = 100 * scaling_factor
    red_height = 30 * scaling_factor
    canvas.coords(red_rectangle,
                (canvas.winfo_width() - red_width)/2,
                toolbar_top + (toolbar_height - red_height)/2,
                (canvas.winfo_width() + red_width)/2,
                toolbar_top + (toolbar_height + red_height)/2)

def main():
    global canvas, blue_toolbar, red_rectangle, scaling_factor, toolbar_height

    root = tk.Tk()
    root.title("DPI Scaling Proof")
    
    system_dpi = get_system_dpi()
    scaling_factor = system_dpi / 96.0
    root.tk.call('tk', 'scaling', scaling_factor * 72.0 / 96.0)

    # Base toolbar dimensions at 96 DPI
    toolbar_height = 50 * scaling_factor
    
    # Create resizable canvas
    canvas = tk.Canvas(root, bg='white', width=800 * scaling_factor, 
                     height=600 * scaling_factor)
    canvas.pack(fill=tk.BOTH, expand=True)
    
    # Blue toolbar (initially full width)
    blue_toolbar = canvas.create_rectangle(0, 600 - toolbar_height, 
                                         800 * scaling_factor, 600 * scaling_factor,
                                         fill='blue', outline='')
    
    # Red centered rectangle (initially centered)
    red_rectangle = canvas.create_rectangle(0, 0, 0, 0, fill='red')
    
    # Bind resize handler
    canvas.bind("<Configure>", update_rectangles)
    
    # Info text
    canvas.create_text(10 * scaling_factor, 10 * scaling_factor,
                     anchor=tk.NW, text=f"DPI: {system_dpi} (Scale: {scaling_factor:.1f}x)",
                     font=('Arial', int(12 * scaling_factor)), fill='black')
    
    root.mainloop()

if __name__ == "__main__":
    main()