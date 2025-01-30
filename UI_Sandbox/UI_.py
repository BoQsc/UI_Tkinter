import tkinter as tk

root = tk.Tk()
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

outer_rect = canvas.create_rectangle(50, 50, 350, 350)
inner_rect = canvas.create_rectangle(100, 100, 300, 300)

# Function to adjust the inner rectangle position
def move_inner_rect(x, y):
    # Get the coordinates of the outer rectangle
    x1, y1, x2, y2 = canvas.coords(outer_rect)
    
    # Calculate the maximum allowable x and y positions for the inner rectangle
    max_x = x2 - 200  # 200 is the width of the inner rectangle
    max_y = y2 - 200  # 200 is the height of the inner rectangle

    # Ensure the inner rectangle stays within the outer rectangle's bounds
    x = max(min(x, max_x), x1)  # x must be within the outer rectangle's x bounds
    y = max(min(y, max_y), y1)  # y must be within the outer rectangle's y bounds

    # Update the position of the inner rectangle
    canvas.coords(inner_rect, x, y, x + 200, y + 200)

move_inner_rect(50, 150)  # Example of adjusting position

root.mainloop()
