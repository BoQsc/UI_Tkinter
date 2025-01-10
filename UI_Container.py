import tkinter
window = tkinter.Tk()

canvas = tkinter.Canvas(window, bg="black")
canvas.pack()

container = canvas.create_rectangle(50, 50, 300, 100, fill="lightgray")
item1 = canvas.create_rectangle(70, 70, 90, 90, fill="blue")
item2 = canvas.create_text(125, 100, text="Item2", font=("Arial", 14))
items = [item1, item2]

def move_container(dx, dy):
    canvas.move(container, dx, dy)
    for item in items:
        canvas.move(item, dx, dy)

def resize_container():
    pass

button = tkinter.Button(window, text="Move", command=lambda: move_container(10, 10))
button.pack()

window.mainloop()