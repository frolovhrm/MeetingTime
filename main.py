from tkinter import *
from tkcalendar import Calendar
from tkinter.ttk import Combobox
from tkinter import ttk
import datetime

date_now = datetime.datetime.now()
meetstart = date_now
meetend = date_now
delda_minuts = 0
num_of_pers = 0
num_of_room = 0

text_meet = "Выберите дату-время\nначала и окончания встречи,\nукажите количество участников"



def make_plan():
    if delda_minuts > 9:
        if num_of_pers > 0:
            this_meeting = [meetstart, meetend, num_of_pers]
            print(this_meeting)
            wnd.destroy()
    else:
        text_meet = "эту встречу запланировать невозможно\n\n измените параметры"
        lb_text_meet.set(text_meet)

def printdate():
    """Выводим время встречи в окно и проверяем полученные от пользователя данные"""
    global num_of_pers
    global meetend
    global meetstart
    global delda_minuts
    text_meet = ""
    
    if cb_start_hour.get() and cb_start_minute.get():
        make_date = cal.get_date() + " " + cb_start_hour.get() + ":" + cb_start_minute.get()
        meetstart = datetime.datetime.strptime(make_date, '%m/%d/%y %H:%M')
    else:
        meetstart = date_now
        print("нет времени начала")

    if cb_end_hour.get() and cb_end_minute.get():
        make_date = cal.get_date() + " " + cb_end_hour.get() + ":" + cb_end_minute.get()
        meetend = datetime.datetime.strptime(make_date, '%m/%d/%y %H:%M')
    else:
        meetend = date_now
        print("нет времени окончания") 

    if meetstart >= date_now:
        if meetend >= date_now:


            if  meetstart < meetend:
                delta = meetend - meetstart
                delda_minuts = int((delta.seconds)/60)
            else:
                delda_minuts = 0
                text_meet = "недопустимое время встречи!\n\n"

            try:
                num_of_pers = int(entry_pers.get())
                if num_of_pers < 1:
                        text_meet = text_meet + "необходимо цифрами ввести\n количество участников встречи"
                else:
                    text_meet = f"начало встречи \n{str(meetstart)}\n\n окончание встречи \n{str(meetend)}\n\n продолжительность {delda_minuts} минут\n\n количество участников {num_of_pers}"
            except:
                text_meet = text_meet + "необходимо цифрами ввести\n количество участников встречи"

            # lb_text_meet.set(text_meet)
    else:
        text_meet = "Время встречи уже прошло!\n\n Выберите будущее время."

        
    lb_text_meet.set(text_meet)

def seve_settings():
    global work_hours
    work_hours.clear()
    ts = cb1_f4_start_work_hour.get()
    tf = cb2_f4_finish_work_hour.get()
    if ts and tf:
        if ts[0] == "0":
            ts.replace("0", "")
        if tf[0] == "0":
            tf.replace("0", "")
        for wh in range(int(ts), int(tf)):
            work_hours.append(f"{wh:02}")
            cb_start_hour.configure(values=work_hours)
            cb_end_hour.configure(values=work_hours)
    print(work_hours)

    global works_minuts
    works_minuts.clear()
    stm = cb3_f4_step_work_minutes.get()
    if stm:
        if stm[0] == "0":
            stm.replace("0", "")
        for step in range(0, 60, int(stm)):
            works_minuts.append(f"{step:02}")
            cb_start_minute.configure(values=works_minuts)
            cb_end_minute.configure(values=works_minuts)
    print(works_minuts)

    global num_of_room
    nr = entry_pers_f4.get()
    if nr !="":
        if int(nr) > 0:
            num_of_room = int(nr)
    print(num_of_room)


wnd = Tk()
wnd.title("MeetingTime")
wnd.geometry("540x350")
wnd.resizable(False, False)

notebook = ttk.Notebook(wnd)
notebook.pack(expand=True, fill=BOTH)
 
# создаем фреймы
frame1 = ttk.Frame(notebook)
frame2 = ttk.Frame(notebook)
frame3 = ttk.Frame(notebook)
frame4 = ttk.Frame(notebook)
frame5 = ttk.Frame(notebook)
frame1.pack(fill=BOTH, expand=True)
frame2.pack(fill=BOTH, expand=True)
frame3.pack(fill=BOTH, expand=True)
frame4.pack(fill=BOTH, expand=True)
frame5.pack(fill=BOTH, expand=True)

# добавляем фреймы в качестве вкладок
notebook.add(frame1, text=" Встречи ")
notebook.add(frame2, text=" Переговорки ")
notebook.add(frame3, text=" Отчет ")
notebook.add(frame4, text=" Настройки ")
notebook.add(frame5, text=" О программе ")

all_hours = []
for h in range(0,24):
    all_hours.append(f"{h:02}")

work_hours = ["09", "10", "11", "12", "13", "14", "15", "16", "17"]
works_minuts = ["00", "10", "20", "30", "40", "50"]
plan_step = ["05", "10", "15", "20", "30"]

this_day = datetime.datetime.now()
cal = Calendar(frame1, selectmode='day', year=this_day.year, month=this_day.month, day=this_day.day)
cal.place(x=10, y=10)

lb_text_meet = StringVar()


"""Закладка №1. Встречи"""
lb1_start_hour = Label(frame1, text="Начало встречи",  anchor="center")
lb1_start_hour.place(x=10, y=210, height=20, width=120)

lb1_end_hour = Label(frame1, text="Окончание встречи", anchor="center")
lb1_end_hour.place(x=130, y=210, height=20, width=150)

lb2_start_hour = Label(frame1, text="час.",  anchor="center")
lb2_start_hour.place(x=10, y=255, height=20, width=60)
lb2_start_hour = Label(frame1, text="мин.", anchor="center")
lb2_start_hour.place(x=70, y=255, height=20, width=60)

lb2_end_hour = Label(frame1, text="час.",  anchor="center")
lb2_end_hour.place(x=10+140, y=255, height=20, width=60)
lb2_end_hour = Label(frame1, text="мин.", anchor="center")
lb2_end_hour.place(x=70+140, y=255, height=20, width=60)

lb_text = Label(frame1, textvariable=lb_text_meet, anchor="center")
lb_text.configure(relief=RAISED)
lb_text.place(x=275, y=10, height=185, width=255)

cb_start_hour = Combobox(frame1, values=work_hours, state="readonly")
cb_start_hour.place(x=10, y=230, height=25, width=60,)
cb_start_minute = Combobox(frame1, values=works_minuts, state="readonly")
cb_start_minute.place(x=70, y=230, height=25, width=60)

cb_end_hour = Combobox(frame1, values=work_hours, state="readonly")
cb_end_hour.place(x=145, y=230, height=25, width=60)

cb_end_minute = Combobox(frame1, values=works_minuts, state="readonly")
cb_end_minute.place(x=205, y=230, height=25, width=60)

lb_entry_pers = Label(frame1, text="Количество участников", anchor="center")
lb_entry_pers.place(x=275, y=210, width=255, height=25)
entry_pers = ttk.Entry(frame1)
entry_pers.place(x=400, y=250, width=55, height=25, anchor="center")

btn = Button(frame1, text="Проверить", command=printdate)
btn.place(x=10, y=280, width=255, height=25)

btn = Button(frame1, text="Запланировать", command=make_plan)
btn.place(x=275, y=280, width=255, height=25)

lb_text_meet.set(text_meet)

"""Закладка №4. Настройки"""
lb1_f4 = Label(frame4, text="Установите диапазон планирования рабочего времени:",  anchor="w")
lb1_f4.place(x=10, y=10, height=25, width=510)
lb2_f4 = Label(frame4, text="c",  anchor="w")
lb2_f4.place(x=10, y=35, height=25, width=510)
lb3_f4 = Label(frame4, text="по",  anchor="w")
lb3_f4.place(x=120, y=35, height=25, width=510)

cb1_f4_start_work_hour = Combobox(frame4, values=all_hours, state="readonly")
cb1_f4_start_work_hour.place(x=30, y=35, height=25, width=60,)
cb2_f4_finish_work_hour = Combobox(frame4, values=all_hours, state="readonly")
cb2_f4_finish_work_hour.place(x=150, y=35, height=25, width=60)

lb4_f4 = Label(frame4, text="Установите шаг планирования времени:",  anchor="w")
lb4_f4.place(x=10, y=80, height=25, width=510)
lb5_f4 = Label(frame4, text="минут",  anchor="w")
lb5_f4.place(x=100, y=105, height=25, width=510)

cb3_f4_step_work_minutes = Combobox(frame4, values=plan_step, state="readonly")
cb3_f4_step_work_minutes.place(x=30, y=105, height=25, width=60)

lb6_f4 = Label(frame4, text="Установите количество доступных переговорных комнат:",  anchor="w")
lb6_f4.place(x=10, y=150, height=25, width=510)
entry_pers_f4 = ttk.Entry(frame4)
entry_pers_f4.place(x=30, y=175, height=25, width=60)
lb7_f4 = Label(frame4, text="комнат",  anchor="w")
lb7_f4.place(x=100, y=175, height=25, width=510)


btn1_f4 = Button(frame4, text="Cохранить", command=seve_settings)
btn1_f4.place(x=370, y=270, width=150, height=25)


"""Закладка №5. О программе"""
about_prog = "Данная программа разработана для облегчения процесса\nпланирования загрузки переговорных комнат\n\nver 1.0\n\n\nАвтор: Алексей Фролов\n\n e-mail: frolovhome@yandex.ru"
lb_frame5 = Label(frame5, text=about_prog,  anchor="center")
lb_frame5.place(x=10, y=10, height=320, width=510)


"""Начало и окончание рабочего времени. Шаг планированияю. Количество мест в переговорке."""

wnd.mainloop()