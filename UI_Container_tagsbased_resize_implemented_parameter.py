import tkinter
window = tkinter.Tk()

canvas = tkinter.Canvas(window, bg="brown")
canvas.pack()

canvas.create_rectangle(50, 50, 300, 100, fill="lightgray", tags="container")
canvas.create_rectangle(70, 70, 90, 90,   fill="blue",      tags="container_item")
canvas.create_text(100, 70, text="Item2", font=("Arial", 10), tags="container_item")


def move_container(container, dx, dy):
    canvas.move(canvas.find_withtag(container), dx, dy)
    for item in canvas.find_withtag(container + "_item"):
        canvas.move(item, dx, dy)

# It is getting complicated if introducing collision detection.
def resize_container(container, y=None):
    # Default to hardcoded values if `y` is not provided
    y_container = y or 10
    y_item = y or 5

    # Linear interpolation for font size
    # When y=10, font_adjustment=2
    # When y=20, font_adjustment=4
    if y is not None:
        # Calculate font adjustment using linear interpolation
        font_adjustment = 2 + (y - 10) * 0.2
        # Only use the font adjustment if it's a whole number
        if not font_adjustment.is_integer():
            font_adjustment = 2  # Default to base adjustment if not integer
        else:
            font_adjustment = int(font_adjustment)
    else:
        font_adjustment = 2  # Default font adjustment

    container_id = canvas.find_withtag(container)
    x0, y0, x1, y1 = canvas.coords(container_id)
    canvas.coords(container_id, x0, y0 + y_container, x1, y1)

    for item in canvas.find_withtag(container + "_item"):
        item_type = canvas.type(item)
        if item_type == "rectangle":
            ix0, iy0, ix1, iy1 = canvas.coords(item)
            canvas.coords(item, ix0, iy0 + y_item, ix1 - y_item, iy1)
            print(ix0, iy0, ix1, iy1)
        elif item_type == "text":
            font_family, font_size = canvas.itemcget(item, "font").split()
            new_font_size = max(int(font_size) - font_adjustment, 1)  # Ensure font size stays >= 1
            canvas.itemconfig(item, font=(font_family, int(new_font_size)))  # Ensure integer font size
            tx, ty = canvas.coords(item)
            canvas.coords(item, tx - y_item, ty + y_item)  # Move diagonally
            print(new_font_size)
            
tkinter.Button(window, text="Move", command=lambda: move_container("container", 10, 10)).pack()
tkinter.Button(window, text="Resize", command=lambda: resize_container("container", 10)).pack()
tkinter.Button(window, text="Resize", command=lambda: resize_container("container", -10)).pack()
window.mainloop()