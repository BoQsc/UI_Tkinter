import tkinter as tk

# Create the main application window
root = tk.Tk()
root.title("Rectangle Drawing App with Drag Update")

# Create a Canvas widget to draw on
canvas = tk.Canvas(root, width=400, height=400, bg="white")
canvas.pack()

# Variables to store the initial click coordinates
start_x, start_y = None, None
current_rectangle = None

# Function to start drawing when mouse button is pressed
def on_press(event):
    global start_x, start_y
    start_x = event.x
    start_y = event.y
    # Clear any existing rectangle
    if current_rectangle:
        canvas.delete(current_rectangle)
    # Store current coordinates to update dynamically
    update_rectangle(event)

# Function to draw the rectangle while dragging
def on_drag(event):
    global start_x, start_y, current_rectangle
    if start_x and start_y:
        # Update the rectangle coordinates dynamically
        if current_rectangle:
            canvas.delete(current_rectangle)
        current_rectangle = update_rectangle(event)

# Function to finalize drawing when mouse is released
def on_release(event):
    global start_x, start_y, current_rectangle
    if start_x and start_y:
        if current_rectangle:
            canvas.delete(current_rectangle)
        end_x = event.x
        end_y = event.y
        canvas.create_rectangle(start_x, start_y, end_x, end_y, fill="red")

# Function to update rectangle while dragging
def update_rectangle(event):
    # Draw the rectangle with updated coordinates
    return canvas.create_rectangle(start_x, start_y, event.x, event.y, outline="blue", dash=(2,2))

# Bind mouse events to the canvas
canvas.bind("<Button-1>", on_press)  # Left mouse button down to start drawing
canvas.bind("<B1-Motion>", on_drag)    # Dragging the mouse to update the rectangle
canvas.bind("<ButtonRelease-1>", on_release)  # Left mouse button up to draw the rectangle

# Run the main loop
root.mainloop()
