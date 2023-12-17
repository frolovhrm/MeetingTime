# list_room = [1, 2] # список номеров комнат
properties_of_meeting_rooms = [[50, "no", "no"], [50, "no", "no"]]  # список всех переговорок с параметрами [кол-во мест, свойство1, свойстово2]
# working_start = 9  # время начала работы
# working_finish = 18  # время окончания работы
work_hours = ["09", "10", "11", "12", "13", "14", "15", "16", "17"]  # рабочие часы
works_minutes = ["00", "10", "20", "30", "40", "50"]  # шаг планирования
# date_meet = f"'{DATE_NOW.date()}'"
# plans_all_miteeng_rooms = []
# list_table_item = []



def count_room(properties_of_meeting_rooms):
    list_room = []
    for i in range(len(properties_of_meeting_rooms)):
        list_room.append(i + 1)
    # print(list_room)
    return list_room


def load_program_settings():
    list_arg = []
    with open('settings.txt', 'r') as file:
        for line in file:
            a = line.rstrip()
            # print(a)
            list_arg.append(a)
            # print(list_arg)
    #         list_arg.append(line.rstrip())
    return list_arg[0], list_arg[1], list_arg[2]




def seve_program_settings(work_hours, works_minutes, properties_of_meeting_rooms):
    # print("save GO")
    list_arg = [str(work_hours), str(works_minutes), str(properties_of_meeting_rooms)]

    with open('settings.txt', 'w') as file:
        for st in list_arg:
            file.write(st + "\n")
            # print("save OK")


seve_program_settings(work_hours, works_minutes, properties_of_meeting_rooms)
work_hours, works_minutes, properties_of_meeting_rooms = load_program_settings()
work_hours = work_hours.strip('][').split(', ')
works_minutes = works_minutes.strip('][').split(', ')
properties_of_meeting_rooms = properties_of_meeting_rooms.strip('][').split(', ')
print((work_hours))
print((works_minutes))
print(properties_of_meeting_rooms)

# load_program_settings()