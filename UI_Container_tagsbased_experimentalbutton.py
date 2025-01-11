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
def resize_container(container, y=None, x=None): 
    pass


button = canvas.create_rectangle(10, 10, 150, 100, fill="green", outline="red")
text_id = canvas.create_text(80, 55, text="Click Me!", fill="white", font=("Arial", 12))
canvas.tag_bind(button, '<Button-1>', lambda args: move_container("container", 10, 10))

button = tkinter.Button(window, text="Move", command=lambda: move_container("container", 10, 10))
button.pack()



window.mainloop()