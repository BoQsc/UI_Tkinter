import tkinter as tk

# Create the main window
root = tk.Tk()

# Create a canvas widget
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Outer rectangle dimensions
outer_x1, outer_y1, outer_x2, outer_y2 = 50, 50, 350, 350

# Create the outer rectangle
canvas.create_rectangle(outer_x1, outer_y1, outer_x2, outer_y2, outline="black", fill="blue")

# Inner rectangle size
inner_width = 50
inner_height = 50

# Loop to create inner rectangles inside the outer rectangle
x = outer_x1
while x + inner_width <= outer_x2:
    y = outer_y1
    while y + inner_height <= outer_y2:
        canvas.create_rectangle(x, y, x + inner_width, y + inner_height, outline="red", fill="yellow")
        y += inner_height
    x += inner_width

# Run the Tkinter event loop
root.mainloop()
