import tkinter as tk

root = tk.Tk()
root.title("Always Visible Window")

# Keep the window always on top
root.attributes('-topmost', True)

# Override window manager behavior
root.wm_attributes('-toolwindow', True)  # Makes it a tool window (optional)
root.wm_attributes('-disabled', False)   # Ensures it remains interactive

root.mainloop()
