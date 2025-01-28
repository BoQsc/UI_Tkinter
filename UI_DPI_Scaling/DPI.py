import tkinter

window = tkinter.Tk()
canvas = tkinter.Canvas(window, bg="blue")
canvas.pack()

print("screen_width: ", window.winfo_screenwidth())
print("screen_height: ", window.winfo_screenheight())
print("window_width: ", window.winfo_width())
print("window_height: ", window.winfo_height())
print("dpi (pixels per inch): ", window.winfo_fpixels('1i'))  # '1i' is the Tkinter unit for 1 inch
print("winfo_pixels: ", window.winfo_pixels("1i"))

window.mainloop()