import tkinter
window = tkinter.Tk()

canvas = tkinter.Canvas(bg="black")
canvas.pack()

canvas.create_rectangle(10,20,30,40, fill="red")

def on_window_event(event):
    if event.widget == window:
        print("test:", event.widget, event.width, event.height)


window.bind("<Configure>", on_window_event)

window.mainloop()