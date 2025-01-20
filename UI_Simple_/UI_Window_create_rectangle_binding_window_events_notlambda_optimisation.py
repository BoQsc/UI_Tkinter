import tkinter
window = tkinter.Tk()

canvas = tkinter.Canvas(bg="black")
canvas.pack()

canvas.create_rectangle(10, 20, 30, 40, fill="red")

def on_window_event(event):
    if event.widget == window:  # Ensure we're handling the main window
        if not hasattr(window, "_previous_geometry"):
            # Store initial geometry (position and size) and initialize flags
            window._previous_geometry = (event.width, event.height, event.x, event.y)
            window._resize_skipped = False
            window._move_skipped = False
            return  # Skip first event entirely

        prev_width, prev_height, prev_x, prev_y = window._previous_geometry

        # Check for resize
        if (event.width, event.height) != (prev_width, prev_height):
            if not window._resize_skipped:
                window._resize_skipped = True  # Skip first resize event
            else:
                print(f"Resized: width={event.width}, height={event.height}")

        # Check for position change
        if (event.x, event.y) != (prev_x, prev_y):
            if not window._move_skipped:
                window._move_skipped = True  # Skip first move event
            else:
                print(f"Moved: x={event.x}, y={event.y}")

        # Update stored geometry
        window._previous_geometry = (event.width, event.height, event.x, event.y)

window.bind("<Configure>", on_window_event)
window.mainloop()
