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
list_room = [1]
persons_of_meeting = 0
# num_of_room = 0
delta_meets_hour = 0
# list_for_table_meetingrooms = [[1,10]]
all_hours = [f"{h:02}" for h in range(0, 24)]

properties_of_meeting_rooms = [[9, 18, 0, "no", "no"]]  # список всех переговорок с параметрами [начало работы, конец, кол-во мест]
all_meetings_list = []  # список всех встреч [start, finish, num_of_pers]
working_start = 9  # время начала работы по умолчанию
working_finish = 18  # время окончания работы по умолчанию
work_hours = ["09", "10", "11", "12", "13", "14", "15", "16", "17"]  # рабочие часы по умолчанию
works_minutes = ["00", "10", "20", "30", "40", "50"]  # шаг планирования по умолчанию
plan_step = ["05", "10", "15", "20", "30"]  # справочник шага планирования
text_meet = "Выберите дату-время\nначала и окончания встречи,\nукажите количество участников"  # базовый текст окна


# сохраняет данные планируемой встречи
def plan_this_meet():
    maked_plan = check_end_view_meet_date()
    text_meet_lb2 = ""
    all_meetings_list
    if maked_plan:
        all_meetings_list.append([meet_start, meet_end, persons_of_meeting])

        for i in range(len(all_meetings_list)):
            start_date = all_meetings_list[i][0]
            start_date_str = start_date.strftime("%m-%d-%Y %H:%M")
            end_date = all_meetings_list[i][1]
            end_date_str = end_date.strftime("%m-%d-%Y %H:%M")
            pers= f"{all_meetings_list[i][2]}"
            text_meet_lb2 += f"  {i+1}\t{start_date_str}\t\t{end_date_str}\t\t{pers}\n"

        print(all_meetings_list)
        lbl2_f3.configure(anchor="nw", text=text_meet_lb2)
        text_meet_lb = "Данные о встрече\nвнесены в базу данных"
        lb_text_meet.set(text_meet_lb)

    else:
        text_meet_lb = "эту встречу запланировать невозможно\n\n проверьте параметры"
        lb_text_meet.set(text_meet_lb)


# Выводит данные в окно с описанием параметров планируемой встречи
def check_end_view_meet_date():
    """Выводим время встречи в окно и проверяем полученные от пользователя данные"""
    global persons_of_meeting
    global meet_end
    global meet_start
    global delta_meets_minutes, delta_meets_hour
    maked_plan = False
    text_meet_lb = ""

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

    if meet_start != False and meet_end != False:
        # проверяем длительность встречи
        if meet_start >= date_now:
            if meet_end >= date_now:
                if meet_start <= meet_end:
                    delta_meets = meet_end - meet_start
                    all_delta_meets_minutes = int(delta_meets.seconds / 60)
                    # print(all_delta_meets_minutes)
                        
                    if all_delta_meets_minutes > 1: 
                        # проверяем есть ли часы в минутах
                        if all_delta_meets_minutes > 59:
                            delta_meets_hour = int(all_delta_meets_minutes / 60)
                            delta_meets_minutes = delta_meets_minutes % 60
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
                                maked_plan = True
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

    return maked_plan


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
    # print(work_hours)

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
    # print(works_minutes)

    # global num_of_room
    global properties_of_meeting_rooms
    global list_room
    work_start = 9  #
    work_finish = 18  #

    nr = entry_pers_f5.get()
    if nr != "":
        if int(nr) > 0:
            num_of_room = int(nr)
        if num_of_room > 12:
            num_of_room = 12
        properties_of_meeting_rooms = []
        list_room = []
        for room in range(num_of_room):
            one_room_prop = []
            room_volume = 0
            room_prop1 = "no"
            room_prop2 = "no"
            first_time = time(work_start, 0, 0)
            second_time = time(work_finish, 0, 0)
            one_room_prop.append(first_time)
            one_room_prop.append(second_time)
            one_room_prop.append(room_volume)
            one_room_prop.append(room_prop1)
            one_room_prop.append(room_prop2)
            properties_of_meeting_rooms.append(one_room_prop)
            list_room.append(str(room + 1)) # создаем новый список комнат
            reload_meeting_table(create_table_meets_as_text())
        cb1_f2_meetroom_number.configure(values=list_room)  # загружаем новый список в чекбокс f2
        # print(properties_of_meeting_rooms)


def create_table_meets_as_text():
    text = "Комната\t\tЧеловек\t\tОпция1\t\tОпция2\n"
    for num_room in range(len(properties_of_meeting_rooms)):
        text += f" {num_room + 1}\t\t{properties_of_meeting_rooms[num_room][2]}\t\t{properties_of_meeting_rooms[num_room][3]}\t\t{properties_of_meeting_rooms[num_room][4]}\n"
    # print(text)
    return text


def reload_meeting_table(text):
    lbl2_f2.configure(text=text, anchor="nw")


def edit_meeting_table():
    number_room = int(cb1_f2_meetroom_number.get())
    new_room_volume = int(e1_f2_volume_of_meetingroom.get())
    properties_of_meeting_rooms[number_room - 1][2] = new_room_volume
    reload_meeting_table(create_table_meets_as_text())

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
notebook.add(frame1, text=" Планирование ")
notebook.add(frame2, text=" Переговорки ")
notebook.add(frame3, text=" Встречи ")
notebook.add(frame4, text=" Отчет ")
notebook.add(frame5, text=" Настройки ")
notebook.add(frame6, text=" О программе ")

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

btn = Button(frame1, text="Проверить", command=check_end_view_meet_date)
btn.place(x=20, y=290, width=255, height=25)

btn = Button(frame1, text="Запланировать", command=plan_this_meet)
btn.place(x=285, y=290, width=255, height=25)

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

btn1_f2 = Button(frame2, text="Изменить", command=edit_meeting_table)
btn1_f2.place(x=430, y=59, width=60, height=25)

lbl2_f2 = Label(frame2, text=create_table_meets_as_text(), anchor="nw", background="#FFFFFF")
lbl2_f2.place(x=20, y=100, height=220, width=340)

"""Закладка №3. Встречи"""
lbl2_f3 = Label(frame3, text="Дата", anchor="w")
lbl2_f3.place(x=20, y=15, height=25, width=80)

cb3_f3_year = Combobox(frame3, values=list_room, state="readonly")
cb3_f3_year.place(x=60, y=15, height=25, width=70)

cb3_f3_year = Combobox(frame3, values=list_room, state="readonly")
cb3_f3_year.place(x=140, y=15, height=25, width=70)

cb3_f3_year = Combobox(frame3, values=list_room, state="readonly")
cb3_f3_year.place(x=220, y=15, height=25, width=70)

lbl3_f3_text = "  #                    начало                              окончание                     кол-во"
lbl3_f3 = Label(frame3, text=lbl3_f3_text, anchor="w")
lbl3_f3.place(x=20, y=45, height=25, width=380)

lbl2_f3 = Label(frame3, text="нет встреч", anchor="center", background="#FFFFFF")
lbl2_f3.place(x=20, y=70, height=250, width=380)

"""Закладка №4. Отчет"""

"""Закладка №5. Настройки"""
lb1_f5 = Label(frame5, text="Установите диапазон планирования рабочего времени:", anchor="w")
lb1_f5.place(x=10, y=10, height=25, width=510)
lb2_f5 = Label(frame5, text="c", anchor="w")
lb2_f5.place(x=10, y=35, height=25, width=510)
lb3_f5 = Label(frame5, text="по", anchor="w")
lb3_f5.place(x=120, y=35, height=25, width=510)

cb1_f5_start_work_hour = Combobox(frame5, values=all_hours, state="readonly")
cb1_f5_start_work_hour.place(x=30, y=35, height=25, width=60, )
cb2_f5_finish_work_hour = Combobox(frame5, values=all_hours, state="readonly")
cb2_f5_finish_work_hour.place(x=150, y=35, height=25, width=60)

lb4_f5 = Label(frame5, text="Установите шаг планирования времени:", anchor="w")
lb4_f5.place(x=10, y=80, height=25, width=510)
lb5_f5 = Label(frame5, text="минут", anchor="w")
lb5_f5.place(x=100, y=105, height=25, width=510)

cb3_f5_step_work_minutes = Combobox(frame5, values=plan_step, state="readonly")
cb3_f5_step_work_minutes.place(x=30, y=105, height=25, width=60)

lb6_f5 = Label(frame5, text="Установите количество доступных переговорных комнат:", anchor="w")
lb6_f5.place(x=10, y=150, height=25, width=510)
entry_pers_f5 = ttk.Entry(frame5)
entry_pers_f5.place(x=30, y=175, height=25, width=60)
lb7_f5 = Label(frame5, text="комнат (max. 12)", anchor="w")
lb7_f5.place(x=100, y=175, height=25, width=510)
lb8_f5 = Label(frame5, foreground="red", text="Внимание! После сохранения новых параметров\n текущие настройки программы изменятся",
               anchor="w")
lb8_f5.place(x=10, y=210, height=60, width=510)

btn1_f5 = Button(frame5, text="Cохранить", command=get_and_save_program_settings)
btn1_f5.place(x=370, y=270, width=150, height=25)

"""Закладка №6. О программе"""
about_prog = "Данная программа разработана для облегчения процесса\nпланирования загрузки переговорных комнат" \
             "\n\nver 1.0\n\n\nАвтор: Алексей Фролов\n\n\n e-mail: frolovhome@yandex.ru"
lb_f6 = Label(frame6, text=about_prog, anchor="center")
lb_f6.place(x=10, y=10, height=320, width=510)


wnd.mainloop()
