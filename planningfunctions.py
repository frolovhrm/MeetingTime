# from meetingtime import *
import sqlite3 as sq

properties_of_all_meeting_rooms = [[5, "no", "no"], [10, "no", "no"], [20, "no", "no"], [20, "no", "no"]]  # список всех переговорок с параметрами [начало работы, конец, кол-во мест]
plans_all_miteeng_rooms = []
base_name = "meetingtime.db"


def get_meeting_list_on_this_date():
    date_meet = "'2023-12-05'"
    with sq.connect(base_name) as con:
        cursor = con.cursor()
        text = f"SELECT * FROM Meetings WHERE datemeet = {date_meet}"
        cursor.execute(text)
        list_meet_one_date = cursor.fetchall()
    return list_meet_one_date


def make_meeting_as_planed():

    pass


def make_meeting_as_unplaned():

    pass


def make_plans_for_all_miteeng_rooms():
    for i in range(len(properties_of_all_meeting_rooms)):
        plans_all_miteeng_rooms.append([])


def planing_room_all_day():
    list_meet_one_date = get_meeting_list_on_this_date() # получаем список всех встреч из базы
    for meet in range(len(list_meet_one_date)): # начинаем искать место для каждой встречи
        if list_meet_one_date[meet][6] == 1: # если встреча отмечена как запланированная, пропускаем.
            break

        meet_planed = 0
        meet_start = list_meet_one_date[meet][1] # время начала встречи
        meet_end = list_meet_one_date[meet][2] # время окончания встречи
        meet_pers = int(list_meet_one_date[meet][3]) # кол-во участников встречи
        
        for room in range(len(properties_of_all_meeting_rooms)): # ищем в каждой переговорке
            volume = properties_of_all_meeting_rooms[room][0]   # кол-во мест в комнате
            if meet_pers <= volume:   # если мест хватает
                this_room_meeting_list = plans_all_miteeng_rooms[room] # получаем план встреч конкретной переговорки
                cros = False # пересечений нет 
                if this_room_meeting_list:  # если план не пустой
                    cros = False
                    for i in range(len(this_room_meeting_list)):  # проверяем его на пересечения
                        print(f"проверяем переговорку {room} ее встречи {this_room_meeting_list[i]}")
                        if meet_start >= this_room_meeting_list[i][0] and meet_start < this_room_meeting_list[i][1]:
                            print(f"{i} есть пересечение по старту {meet_start} <= {this_room_meeting_list[i][0]} или {meet_start} > {this_room_meeting_list[i][1]}")
                            cros = True
                        if meet_end <= this_room_meeting_list[i][0]  and meet_end > this_room_meeting_list[i][1]:
                            print(f"{i} есть пересечение по финишу {meet_end} => {this_room_meeting_list[i][0]} или {meet_end} < {this_room_meeting_list[i][1]}")
                            cros = True
                else:
                    print(f"В переговорке {room} еще нет встреч. ", end="")    
                if cros == False: # если пересечений ненашлось добавляем встречу в план комнаты
                    print(f"Встречу № {meet} на {meet_pers} чел. проводим в комнате № {room} from {meet_start} to {meet_end}")
                    plans_all_miteeng_rooms[room].append([meet_start, meet_end, meet_pers])
                    meet_planed = 1  # встреча запланирована
                    break
            else:   # если мест не хватает
                print(f"Встречу № {meet} на {meet_pers} чел. в комнате № {room} сделать не можем, мало мест")


        if meet_planed == 0:   # если комнат свободных больше нет и встреча не запланированна  
            print(f"Встречу № {meet} на {meet_pers} незапланирована, нет мест!!!")

    # print(plans_all_miteeng_rooms)
    return plans_all_miteeng_rooms


def print_meetings_plan_on_date(list_meetings):
    for room in range(len(list_meetings)):
        for meeting in range(len(list_meetings[room])):
            print(f"Комната {room} встреча {meeting} с {list_meetings[room][meeting][0]}  по {list_meetings[room][meeting][1]} на {list_meetings[room][meeting][2]} человек")



make_plans_for_all_miteeng_rooms()

print_meetings_plan_on_date(planing_room_all_day())
   
if __name__ == '__main__':
    planing_room_all_day()    
