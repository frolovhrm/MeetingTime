from tkinter import *
from tkcalendar import Calendar
from tkinter.ttk import Combobox
from tkinter import ttk
import datetime
from datetime import time
import sqlite3 as sq

from settings import count_room, seve_program_settings, load_program_settings
from creat_db import createNewBase


base_name = "meetingtime.db"
createNewBase()
DATE_NOW = datetime.datetime.now()



""" Список переменных с начальными значениями(по умолчанию) """
# list_room = [1, 2] # список номеров комнат
properties_of_meeting_rooms = [[50, "no", "no"], [50, "no", "no"]]  # список всех переговорок с параметрами [кол-во мест, свойство1, свойстово2]
# work_hours, works_minutes, properties_of_meeting_rooms = load_program_settings()
list_room = count_room(properties_of_meeting_rooms)
# working_start = 9  # время начала работы
# working_finish = 18  # время окончания работы
work_hours = ["09", "10", "11", "12", "13", "14", "15", "16", "17"]  # рабочие часы
works_minutes = ["00", "10", "20", "30", "40", "50"]  # шаг планирования
# date_meet = f"'{DATE_NOW.date()}'"
plans_all_miteeng_rooms = []
list_table_item = []






# обрабатывает дуйствие кнопки сохранения заявки на встречу и вызывает фцнкцию записи в базу
def plan_this_meet():
    drawn_up_plan, meet_start, meet_end, persons_of_meeting = check_end_view_meet_date()
    if drawn_up_plan:
        push_base_new_metting(meet_start, meet_end, persons_of_meeting)
    else:
        text_meet_lb = "эту встречу запланировать невозможно\n\n проверьте параметры"
        lb_text_meet.set(text_meet_lb)


# Выводит данные в окно с описанием параметров планируемой встречи
def check_end_view_meet_date():
    """Выводим время встречи в окно и проверяем полученные от пользователя данные"""
    # meet_start = DATE_NOW
    # meet_end = DATE_NOW
    persons_of_meeting = 0
    drawn_up_plan: bool = False
    # text_meet_lb = ""

    if cb_start_hour.get() and cb_start_minute.get():
        make_date = cal.get_date() + " " + cb_start_hour.get() + ":" + cb_start_minute.get()
        meet_start = datetime.datetime.strptime(make_date, '%m/%d/%y %H:%M')
    else:
        meet_start = False
        # print("нет времени начала")

    if cb_end_hour.get() and cb_end_minute.get():
        make_date = cal.get_date() + " " + cb_end_hour.get() + ":" + cb_end_minute.get()
        meet_end = datetime.datetime.strptime(make_date, '%m/%d/%y %H:%M')
    else:
        meet_end = False
        # print("нет времени окончания")

    if meet_start is not False and meet_end is not False:
        # проверяем длительность встречи
        if meet_start >= DATE_NOW:
            if meet_end >= DATE_NOW:
                if meet_start <= meet_end:
                    delta_meets = meet_end - meet_start
                    all_delta_meets_minutes = int(delta_meets.seconds / 60)
                    # print(all_delta_meets_minutes)

                    if all_delta_meets_minutes > 1:
                        # проверяем есть ли часы в минутах
                        if all_delta_meets_minutes > 59:
                            delta_meets_hour = int(all_delta_meets_minutes / 60)
                            delta_meets_minutes = all_delta_meets_minutes % 60
                        else:
                            delta_meets_hour = 0
                            delta_meets_minutes = all_delta_meets_minutes

                        # проверяем количество персон на встрече
                        try:
                            persons_of_meeting = int(entry_pers.get())
                            if persons_of_meeting > 1:
                                text_meet_lb = f"начало встречи: \n{str(meet_start)}\n\n окончание встречи: \n{str(meet_end)}\n\n" \
                                               f"продолжительностью {delta_meets_hour} ч. {delta_meets_minutes} мин.\n\n " \
                                               f"количество участников {persons_of_meeting} чел. "
                                drawn_up_plan = True
                            else:
                                text_meet_lb = "необходимо цифрами ввести\n количество участников встречи"
                        except ValueError:
                            text_meet_lb = "необходимо цифрами ввести\n количество участников встречи"
                    else:
                        text_meet_lb = "продолжительность встречи\nслишком мала\n"
                else:
                    text_meet_lb = "продолжительность встречи\nслишком мала\n"
            else:
                text_meet_lb = "Время встречи уже прошло!\n\n Выберите будущее время."
        else:
            text_meet_lb = "Время встречи уже прошло!\n\n Выберите будущее время."
    else:
        text_meet_lb = "Введите корректные время начала\nи окончания встречи"

    lb_text_meet.set(text_meet_lb)

    return drawn_up_plan, meet_start, meet_end, persons_of_meeting


# сохраняет настройки программы
def get_and_save_program_settings():
    global work_hours
    work_hours.clear()
    ts = cb1_f5_start_work_hour.get()
    tf = cb2_f5_finish_work_hour.get()
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
    stm = cb3_f5_step_work_minutes.get()
    if stm:
        if stm[0] == "0":
            stm.replace("0", "")
        for step in range(0, 60, int(stm)):
            works_minutes.append(f"{step:02}")
            cb_start_minute.configure(values=works_minutes)
            cb_end_minute.configure(values=works_minutes)
    print(works_minutes)

    global properties_of_meeting_rooms
    # if work_start = 9  #
    # work_finish = 18  #

    try:
        num_of_room = int(entry_pers_f5.get())
        if num_of_room <= 0:
            return
        if num_of_room > 12:
            num_of_room = 12
        properties_of_meeting_rooms = []
        list_room = []
        for room in range(num_of_room):
            one_room_prop = []
            room_volume = 0
            room_prop1 = "no"
            room_prop2 = "no"
            one_room_prop.append(room_volume)
            one_room_prop.append(room_prop1)
            one_room_prop.append(room_prop2)
            properties_of_meeting_rooms.append(one_room_prop)
            list_room.append(str(room + 1))  # создаем новый список комнат
            reload_meetingrooms_table(create_table_meetingrooms_as_text())
        cb1_f2_meetroom_number.configure(values=list_room)  # загружаем новый список в чекбокс f2
        print(properties_of_meeting_rooms)
        seve_program_settings(work_hours, works_minutes, properties_of_meeting_rooms)
    except:
        pass


# создает таблицу всех переговорок
def create_table_meetingrooms_as_text():
    text = "Комната\t\tЧеловек\t\tОпция1\t\tОпция2\n"
    for num_room in range(len(properties_of_meeting_rooms)):
        text += f" {num_room + 1}\t\t{properties_of_meeting_rooms[num_room][0]}\t\t{properties_of_meeting_rooms[num_room][1]}\t\t{properties_of_meeting_rooms[num_room][2]}\n"
    return text


# размещает таблицу переговорок в окне
def reload_meetingrooms_table(text):
    lbl2_f2.configure(text=text, anchor="nw")


# меняет количество участников в существующих переговорках
def edit_meetingroom_table(): 
    number_room = int(cb1_f2_meetroom_number.get())
    new_room_volume = int(e1_f2_volume_of_meetingroom.get())
    properties_of_meeting_rooms[number_room - 1][0] = new_room_volume
    reload_meetingrooms_table(create_table_meetingrooms_as_text())


# сохраняет в базу заявку на новую встречу
def push_base_new_metting(meet_start, meet_end, persons_of_meeting):
    with sq.connect(base_name) as con:
        # print(meet_start, meet_end, persons_of_meeting)
        date_meet = meet_start.date()
        time_start = meet_start.time().strftime("%H.%M")
        time_end = meet_end.time().strftime("%H.%M")
        cursor = con.cursor()
        # print(date_meet, time_start, time_end, persons_of_meeting)
        cursor.execute('INSERT INTO Meetings (datemeet, timestart, timeend, quantity) VALUES (?, ?, ?, ?)', (date_meet, str(time_start), str(time_end), persons_of_meeting))
    get_all_unique_date_from_base()


# получает из базы список всех встреч на указанную дату и выводит в окно
def get_from_base_meeting_for_a_day():
    list = get_all_unique_date_from_base()
    cb3_f3_date.configure(values=list)
    
    date_meet = check_date_box_in_the_planing_frame()
    with sq.connect(base_name) as con:
        # print(date_meet)
        date_meet = f"{date_meet}"
        cursor = con.cursor()
        # print(date_meet)
        text = f"SELECT * FROM Meetings WHERE datemeet = {date_meet}"
        # print(text)
        cursor.execute(text)
        list_meet_one_date = cursor.fetchall()
        # print(list_meet_one_date)
        text_meet_lb2 = "\n\n\tвстречи не найдены"
        if list_meet_one_date:
            text_meet_lb2 = " "
            for i in range(len(list_meet_one_date)):
                num_meet = list_meet_one_date[i][0]
                time_start = list_meet_one_date[i][2]
                time_end = list_meet_one_date[i][3]
                persons_of_meeting = list_meet_one_date[i][4]
                text_meet_lb2 += f"{num_meet}\t{date_meet}\t{time_start}\t\t{time_end}\t\t{persons_of_meeting}\n"

        lbl3_f3.configure(anchor="nw", text=text_meet_lb2)
        # print(list_meet_one_date)


# находит в базе все уникальные даты в которые есть встречи
def get_all_unique_date_from_base():
    with sq.connect(base_name) as con:
        cursor = con.cursor()
        text = f"SELECT DISTINCT datemeet FROM Meetings"
        cursor.execute(text)
        list_all_meet_date = cursor.fetchall()
        # print(f"список уникальных дат {list_all_meet_date}")
    return list_all_meet_date


# проверяет значение поля Дата в Отчете и воздращает данные
def check_date_box_in_the_planing_frame():
    date = cb3_f3_date.get()
    if date != "":
        date_meet = f"'{date}'"
    else:
        date_meet = f"'{DATE_NOW.date()}'"
    return date_meet


# проверяет значение поля Дата во Встречах и воздращает данные
def check_date_box_in_the_meeting_frame():
    date = cb3_f4_date.get()
    if date != "":
        date_meet = f"'{date}'"
    else:
        date_meet = f"'{DATE_NOW.date()}'"
    return date_meet


# возвращает выборку из базы, о всех встречах на дату
def get_meeting_list_on_this_date(this_date):
    date_meet = this_date
    with sq.connect(base_name) as con:
        cursor = con.cursor()
        text = f"SELECT * FROM Meetings WHERE datemeet = {date_meet}"
        cursor.execute(text)
        list_meet_one_date = cursor.fetchall()
    # print(f"get_meeting_list_on_this_date = {this_date} - {list_meet_one_date}")
    return list_meet_one_date


# помечает встречу в базе как запланированную
def make_meeting_as_planed():

    pass


# помечает встречу в базе как не запланированную
def make_meeting_as_unplaned():

    pass


# создает пустой шаблон плана встреч на дату
def make_base_plan_for_all_miteeng_rooms():
    global plans_all_miteeng_rooms
    plans_all_miteeng_rooms = []
    for i in range(len(properties_of_meeting_rooms)):
        plans_all_miteeng_rooms.append([])


# заполняет шаблон плана встреч на указанную дату
def creating_plan_all_rooms_this_day():
    global plans_all_miteeng_rooms
    plans_all_miteeng_rooms = []
    make_base_plan_for_all_miteeng_rooms()
    this_date = check_date_box_in_the_meeting_frame()
    print(f"Make a plan, for this_date - {this_date}")
    list_meet_one_date = get_meeting_list_on_this_date(this_date) # получаем список всех встреч из базы
    print(f"list_meet_one_date - {list_meet_one_date}")
    for meet in range(len(list_meet_one_date)): # начинаем искать место для каждой встречи
        if list_meet_one_date[meet][7] == 1: # если встреча отмечена как запланированная, пропускаем.
            break

        meet_num = list_meet_one_date[meet][0] # время начала встречи
        meet_start = list_meet_one_date[meet][2] # время начала встречи
        meet_end = list_meet_one_date[meet][3] # время окончания встречи
        meet_pers = int(list_meet_one_date[meet][4]) # кол-во участников встречи
        print(list_meet_one_date[meet])
        print(f"properties_of_meeting_rooms = {properties_of_meeting_rooms}")

        for room in range(len(properties_of_meeting_rooms)): # ищем в каждой переговорке
            volume = properties_of_meeting_rooms[room][0]   # кол-во мест в комнате
            if meet_pers <= volume:   # если мест хватает
                this_room_meeting_list = plans_all_miteeng_rooms[room] # получаем план встреч конкретной переговорки
                print(f"this_room_meeting_list = {this_room_meeting_list}")
                cros = False # пересечений нет 
                if this_room_meeting_list:  # если план не пустой
                    for i in range(len(this_room_meeting_list)):  # проверяем его на пересечения
                        print(f"\nПереговорка {room} ее встречи {this_room_meeting_list[i]}")
                        if meet_start >= this_room_meeting_list[i][1] and meet_start < this_room_meeting_list[i][2]:
                            print(f"существующая встреча {i} есть пересечение по старту {meet_start} <= {this_room_meeting_list[i][0]} или {meet_start} > {this_room_meeting_list[i][1]}")
                            cros = True
                        if meet_end <= this_room_meeting_list[i][1]  and meet_end > this_room_meeting_list[i][2]:
                            print(f"существующая встреча {i} есть пересечение по финишу {meet_end} => {this_room_meeting_list[i][0]} или {meet_end} < {this_room_meeting_list[i][1]}")
                            cros = True
                else:
                    print(f"\nВ переговорке {room} еще нет встреч, значит ", end="")
                    pass    
                if cros == False: # если пересечений ненашлось добавляем встречу в план комнаты
                    print(f"встречу № {meet} на {meet_pers} чел. проводим в комнате № {room} from {meet_start} to {meet_end}")
                    plans_all_miteeng_rooms[room].append([meet_num, meet_start, meet_end, meet_pers])
                    break
                else:
                    print(f"В переговорке {room} встреча № {meet} на {meet_pers} чел. незапланирована, нет свободного времени!")
                    continue

            else:   # если мест не хватает
                print(f"\nВстречу № {meet} на {meet_pers} чел. в комнате № {room} сделать не можем, мало места!")
                pass

    print(f"plans_all_miteeng_rooms {plans_all_miteeng_rooms}")
    return plans_all_miteeng_rooms


# выводит в консоль отчет о уже запланированных встречах на дату
def print_meetings_plan_on_date(list_meetings):
    for room in range(len(list_meetings)):
        for meeting in range(len(list_meetings[room])):
            print(f"Комната {room} встреча {list_meetings[room][meeting][0]} с {list_meetings[room][meeting][1]}  по {list_meetings[room][meeting][2]} на {list_meetings[room][meeting][3]} человек")


# создает отчет о уже запланированных встречах на дату
def make_list_for_table_meetings_plan_on_date(list_meetings):
    list_for_table_meetings_plan_on_date = []
    for room in range(len(list_meetings)):
        for meeting in range(len(list_meetings[room])):
            meet = (room, list_meetings[room][meeting][0], list_meetings[room][meeting][1], list_meetings[room][meeting][2], list_meetings[room][meeting][3])
            list_for_table_meetings_plan_on_date.append(meet)
    print(f"list_for_table_meetings_plan_on_date - {list_for_table_meetings_plan_on_date}")
    return list_for_table_meetings_plan_on_date


def drow_new_table_resive():
    global list_table_item
    for i in list_table_item:
        tree.delete(i)

    # получаем план всех встреч на дату

    plan_for_tree = creating_plan_all_rooms_this_day()
    meets = make_list_for_table_meetings_plan_on_date(plan_for_tree)

    list_table_item = []
    # добавляем данные
    for meet in meets:
        tree.insert("", END, values=meet)

    for meet in tree.get_children(""):
        list_table_item.append(meet)



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
frame6 = ttk.Frame(notebook)
frame1.pack(fill=BOTH, expand=True)
frame2.pack(fill=BOTH, expand=True)
frame3.pack(fill=BOTH, expand=True)
frame4.pack(fill=BOTH, expand=True)
frame5.pack(fill=BOTH, expand=True)
frame6.pack(fill=BOTH, expand=True)

# добавляем фреймы в качестве вкладок
notebook.add(frame1, text=" Заявки ")
notebook.add(frame2, text=" Переговорки ")
notebook.add(frame3, text=" Встречи ")
notebook.add(frame4, text=" Отчет ")
notebook.add(frame5, text=" Настройки ")
notebook.add(frame6, text=" О программе ")

# Размещаем календарь с текущей датой
cal = Calendar(frame1, selectmode='day', year=DATE_NOW.year, month=DATE_NOW.month, day=DATE_NOW.day)
cal.place(x=20, y=20)

# создаем экземпляр класса для последующего обновления по требованию
lb_text_meet = StringVar()

"""Закладка №1. Заявки"""
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

btn = Button(frame1, text="Проверить", command=check_end_view_meet_date)
btn.place(x=20, y=290, width=255, height=25)

btn = Button(frame1, text="Запланировать", command=plan_this_meet)
btn.place(x=285, y=290, width=255, height=25)

text_meet = "Выберите дату-время\nначала и окончания встречи,\nукажите количество участников"  # базовый текст окна
lb_text_meet.set(text_meet)

"""закладка №2. Переговорки"""
lb1_f2 = Label(frame2, text="Настройте параметры для каждой переговорной комнаты:", anchor="w")
lb1_f2.place(x=20, y=10, height=25, width=510)
lb2_f2 = Label(frame2, text="Комната                Человек                 Опция1                   Опция2", anchor="w")
lb2_f2.place(x=20, y=40, height=25, width=350)
lb3_f2 = Label(frame2, text="если нужно\nвведите новые\n параметры\n и подтвердите\n изменения", anchor="center")
lb3_f2.place(x=385, y=100, height=200, width=150)

cb1_f2_meetroom_number = Combobox(frame2, justify="center", values=list_room, state="readonly")
cb1_f2_meetroom_number.place(x=20, y=60, height=25, width=70)

e1_f2_volume_of_meetingroom = ttk.Entry(frame2, justify="center")
e1_f2_volume_of_meetingroom.place(x=120, y=60,  height=25, width=45)

e2_f2_volume_of_meetingroom = ttk.Entry(frame2, state=DISABLED)
e2_f2_volume_of_meetingroom.place(x=215, y=60, height=25, width=40)

e3_f2_volume_of_meetingroom = ttk.Entry(frame2, state=DISABLED)
e3_f2_volume_of_meetingroom.place(x=315, y=60, height=25, width=40)

btn1_f2 = Button(frame2, text="Изменить", command=edit_meetingroom_table)
btn1_f2.place(x=430, y=59, width=60, height=25)

lbl2_f2 = Label(frame2, text=create_table_meetingrooms_as_text(), anchor="nw", background="#FFFFFF")
lbl2_f2.place(x=20, y=100, height=220, width=340)

"""Закладка №3. Встречи"""
lbl1_f3 = Label(frame3, text="Дата", anchor="w")
lbl1_f3.place(x=20, y=15, height=25, width=80)

list = get_all_unique_date_from_base()
cb3_f3_date = Combobox(frame3, values=list, state="readonly")
cb3_f3_date.place(x=60, y=15, height=25, width=90)

lbl2_f3_text = "  #                 дата                   начало                окончание        кол-во"
lbl2_f3 = Label(frame3, text=lbl2_f3_text, anchor="w")
lbl2_f3.place(x=20, y=45, height=25, width=380)

lbl3_f3 = Label(frame3, text="нет встреч", anchor="center", background="#FFFFFF")
lbl3_f3.place(x=20, y=70, height=250, width=380)

btn1_f3 = Button(frame3, text="Проверить", command=get_from_base_meeting_for_a_day)
btn1_f3.place(x=430, y=15, width=80, height=25)

"""Закладка №4. Отчет"""
lbl1_f4 = Label(frame4, text="Дата", anchor="w")
lbl1_f4.place(x=20, y=15, height=25, width=80)

list = get_all_unique_date_from_base()
cb3_f4_date = Combobox(frame4, values=list, state="readonly")
cb3_f4_date.place(x=60, y=15, height=25, width=90)

btn1_f4 = Button(frame4, text="Планировать", command=drow_new_table_resive)
btn1_f4.place(x=430, y=15, width=90, height=25)

# определяем столбцы
columns = ("room", "num", "for", "to", "pers")

# создаем обект таблицу
tree = ttk.Treeview(frame4, columns=columns, show="headings")
tree.place(x=20, y=45, height=251, width=353)
 
# определяем заголовки
tree.heading("room", text="комната") 
tree.heading("num", text="встреча")
tree.heading("for", text="с")
tree.heading("to", text="по")
tree.heading("pers", text="чел.")

# настраиваем столбцы
tree.column("#1", stretch=NO, width=70)
tree.column("#2", stretch=NO, width=70)
tree.column("#3", stretch=NO, width=70)
tree.column("#4", stretch=NO, width=70)
tree.column("#5", stretch=NO, width=70)

"""Закладка №5. Настройки"""
lb1_f5 = Label(frame5, text="Установите диапазон планирования рабочего времени (в рамках одних суток):", anchor="w")
lb1_f5.place(x=10, y=10, height=25, width=510)
lb2_f5 = Label(frame5, text="c", anchor="w")
lb2_f5.place(x=10, y=35, height=25, width=510)
lb3_f5 = Label(frame5, text="по", anchor="w")
lb3_f5.place(x=120, y=35, height=25, width=510)

all_hours = [f"{h:02}" for h in range(0, 24)]
cb1_f5_start_work_hour = Combobox(frame5, values=all_hours, state="readonly")
cb1_f5_start_work_hour.place(x=30, y=35, height=25, width=60, )
cb2_f5_finish_work_hour = Combobox(frame5, values=all_hours, state="readonly")
cb2_f5_finish_work_hour.place(x=150, y=35, height=25, width=60)

lb4_f5 = Label(frame5, text="Установите шаг планирования времени:", anchor="w")
lb4_f5.place(x=10, y=80, height=25, width=510)
lb5_f5 = Label(frame5, text="минут", anchor="w")
lb5_f5.place(x=100, y=105, height=25, width=510)

plan_step = ["05", "10", "15", "20", "30"]  # справочник шага планирования времени
cb3_f5_step_work_minutes = Combobox(frame5, values=plan_step, state="readonly")
cb3_f5_step_work_minutes.place(x=30, y=105, height=25, width=60)

lb6_f5 = Label(frame5, text="Установите количество доступных переговорных комнат:", anchor="w")
lb6_f5.place(x=10, y=150, height=25, width=510)
entry_pers_f5 = ttk.Entry(frame5)
entry_pers_f5.place(x=30, y=175, height=25, width=60)
lb7_f5 = Label(frame5, text="комнат (max. 12)", anchor="w")
lb7_f5.place(x=100, y=175, height=25, width=510)
lb8_f5 = Label(frame5, foreground="red", text="Внимание! После сохранения новых параметров\n" \
               "текущие настройки программы изменятся, и все будущие встречи перейдут в статус незапланировано.", anchor="w")
lb8_f5.place(x=10, y=210, height=60, width=510)

btn1_f5 = Button(frame5, text="Cохранить", command=get_and_save_program_settings)
btn1_f5.place(x=370, y=270, width=150, height=25)

"""Закладка №6. О программе"""
about_prog = "Данная программа разработана для облегчения процесса\nпланирования загрузки переговорных комнат" \
             "\n\nver 1.0\n\n\nАвтор: Алексей Фролов\n\n\n e-mail: frolovhome@yandex.ru"
lb_f6 = Label(frame6, text=about_prog, anchor="center")
lb_f6.place(x=10, y=10, height=320, width=510)


wnd.mainloop()
