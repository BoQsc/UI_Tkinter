import tkinter
window = tkinter.Tk()

canvas = tkinter.Canvas(bg="black")
canvas.pack()

canvas.create_rectangle(10,20,30,40, fill="red")

window.size = (window.winfo_width(), window.winfo_height())
window.pos = (window.winfo_x(), window.winfo_y())

def on_configure(event):
    if event.widget == window: # IMPORTANT
        if (event.width, event.height) != window.size:
            print(f"Resized to {event.width}x{event.height}")
            window.size = (event.width, event.height)
        if (event.x, event.y) != window.pos:
            print(f"Moved to ({event.x}, {event.y})")
            window.pos = (event.x, event.y)

window.bind("<Configure>", on_configure)

window.mainloop()