from tkinter import *
# icon_win = PhotoImage(file="C:\\Python projects\\SA\\wi.png")

wnd = Tk()
wnd.title("Простое окно")
# wnd.iconphoto(True, icon_win)
wnd.geometry("250x500")
wnd.resizable(False, False)
lbl = Label(wnd, text="Всем привет!", font=('', 20))
lbl.place(x=40, y=30)
btn = Button(wnd, text="Закрыть", font=("", 13), command=wnd.destroy)
btn.place(x=40, y=100, width=170, height=30)

wnd.mainloop()
quit()
