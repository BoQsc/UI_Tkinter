import tkinter

window = tkinter.Tk()
canvas = tkinter.Canvas(window, bg="blue")
canvas.pack()

# Update the window to ensure accurate dimensions and position are retrieved
window.update()

# Screen and window metrics
print("screen_width:", window.winfo_screenwidth())
print("screen_height:", window.winfo_screenheight())
print("screen_depth (bits per pixel):", window.winfo_screendepth())

# Window-specific details
print("window_width:", window.winfo_width())
print("window_height:", window.winfo_height())
print("window_x (position from left):", window.winfo_x())
print("window_y (position from top):", window.winfo_y())
print("window_geometry:", window.geometry())  # Format: WxH+X+Y

# DPI and scaling information
print("dpi (via winfo_fpixels):", window.winfo_fpixels('1i'))  # Pixels per inch as float
print("dpi (via winfo_pixels):", window.winfo_pixels('1i'))    # Pixels per inch as int
print("tk_scaling_factor:", window.tk.call('tk', 'scaling'))   # Tk's internal scaling factor

window.mainloop()