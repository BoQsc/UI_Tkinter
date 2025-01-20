
       

import tkinter

# Initialize the window
window = tkinter.Tk()

# Set up the canvas
canvas = tkinter.Canvas(window, bg="black")
canvas.pack(fill=tkinter.BOTH, expand=True)

# Create a rectangle on the canvas
canvas.create_rectangle(10, 20, 30, 40, fill="red")

# Store initial size and position
window.size = (window.winfo_width(), window.winfo_height())
window.pos = (window.winfo_x(), window.winfo_y())

def on_configure(event):
    if event.widget == window:  # IMPORTANT Check if the event originated from the window

        # Separate resize and move events
        resized = (event.width, event.height) != window.size
        moved = (event.x, event.y) != window.pos

        if resized:
            print(f"Resized to {event.width}x{event.height}")
            window.size = (event.width, event.height)

        if moved:
            print(f"Moved to ({event.x}, {event.y})")
            window.pos = (event.x, event.y)

# Bind the configure event
window.bind("<Configure>", on_configure)

# Run the main loop
window.mainloop()

