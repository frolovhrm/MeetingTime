from tkinter import *
from tkcalendar import Calendar
from tkinter.ttk import Combobox
from tkinter import ttk
import datetime
from datetime import time

date_now = datetime.datetime.now()
meet_start = date_now
meet_end = date_now
delta_meets_minutes = 0
num_of_pers = 0
num_of_room = 0
delta_meets_hour = 0
list_room = [1]
table_meet = []
all_hours = [f"{h:02}" for h in range(0, 24)]

meeting_rooms_work_time = [[9, 18, 10],
                           [9, 18, 10]]  # список всех переговорок с параметрами [начало работы, конец, места]
meetings_time = []  # список всех встреч [start, finish, num_of_pers]
working_start = 9  # время начала работы по умолчанию
working_finish = 18  # время окончания работы по умолчанию
work_hours = ["09", "10", "11", "12", "13", "14", "15", "16", "17"]  # рабочие часы по умолчанию
works_minutes = ["00", "10", "20", "30", "40", "50"]  # шаг планирования по умолчанию
plan_step = ["05", "10", "15", "20", "30"]  # справочник шага планирования
text_meet = "Выберите дату-время\nначала и окончания встречи,\nукажите количество участников"  # базовый текст окна


# сохраняет данные планируемой встречи и закрывает программу
def make_plan():
    if delta_meets_minutes > 9:
        if num_of_pers > 0:
            this_meeting = [meet_start, meet_end, num_of_pers]
            print(this_meeting)
            wnd.destroy()
    else:
        text_meet_lb = "эту встречу запланировать невозможно\n\n измените параметры"
        lb_text_meet.set(text_meet_lb)


# Выводит данные в окно с описанием параметров планируемой встречи
def print_date():
    """Выводим время встречи в окно и проверяем полученные от пользователя данные"""
    global num_of_pers, delta_meets_hour
    global meet_end
    global meet_start
    global delta_meets_minutes
    text_meet_lb = ""

    if cb_start_hour.get() and cb_start_minute.get():
        make_date = cal.get_date() + " " + cb_start_hour.get() + ":" + cb_start_minute.get()
        meet_start = datetime.datetime.strptime(make_date, '%m/%d/%y %H:%M')
    else:
        meet_start = date_now
        print("нет времени начала")

    if cb_end_hour.get() and cb_end_minute.get():
        make_date = cal.get_date() + " " + cb_end_hour.get() + ":" + cb_end_minute.get()
        meet_end = datetime.datetime.strptime(make_date, '%m/%d/%y %H:%M')
    else:
        meet_end = date_now
        print("нет времени окончания")

    if meet_start >= date_now:
        if meet_end >= date_now:

            if meet_start < meet_end:
                delta_meets = meet_end - meet_start
                delta_meets_minutes = int(delta_meets.seconds / 60)
                if delta_meets_minutes > 59:
                    delta_meets_hour = int(delta_meets_minutes / 60)
                    delta_meets_minutes = delta_meets_minutes % 60

            else:
                delta_meets_minutes = 0
                text_meet_lb = "недопустимое время встречи!\n\n"

            try:
                num_of_pers = int(entry_pers.get())
                if num_of_pers < 1:
                    text_meet_lb = text_meet_lb + "необходимо цифрами ввести\n количество участников встречи"
                else:
                    text_meet_lb = f"начало встречи: \n{str(meet_start)}\n\n окончание встречи: \n{str(meet_end)}\n\n" \
                                   f"продолжительностью {delta_meets_hour} ч. {delta_meets_minutes} мин.\n\n " \
                                   f"количество участников {num_of_pers} чел. "
            except ValueError:
                text_meet_lb = text_meet_lb + "необходимо цифрами ввести\n количество участников встречи"

            # lb_text_meet.set(text_meet_lb)
    else:
        text_meet_lb = "Время встречи уже прошло!\n\n Выберите будущее время."

    lb_text_meet.set(text_meet_lb)


# сохраняет настройки программы
def save_settings():
    global work_hours
    work_hours.clear()
    ts = cb1_f4_start_work_hour.get()
    tf = cb2_f4_finish_work_hour.get()
    if ts and tf:
        if ts[0] == "0":
            ts.replace("0", "")
        if tf[0] == "0":
            tf.replace("0", "")
        work_start = int(ts)
        work_finish = int(tf)
        for wh in range(work_start, work_finish):
            work_hours.append(f"{wh:02}")
            cb_start_hour.configure(values=work_hours)
            cb_end_hour.configure(values=work_hours)
    print(work_hours)

    global works_minutes
    works_minutes.clear()
    stm = cb3_f4_step_work_minutes.get()
    if stm:
        if stm[0] == "0":
            stm.replace("0", "")
        for step in range(0, 60, int(stm)):
            works_minutes.append(f"{step:02}")
            cb_start_minute.configure(values=works_minutes)
            cb_end_minute.configure(values=works_minutes)
    print(works_minutes)

    global num_of_room
    global meeting_rooms_work_time
    global list_room
    work_start = 9  #
    work_finish = 18  #

    nr = entry_pers_f4.get()
    if nr != "":
        if int(nr) > 0:
            num_of_room = int(nr)
        meeting_rooms_work_time = []
        list_room = []
        for room in range(num_of_room):
            one_room_time = []
            room_volume = 10
            first_time = time(work_start, 0, 0)
            second_time = time(work_finish, 0, 0)
            one_room_time.append(first_time)
            one_room_time.append(second_time)
            one_room_time.append(room_volume)
            meeting_rooms_work_time.append(one_room_time)
            list_room.append(str(room + 1))
            cb1_f2_start_work_hour.configure(values=list_room)
        print(list_room)


# выводит данные о переговорке в таблицу
def save_room_volume():
    for table_row in table_rooms:
        tree.insert("", END, values=table_row)


# создает список для таблицы переговорок
def make_table_rooms(list_of_rooms):
    global table_meet
    table_meet = []
    for meet in range(len(list_of_rooms)):
        table_meet.append((meet + 1, list_of_rooms[meet][2]))
        print(table_meet)
    return table_meet


wnd = Tk()
wnd.title("MeetingTime")
wnd.geometry("560x360")
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

# Размещаем календарь с текущей датой
cal = Calendar(frame1, selectmode='day', year=date_now.year, month=date_now.month, day=date_now.day)
cal.place(x=20, y=20)

# создаем экземпляр класса для последующего обновления по требованию
lb_text_meet = StringVar()

"""Закладка №1. Встречи"""
lb1_start_hour = Label(frame1, text="Начало встречи", anchor="center")
lb1_start_hour.place(x=20, y=220, height=20, width=120)

lb1_end_hour = Label(frame1, text="Окончание встречи", anchor="center")
lb1_end_hour.place(x=140, y=220, height=20, width=150)

lb2_start_hour = Label(frame1, text="час.", anchor="center")
lb2_start_hour.place(x=20, y=265, height=20, width=60)
lb2_start_hour = Label(frame1, text="мин.", anchor="center")
lb2_start_hour.place(x=80, y=265, height=20, width=60)

lb2_end_hour = Label(frame1, text="час.", anchor="center")
lb2_end_hour.place(x=160, y=265, height=20, width=60)
lb2_end_hour = Label(frame1, text="мин.", anchor="center")
lb2_end_hour.place(x=220, y=265, height=20, width=60)

lb_text = Label(frame1, textvariable=lb_text_meet, bd=2, anchor="center")
lb_text.configure(relief=RAISED)
lb_text.place(x=285, y=20, height=185, width=255)

cb_start_hour = Combobox(frame1, values=work_hours, state="readonly")
cb_start_hour.place(x=20, y=240, height=25, width=60, )
cb_start_minute = Combobox(frame1, values=works_minutes, state="readonly")
cb_start_minute.place(x=80, y=240, height=25, width=60)

cb_end_hour = Combobox(frame1, values=work_hours, state="readonly")
cb_end_hour.place(x=155, y=240, height=25, width=60)

cb_end_minute = Combobox(frame1, values=works_minutes, state="readonly")
cb_end_minute.place(x=215, y=240, height=25, width=60)

lb_entry_pers = Label(frame1, text="Количество участников", anchor="center")
lb_entry_pers.place(x=285, y=220, width=255, height=25)
entry_pers = ttk.Entry(frame1)
entry_pers.place(x=410, y=260, width=55, height=25, anchor="center")

btn = Button(frame1, text="Проверить", command=print_date)
btn.place(x=20, y=290, width=255, height=25)

btn = Button(frame1, text="Запланировать", command=make_plan)
btn.place(x=285, y=290, width=255, height=25)

lb_text_meet.set(text_meet)

"""закладка №2. Переговорки"""
lb1_f2 = Label(frame2, text="Настройте параметры для каждой переговорной комнаты:", anchor="w")
lb1_f2.place(x=20, y=10, height=25, width=510)
lb1_f2 = Label(frame2, text="переговорная", anchor="w")
lb1_f2.place(x=20, y=50, height=25, width=90)
lb1_f2 = Label(frame2, text="для", anchor="w")
lb1_f2.place(x=190, y=50, height=25, width=40)
lb1_f2 = Label(frame2, text="человек", anchor="w")
lb1_f2.place(x=270, y=50, height=25, width=60)

cb1_f2_start_work_hour = Combobox(frame2, values=list_room, state="readonly")
cb1_f2_start_work_hour.place(x=110, y=50, height=25, width=70)

entry_volume_f2 = ttk.Entry(frame2)
entry_volume_f2.place(x=230, y=50, height=25, width=40)

btn1_f2 = Button(frame2, text="Ok", command=save_room_volume)
btn1_f2.place(x=350, y=50, width=60, height=25)

table_rooms = make_table_rooms(meeting_rooms_work_time)
columns = ("Номер переговорки", "Мест")
tree = ttk.Treeview(frame2, columns=columns, show="headings")
tree.place(x=20, y=100, height=150)
tree.configure()
tree.heading("Номер переговорки", text="Номер переговорки", anchor=W)
tree.heading("Мест", text="Мест", anchor=W)
tree.column("#1", stretch=NO, width=150)
tree.column("#2", stretch=NO, width=100)
for row in table_rooms:
    tree.insert("", END, values=row)

"""Закладка №4. Настройки"""
lb1_f4 = Label(frame4, text="Установите диапазон планирования рабочего времени:", anchor="w")
lb1_f4.place(x=10, y=10, height=25, width=510)
lb2_f4 = Label(frame4, text="c", anchor="w")
lb2_f4.place(x=10, y=35, height=25, width=510)
lb3_f4 = Label(frame4, text="по", anchor="w")
lb3_f4.place(x=120, y=35, height=25, width=510)

cb1_f4_start_work_hour = Combobox(frame4, values=all_hours, state="readonly")
cb1_f4_start_work_hour.place(x=30, y=35, height=25, width=60, )
cb2_f4_finish_work_hour = Combobox(frame4, values=all_hours, state="readonly")
cb2_f4_finish_work_hour.place(x=150, y=35, height=25, width=60)

lb4_f4 = Label(frame4, text="Установите шаг планирования времени:", anchor="w")
lb4_f4.place(x=10, y=80, height=25, width=510)
lb5_f4 = Label(frame4, text="минут", anchor="w")
lb5_f4.place(x=100, y=105, height=25, width=510)

cb3_f4_step_work_minutes = Combobox(frame4, values=plan_step, state="readonly")
cb3_f4_step_work_minutes.place(x=30, y=105, height=25, width=60)

lb6_f4 = Label(frame4, text="Установите количество доступных переговорных комнат:", anchor="w")
lb6_f4.place(x=10, y=150, height=25, width=510)
entry_pers_f4 = ttk.Entry(frame4)
entry_pers_f4.place(x=30, y=175, height=25, width=60)
lb7_f4 = Label(frame4, text="комнат", anchor="w")
lb7_f4.place(x=100, y=175, height=25, width=510)
lb8_f4 = Label(frame4, text="* после сохранения нового количества комнат текущие настройки переговорок сбросятся",
               anchor="w")
lb8_f4.place(x=10, y=200, height=25, width=510)

btn1_f4 = Button(frame4, text="Cохранить", command=save_settings)
btn1_f4.place(x=370, y=270, width=150, height=25)

"""Закладка №5. О программе"""
about_prog = "Данная программа разработана для облегчения процесса\nпланирования загрузки переговорных комнат" \
             "\n\nver 1.0\n\n\nАвтор: Алексей Фролов\n\n e-mail: frolovhome@yandex.ru"
lb_frame5 = Label(frame5, text=about_prog, anchor="center")
lb_frame5.place(x=10, y=10, height=320, width=510)

wnd.mainloop()
