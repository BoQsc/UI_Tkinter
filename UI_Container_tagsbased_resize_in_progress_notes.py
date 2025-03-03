import tkinter
window = tkinter.Tk()

canvas = tkinter.Canvas(window, bg="black")
canvas.pack()

canvas.create_rectangle(50, 50, 300, 100, fill="lightgray", tags="container")
canvas.create_rectangle(70, 70, 90, 90,   fill="blue",      tags="container_item")
canvas.create_text(125, 100, text="Item2", font=("Arial", 14), tags="container_item")


def move_container(container, dx, dy):
    canvas.move(canvas.find_withtag(container), dx, dy)
    for item in canvas.find_withtag(container + "_item"):
        canvas.move(item, dx, dy)

# Container should get smaller From the top to bottom. Items should get smaller from the top-right corner to left bottom.
# Container resize should trigger collision detection with items. 
def resize_container(container, y=None, x=None):
    print(canvas.coords(canvas.find_withtag("container")))
    x0, y0, x1, y1 = canvas.coords(canvas.find_withtag("container"))
    canvas.coords(canvas.find_withtag("container"), x0, y0+10, x1, y1)
    for item in canvas.find_withtag("container_item"):
        print("item", canvas.coords(canvas.find_withtag(item)))
        # Needs Handle text items and handle rectangle items separately.
        #ix0, iy0, ix1, iy1 = canvas.coords(item)
        #print(ix0, iy0, ix1, iy1)
        #canvas.coords(item, ix0, iy0+10, ix1-10, iy1)
    pass
tkinter.Button(window, text="Move", command=lambda: move_container("container", 10, 10)).pack()
tkinter.Button(window, text="Resize", command=lambda: resize_container("container", 10, 10)).pack()

window.mainloop()