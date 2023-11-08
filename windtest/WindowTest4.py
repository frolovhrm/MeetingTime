from tkinter import *


def getFont():
    res = []
    name = lst.get(lst.curselection())
    size = scl.get()
    res.append(name)
    res.append(size)

    if bold.get() != "":
        res.append(bold.get())
    if italic.get() != "":
        res.append(italic.get())
    return res


def setALL(*args):
    fnt = getFont()
    lbl.configure(font=fnt)
    lbl.configure(fg=color.get())
    txt = "\nШрифт "
    txt += fnt[0]
    txt += " размера " + str(fnt[1])+"\n"
    if "bold" in fnt:
        txt += " жирный"
    if "italic" in fnt:
        txt += " курсивный"
    if color.get() == "red":
        txt += " красного"
    if color.get() == "blue":
        txt += " синего"
    if color.get() == "black":
        txt += " черного"
    txt += " цвета\n"
    text.set(txt)


fnt_1 = ["Arial", 12, "italic"]
fnt_2 = ["Times New Roman", 13, "bold", "italic"]

fonts = ["Times New Roman", "Arial", "Courier New"]

min_size = 15
max_size = 21

W = 640
H = 420

Hf = 140
Wl = W / 3
Hl = H - Hf - 15
Hb = 60
Ws = W - Wl - 15
Hs = Hl - Hb - 5

wnd = Tk()
wnd.title("Параметры шрифта")
wnd.geometry(str(W) + "x" + str(H))
wnd.resizable(False, True)

frm_scale = Frame(wnd, bd=3, relief=GROOVE)
frm_text = Frame(wnd, bd=3, relief=GROOVE)
frm_btn = Frame(wnd, bd=3, relief=GROOVE)
frm_list = Frame(wnd, bd=3, relief=GROOVE)
frm_check = Frame(frm_list, bd=3, relief=GROOVE)

text = StringVar()
color = StringVar()
bold = StringVar()
italic = StringVar()

lbl_text = Label(frm_text, text="Пример текста:", font=fnt_2)
lbl_color = Label(frm_scale, text="Цвет текста:", font=fnt_2)
lbl_size = Label(frm_scale, text="Размер текста:", font=fnt_2)
lbl_font = Label(frm_list, text="Название шрифта:", font=fnt_2)
lbl_style = Label(frm_check, text="Стиль шрифта:", font=fnt_2)

lbl = Label(frm_text, textvariable=text)
lbl.configure(bg="white", relief=RAISED)

rb_1 = Radiobutton(frm_scale, text="красный", variable=color)
rb_1.configure(value="red", font=fnt_1)
rb_2 = Radiobutton(frm_scale, text="синий", variable=color)
rb_2.configure(value="blue", font=fnt_1)
rb_3 = Radiobutton(frm_scale, text="черный", variable=color)
rb_3.configure(value="black", font=fnt_1)

color.set("blue")

scl = Scale(frm_scale, orient=HORIZONTAL)
scl.configure(from_=min_size, to=max_size)
scl.configure(tickinterval=1, resolution=1)
scl.config(command=setALL)

chb_1 = Checkbutton(frm_check, text="жирный", variable=bold)
chb_1.configure(onvalue="bold", offvalue="", font=fnt_1)
chb_2 = Checkbutton(frm_check, text="курсив", variable=italic)
chb_2.configure(onvalue="italic", offvalue="", font=fnt_1)

bold.set("")
italic.set("italic")

lst = Listbox(frm_list, selectmode=SINGLE, font=fnt_1)
lst.configure(bg="gray96", selectbackground="gray")
lst.configure(activestyle="none", height=len(fonts)+1)

for n in fonts:
    lst.insert(END, n)

lst.select_set(0)
lst.bind("<<ListboxSelect>>", setALL)

btn = Button(frm_btn, text="OK", font=fnt_2)
btn.configure(command=wnd.destroy)

lbl_text.pack(side="top", fill="x", padx=5, pady=5)
lbl.pack(side="top", fill="both", padx=5, pady=5)
lbl_color.pack(side="top", fill="x", padx=5, pady=5)
scl.pack(side="bottom", fill="x", padx=5, pady=5)
lbl_size.pack(side="bottom", fill="x", padx=5, pady=[25, 5])
lbl_font.pack(side="top", fill="x", padx=5, pady=5)
lbl_style.pack(side="top", fill="x", padx=5, pady=5)

rb_1.pack(side="left", fill="x", padx=5, pady=5)
rb_2.pack(side="left", fill="x", padx=5, pady=5)
rb_3.pack(side="left", fill="x", padx=5, pady=5)

chb_1.pack(side="left", fill="x", padx=5, pady=5)
chb_2.pack(side="left", fill="x", padx=5, pady=5)

lst.pack(side="top", fill="x", padx=5, pady=5)

btn.pack(side="bottom", fill="x", padx=50, pady=10)

frm_text.place(x=5, y=5, width=W-10, height=Hf)
frm_check.pack(side="bottom", fill="both", padx=5, pady=5)
frm_list.place(x=5, y=Hf+10, height=Hl, width=Wl)
frm_scale.place(x=Wl+10, y=Hf+10, width=Ws, height=Hs)
frm_btn.place(x=Wl+10, y=Hf+Hs+15, width=Ws, height=Hb)

setALL()

color.trace("w", setALL)
bold.trace("w", setALL)
italic.trace("w", setALL)

wnd.mainloop()
