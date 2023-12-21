import json
import sqlite3 as sq



# читаем текущие количество переговорок
def count_room(properties_of_meeting_rooms):
    list_room = []
    for i in range(len(properties_of_meeting_rooms)):
        list_room.append(i + 1)
    return list_room

# читаем настройки программы из файла
def load_program_settings():
    with open('settings.json', 'r') as file:
        json_data = json.load(file)
    return json_data[0], json_data[1], json_data[2]

# сохраняем настройки программы в файл
def seve_program_settings(work_hours, works_minutes, properties_of_meeting_rooms):
    with open('settings.json', 'w') as file:
        json.dump((work_hours, works_minutes, properties_of_meeting_rooms), file)

# находит в базе все уникальные даты в которые есть встречи
def get_all_unique_date_from_base(base_name, DATE_NOW):
    with sq.connect(base_name) as con:
        cursor = con.cursor()
        date = str(DATE_NOW.date())
        date = "'"+date+"'"
        text = f"SELECT DISTINCT datemeet FROM Meetings WHERE datemeet > {date}"
        cursor.execute(text)
        list_uniq_date = cursor.fetchall()
    return list_uniq_date

# находит в базе все будущие встречи и отменяет их планирование
def unplan_all_meetings_in_future(base_name, DATE_NOW):
    with sq.connect(base_name) as con:
        cursor = con.cursor()
        date = str(DATE_NOW.date())
        time = (DATE_NOW.time())
        time = time.strftime("%H:%M")
        date = "'"+date+"'"
        time = "'"+time+"'"
        text = f"SELECT ALL _id FROM Meetings WHERE datemeet > {date} and timestart > {time}"
        cursor.execute(text)
        list_all = cursor.fetchall()
        for num in list_all:
            text = f"UPDATE Meetings SET planned = 0 WHERE _id = {int(num[0])}"
            cursor.execute(text)
