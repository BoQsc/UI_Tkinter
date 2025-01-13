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
    container_y = y
    item_cy = y / 2 
    text_cy = int(y / 5)
    text_cy_pos = int(y / 2) 

    container_id = canvas.find_withtag(container)
    x0, y0, x1, y1 = canvas.coords(container_id)
    canvas.coords(container_id, x0, y0 + container_y, x1, y1)

    for item in canvas.find_withtag(container + "_item"):
        item_type = canvas.type(item)
        if item_type == "rectangle":
            ix0, iy0, ix1, iy1 = canvas.coords(item)
            canvas.coords(item, ix0, iy0 + item_cy, ix1 - item_cy, iy1)
            print(ix0, iy0, ix1, iy1)
        elif item_type == "text":
            font_family, font_size = canvas.itemcget(item, "font").split()
            canvas.itemconfig(item, font=(font_family, int(font_size) - text_cy))
            tx, ty = canvas.coords(item)
            canvas.coords(item, tx - text_cy_pos, ty + text_cy_pos)  # Move diagonally
            print(font_size)
    pass
tkinter.Button(window, text="Move", command=lambda: move_container("container", 10, 10)).pack()
tkinter.Button(window, text="Resize", command=lambda: resize_container("container", 10)).pack()
tkinter.Button(window, text="Resize", command=lambda: resize_container("container", -10)).pack()
window.mainloop()