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

def resize_container(): # Container gets smaller From the top. Items get smaller from the top as well.
    pass

button = tkinter.Button(window, text="Move", command=lambda: move_container("container", 10, 10))
button.pack()

window.mainloop()