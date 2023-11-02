"""
Считаем количество переговорок.
На входе список со временем начала и окончание встреч, количество персон, количество переговорок, и их размер.
"""

# print("\033c", end="")

work_time = [9, 17]  # рабочее время
meetingrooms_volume = {1: 12, 2: 15, 3: 6, 4: 12, 5: 20, 6: 6,
                       7: 12}  # номер и максимальное количество людей в переговорке
meetings_time = [[10, 15, 13], [9, 11, 8], [16, 18, 4]]  # запланированные встречи [начало, окончание, люди]
# meetings_time +=[[15, 18, 6], [10, 15, 2], [9, 11, 5], [15, 18, 6], [10, 15, 18], [9, 11, 5], [15, 18, 6], [10, 15,
# 2], [11, 13, 5]]   # дополнительные данные для тестирования

list_meets = {}
number_room = 0
all_work_time = []  # список всех рабочих часов
list_time_one_meet = []    # список часов одной встречи


def makeDay(worktime):
    """создает список из рабочего дня"""
    work_day = []
    for time in range(worktime[0], worktime[1] + 1):
        work_day += [time]
    return work_day


def makeMeetLineTime(s, f):
    """ создает список из времени встречи """
    line_time = []
    for time in range(s, f):
        line_time += [time]
    return line_time

def printCheck(dict_meet, meet_times):
    """Печатаем отчет о всех встречах"""
    print("\nВстреча\t   Время\tПереговорка\tУчастников")
    for key, value in dict_meet.items():
        print(
            f"{key: ^7}\t   {meet_times[key - 1][0]:0>2}-{meet_times[key - 1][1]:0>2}\t{value: ^11}\t    {meetings_time[key - 1][2]:>2}")


print(f"Список встреч [начало, окончание, кол-во чел.]\n{meetings_time}\n")
print(f"Количество встреч\n{len(meetings_time)}\n")
print(f"Свободно переговорных комнат\n{len(meetingrooms_volume)}\n")
print(f"Переговорки : max. персон\n{meetingrooms_volume}\n")

# это список встреч для всех переговорках, создаем первую встречу
meetings_list_all_day = [[]]

for meeting in range(len(meetings_time)):  # ищем место для каждой встречи
    added = False   # маркер, если встреча не добавлена в переговорку
    for room in range(len(meetings_list_all_day)):  # проверяем все открытые переговорки
        list_time_one_meet = makeMeetLineTime(meetings_time[meeting][0],
                                              meetings_time[meeting][1])  # список времени каждой встречи
        numPersOneMeet = meetings_time[meeting][2]
        number_room = room

        # если персон больше чем мест в переговорке
        if numPersOneMeet > meetingrooms_volume[room + 1]:
            added = False
            continue

        # если пересечений в этой переговорке нет, добавляем в неё встречу 
        if set(list_time_one_meet).isdisjoint(set(meetings_list_all_day[room])):
            for i in list_time_one_meet:
                meetings_list_all_day[room].append(i)
            meetings_list_all_day[room].sort()

            list_meets[meeting + 1] = room + 1  # добавляем в библиотеку всех встреч {номер встречи:номер переговорки}
            added = True
            break
        else:
            added = False
            continue

    if len(meetings_list_all_day) > len(meetingrooms_volume):  # если переговорки кончились, встречу пропускаем
        print(
            f"Свободные переговорки закончились. Для встречи {meeting + 1} нет места, выберите другое время или "
            f"уменьшите количество участников\n")
        continue

    if not added:  # если места нет в открытых переговорках, то открываем еще одну
        meetings_list_all_day.append(list_time_one_meet)
        list_meets[meeting + 1] = number_room + 2  # добавляем в номер встречи номер переговорки

printCheck(list_meets, meetings_time)
print("")
