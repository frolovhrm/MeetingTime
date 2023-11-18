"""
meetings_time - список встреч - [[начало, окончание, челвек], ]
meetingrooms_volume - размер переговорки {номер: места, }


"""

def makeDay(worktime):
    """создает список из рабочего дня"""
    work_day = []
    for time in range(worktime[0], worktime[1] + 1):
        work_day += [time]
    return work_day

def makeMeetLineTime(s, f):
    """ создает список часов из времени встречи """
    line_time = []
    for time in range(s, f):
        line_time += [time]
    return line_time

def make_plan(meetings_time, meetingrooms_volume):
    """распределяет встречи по доступным переговоркам"""
    meetings_time = meetings_time   # список всех запланированный встреч
    meetingrooms_volume = meetingrooms_volume   # количество мест в переговорках
    list_meets = {} # справочник всех распределенных встреч в переговорках
    list_time_one_meet = []  # список часов одной встречи
    number_room = 0 # номер переговорки
    meetings_list_all_day = [[]]    # это список встреч для всех переговорках, создаем первую встречу

    for meeting in range(len(meetings_time)):  # ищем место для каждой встречи
        added = False  # маркер, если встреча не добавлена в переговорку
        for room in range(len(meetings_list_all_day)):  # проверяем все открытые переговорки
            print(f"\nВстреча - {meeting + 1} переговорка - {room + 1}")
            list_time_one_meet = makeMeetLineTime(meetings_time[meeting][0],
                                                meetings_time[meeting][1])  # список времени каждой встречи
            numPersOneMeet = meetings_time[meeting][2]
            number_room = room

            # если персон больше чем мест в переговорке
            
            try:
                if numPersOneMeet > meetingrooms_volume[room + 1]:
                    print(f"переговорка {room + 1} для встречи {meeting + 1} маленькая, дальше")
                    added = False
                    continue
            except KeyError:
                print(
                f"Свободные переговорки закончились. Для встречи {meeting + 1} нет места, выберите другое время или "
                f"уменьшите количество участников\n")
                continue


            # если пересечений в этой переговорке нет, добавляем в неё встречу 
            if set(list_time_one_meet).isdisjoint(set(meetings_list_all_day[room])):
                print(f"переговорка {room + 1} для встречи {meeting + 1} по времени подошла")
                for i in list_time_one_meet:
                    meetings_list_all_day[room].append(i)
                meetings_list_all_day[room].sort()

                list_meets[meeting + 1] = room + 1  # добавляем в библиотеку всех встреч {номер встречи:номер переговорки}
                added = True
                break
            else:
                print(f"переговорка  {room + 1} для встречи {meeting + 1} по времени не подошла")
                added = False
                continue

        if len(meetings_list_all_day) > len(meetingrooms_volume):  # если переговорки кончились, встречу пропускаем
            print(
                f"Свободные переговорки закончились. Для встречи {meeting + 1} нет места, выберите другое время или "
                f"уменьшите количество участников\n")
            continue

        if not added:  # если места нет в открытых переговорках, то открываем еще одну
            print(f"встречу {meeting + 1} помещаем в слудущую переговорку {room + 2}")
            meetings_list_all_day.append(list_time_one_meet)
            list_meets[meeting + 1] = number_room + 2  # добавляем в номер встречи номер переговорки
        print(f"переговорка {room + 1} просмотрена")
    
    return list_meets

def printCheck(dict_meet, meet_times):
    """Печатаем отчет о всех встречах"""
    print("\nВстреча\t   Время\tПереговорка\tУчастников")
    for key, value in dict_meet.items():
        print(
            f"{key: ^7}\t   {meet_times[key - 1][0]:0>2}-{meet_times[key - 1][1]:0>2}\t{value: ^11}\t    {meetings_time[key - 1][2]:>2}")

# номер и максимальное количество людей в переговорке
meetingrooms_volume = {1: 12, 2: 15, 3: 6, 4: 12, 5: 20, 6: 6, 7: 12}  

# запланированные встречи [начало, окончание, люди]
meetings_time = [[10, 15, 13], [9, 11, 8], [16, 18, 4], [9, 11, 8], [16, 18, 4], [9, 11, 8], [9, 11, 8], [16, 18, 4], [9, 11, 8], [16, 18, 4], [9, 11, 8], [16, 18, 4], [9, 11, 12], [16, 18, 4], [9, 11, 8], [16, 18, 4], [9, 11, 8], [16, 18, 4]]  

print(f"всего встреч - {len(meetings_time)}")
# print(f"\nСписок встреч [начало, окончание, кол-во чел.] - {meetings_time}")
# print(f"Доступно переговорных комнат {len(meetingrooms_volume)} - (номер: кол-во мест)\n{meetingrooms_volume}")

list_meets = make_plan(meetings_time, meetingrooms_volume)

printCheck(list_meets, meetings_time)
print("")
