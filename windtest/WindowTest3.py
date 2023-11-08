from tkinter import *

from tkinter.ttk import Combobox


def change(e):
    t = cb.get()
    for k in range(len(names)):
        if t == names[k]:
            lbl.configure(image=imgs[k])


path = ".\\image\\"
names = ["Тигр", "Летучая мышь", "Нарвал", "Хорёк"]
files = ["Тигр.png", "Летучая мышь.png", "Нарвал.png", "Хорёк.png"]

wnd = Tk()
wnd.title("Звери")
wnd.geometry("420x370")
wnd.resizable(False, False)

imgs = [PhotoImage(file=path+f) for f in files]
index = 0

lbl = Label(wnd, image=imgs[index])
lbl.place(x=10, y=10, width=400, height=240)

cb = Combobox(values=names, state="readonly")
cb.configure(font=("", 11, "bold"))
cb.bind("<<ComboboxSelected>>", change)
cb.place(x=10, y=260, width=400, height=30)

btn = Button(wnd, text="OK")
btn.configure(command=wnd.destroy)
btn.place(x=120, y=300, width=160, height=30)

wnd.mainloop()

