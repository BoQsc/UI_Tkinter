import tkinter
window = tkinter.Tk()

canvas = tkinter.Canvas(bg="black")
canvas.pack()

canvas.create_rectangle(10,20,30,40, fill="red")


window.bind("<Configure>", lambda event:
    print("test:", event.widget, event.width, event.height)
)
window.mainloop()