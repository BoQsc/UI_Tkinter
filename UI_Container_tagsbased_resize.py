import tkinter
window = tkinter.Tk()

canvas = tkinter.Canvas(window, bg="brown")
canvas.pack()

canvas.create_rectangle(50, 50, 300, 100, fill="lightgray", tags="container")
canvas.create_rectangle(70, 70, 90, 90,   fill="blue",      tags="container_item")
canvas.create_text(125, 100, text="Item2", font=("Arial", 14), tags="container_item")


def move_container(container, dx, dy):
    canvas.move(canvas.find_withtag(container), dx, dy)
    for item in canvas.find_withtag(container + "_item"):
        canvas.move(item, dx, dy)

# It is getting complicated if introducing collision detection.
def resize_container(container, y=None, x=None):
    container_id = canvas.find_withtag(container)
    x0, y0, x1, y1 = canvas.coords(container_id)
    canvas.coords(container_id, x0, y0 + 10, x1, y1)

    for item in canvas.find_withtag(container + "_item"):
        item_type = canvas.type(item)
        if item_type == "rectangle":
            ix0, iy0, ix1, iy1 = canvas.coords(item)
            canvas.coords(item, ix0, iy0 + 5, ix1 - 5, iy1)
        elif item_type == "text":
            tx, ty = canvas.coords(item)
            canvas.coords(item, tx - 5, ty + 5)  # Move diagonally
    pass
tkinter.Button(window, text="Move", command=lambda: move_container("container", 10, 10)).pack()
tkinter.Button(window, text="Resize", command=lambda: resize_container("container", 10, 10)).pack()

window.mainloop()