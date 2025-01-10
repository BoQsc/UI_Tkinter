import tkinter
window = tkinter.Tk()

canvas = tkinter.Canvas(window, bg="black")
canvas.pack()

container = canvas.create_rectangle(50, 50, 200, 150, fill="lightgray")

items = []

item1 = canvas.create_oval(70, 70, 90, 90, fill="blue")
item2 = canvas.create_text(125, 100, text="Item2", font=("Arial", 14))
items.append(item1)
items.append(item2)

def move_container(dx, dy):
    canvas.move(container, dx, dy)
    for item in items:
        canvas.move(item, dx, dy)

button = tkinter.Button(window, text="Move", command=lambda: move_container(10, 10))
button.pack()

window.mainloop()