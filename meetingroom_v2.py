"""Считаем колличество переговорок.
На входе список со временем начала и окончание встречь.
"""

print("\033c", end="")

work_time = [9, 17]  # рабочее время
meetingrooms_and_pers = {1:12, 2:15, 3:6, 4:12, 5:20, 6:6, 7:12}    # номер и максимальное количество людей в переговорке
meetings_time = [[10, 15, 13], [9, 11, 8], [16, 18, 4]]  # запланированные встречи [начало, окончание, люди]
meetings_time +=[[15, 18, 6], [10, 15, 2], [9, 11, 5], [15, 18, 6], [10, 15, 2], [9, 11, 5], [15, 18, 6], [10, 15, 2], [11, 13, 5]]
added = True
list_meets = {}
number_room = 0
all_work_time = []  # список всех рабочих часов


"""создает список из рабочего дня"""
def makeDay(work_time):
    work_day = []
    for i in range(work_time[0], work_time[1] + 1):
        work_day += [(i)]
    return work_day

""" создает список из времени встречи """
def makeMeetLineTime(s, f):
    lineTime = []
    for i in range(s, f):
        lineTime += [i]
    return lineTime

"""печатаем отчет о всех встечах"""
def printCheck(dict_meet, meet_times):
    print("\nВстреча\t   Время\tПереговорка\tУчастников")
    for key, value in dict_meet.items():
        print(f"{key: ^7}\t   {meet_times[key - 1][0]:>2}-{meet_times[key - 1][1]:>2}\t{value: ^11}\t    {meetings_time[key - 1][2]:>2}")


print(f"Список встреч [начало, окончание, кол-во чел.] - {meetings_time} \n")
print(f"Количество встреч - {len(meetings_time)}\n")
print(f"Свободно переговорных комнат - {len(meetingrooms_and_pers)}\n")
print(f"Переговорки: max. персон - {meetingrooms_and_pers}\n")

# это списоок встреч для всех переговорках, создаем первую встречу
meetings_list_all_day = [[]]


for meeting in range(len(meetings_time)):    # ищем место для каждой встречи
    for room in range(len(meetings_list_all_day)):   # проверяем все переговорки
        listTimeOneMeet = makeMeetLineTime(meetings_time[meeting][0], meetings_time[meeting][1]) # спосок времени каждой встречи
        numPersOneMeet = meetings_time[meeting][2]
        # print(f"встреча {meeting + 1} переговорка {room + 1} время встречи {listTimeOneMeet} кол-во гостей {numPersOneMeet}")
        number_room = room

        if numPersOneMeet > meetingrooms_and_pers[room+1]:
            # print(f'не поместились в {room + 1}-ю ', end='')
            added = False
            continue
        
        # если пересечений в этой переговорке нет, добавляем сюда встречу 
        if set(listTimeOneMeet).isdisjoint(set(meetings_list_all_day[room])):
            for i in listTimeOneMeet:
                meetings_list_all_day[room].append(i)
            meetings_list_all_day[room].sort()
            # print(f"добавили встречу {meeting + 1} в переговорку {room + 1}, теперь {meetings_list_all_day}")
            
            list_meets[meeting +1] = room + 1 # добавляем в номер встречи номер переговорки
            added = True
            break
        else:
            added = False
            # print(f"переговорка {room + 1} время {listTimeOneMeet} занято, смотрим дальше\n")
            continue

    if len(meetings_list_all_day)+1 > len(meetingrooms_and_pers):
        # print(f"Свободные переговорки закончились. Для встречи {meeting + 1} нет места, выбирите другое время и ли уменьшите количество участников\n")
        continue

    if added == False:  # если места нет в открытых переговорках, то открываем еще одну
        meetings_list_all_day.append(listTimeOneMeet)
        # print(f"и открыли еще одну переговорку № {room + 2} и встреча теперь там {meetings_list_all_day}")
        list_meets[meeting + 1] = number_room + 2  # добавляем в номер встречи номер переговорки

    # print(list_meets)
    # print()

# print(f"Всего потребуется переговорок - {len(meeting_day)}\n")

# print(meetings_time)
# print(list_meets)
# print(meetings_list_all_day)
printCheck(list_meets, meetings_time)
print("")

for time in range(work_time[0], work_time[1]+1):
    all_work_time += [time]

for t in range(len(all_work_time)):
    print(f"{all_work_time[t]}\t", end='')

for m in range(len(meetings_list_all_day)):
    if m == 0:
        print(f"\n{meetings_list_all_day[m]}")
    print(f"{meetings_list_all_day[m]}")
