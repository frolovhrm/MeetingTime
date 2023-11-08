from tkinter import *


def clicked():
    global t
    t = txt.get()
    wnd.destroy()


wnd = Tk()
wnd.title("Давайте познакомимся")
wnd.geometry("300x120")
wnd.resizable(False, False)
fnt_1 = ("Cosmic", 13, "bold")
fnt_2 = ("Cosmic", 13, "italic")
fnt_3 = ("Cosmic", 10, "bold")
t = ""

lbl = Label(master=wnd, text="Как вас зовут?", foreground="#01579B")
lbl.configure(font=fnt_1)
lbl.place(x=10, y=20)

txt = Entry(master=wnd, width=30)
txt.configure(font=fnt_2)
txt.place(x=10, y=50)

btn_1 = Button(master=wnd, text="OK")
btn_2 = Button(master=wnd, text="Отмена")

btn_1.configure(font=fnt_3)
btn_1.configure(command=clicked)
btn_2.configure(font=fnt_3)
btn_2.configure(command=wnd.destroy)

btn_1.place(x=40, y=80, width=100, height=30)
btn_2.place(x=150, y=80, width=100, height=30)

wnd.mainloop()

if t != "":
    msg = Tk()
    msg.title("Знакомство состоялось")
    msg.geometry("320x100")
    msg.resizable(False, False)

    lbl = Label(master=msg, text="Очень приятно, " + t + "!", relief=GROOVE)
    lbl.configure(font=fnt_1)
    lbl.place(x=10, y=10, height=40, width=300)

    btn = Button(master=msg, text="OK")
    btn.configure(font=fnt_3)
    btn.configure(command=msg.destroy)
    btn.place(x=110, y=60, width=100, height=30)

    msg.mainloop()
