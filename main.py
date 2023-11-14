from tkinter import *
from tkcalendar import Calendar
from tkinter.ttk import Combobox
import datetime

def printdate():
    """Выводим время вмтречи в окно"""
    if cb_start_hour.get() and cb_start_minute.get():
        caldate = cal.get_date() + " " + cb_start_hour.get() + ":" + cb_start_minute.get()
        meetstart = datetime.datetime.strptime(caldate, '%m/%d/%y %H:%M')
    else:
        meetstart = "0000-00-00 00:00"
        print("нет времени начала")

    if cb_end_hour.get() and cb_end_minute.get():
        caldate = cal.get_date() + " " + cb_end_hour.get() + ":" + cb_end_minute.get()
        meetend = datetime.datetime.strptime(caldate, '%m/%d/%y %H:%M')
    else:
        meetend = "0000-00-00 00:00"
        print("нет времени окончания") 

    if  meetstart < meetend:
        delta = meetend - meetstart
        delda_minuts = int((delta.seconds)/60)
        text_meet = f"начало встречи \n{str(meetstart)}\n\n окончание встречи \n{str(meetend)}\n\n продолжительность {delda_minuts} минут"
    else:
        text_meet = f"проверьте время начала\n и окончания встречи"
    
    lb_text = Label(text=text_meet, anchor="center")
    lb_text.configure(relief=RAISED)
    lb_text.place(x=275, y=10, height=185, width=255)



wnd = Tk()
wnd.title("MeetingTime")
wnd.geometry("540x330")
wnd.resizable(False, False)
text_meet = "XXXX-XX-XX XX:XX - XXXX-XX-XX XX:XX"

work_hours = ["09", "10", "11", "12", "13", "14", "15", "16", "17"]
works_minuts = ["00", "10", "20", "30", "40", "50"]

this_day = datetime.datetime.now()
cal = Calendar(wnd, selectmode='day', year=this_day.year, month=this_day.month, day=this_day.day)
cal.place(x=10, y=10)

lb1_start_hour = Label(text="Начало встречи",  anchor="center")
lb1_start_hour.place(x=10, y=210, height=20, width=120)

lb1_end_hour = Label(text="Окончание встречи", anchor="center")
lb1_end_hour.place(x=130, y=210, height=20, width=150)

lb2_start_hour = Label(text="час.",  anchor="center")
lb2_start_hour.place(x=10, y=255, height=20, width=60)
lb2_start_hour = Label(text="мин.", anchor="center")
lb2_start_hour.place(x=70, y=255, height=20, width=60)

lb2_end_hour = Label(text="час.",  anchor="center")
lb2_end_hour.place(x=10+140, y=255, height=20, width=60)
lb2_end_hour = Label(text="мин.", anchor="center")
lb2_end_hour.place(x=70+140, y=255, height=20, width=60)

lb_text = Label(text=text_meet, anchor="center")
lb_text.configure(relief=RAISED)
lb_text.place(x=275, y=10, height=185, width=255)

cb_start_hour = Combobox(values=work_hours, state="readonly")
cb_start_hour.place(x=10, y=230, height=25, width=60,)
cb_start_minute = Combobox(values=works_minuts, state="readonly")
cb_start_minute.place(x=70, y=230, height=25, width=60)

cb_end_hour = Combobox(values=work_hours, state="readonly")
cb_end_hour.place(x=145, y=230, height=25, width=60)
cb_end_minute = Combobox(values=works_minuts, state="readonly")
cb_end_minute.place(x=205, y=230, height=25, width=60)



btn = Button(wnd, text="Выбрать", command=printdate)
btn.place(x=10, y=280, width=255, height=25)

btn = Button(wnd, text="Запланировать", command=wnd.destroy)
btn.place(x=275, y=280, width=255, height=25)


print(cal.get_date())


wnd.mainloop()



