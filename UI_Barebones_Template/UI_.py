import tkinter

window = tkinter.Tk()
canvas = tkinter.Canvas(window, bg="blue")
canvas.pack()


def on_resize(event):
    if event.widget == window:
        print("window_width: ", window.winfo_width())
        print("window_height: ", window.winfo_height())


window.bind('<Configure>', on_resize)
window.mainloop()