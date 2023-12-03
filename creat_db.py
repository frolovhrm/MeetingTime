import sqlite3 as sq


def createNewBase():
    with sq.connect('meetingtime.db') as con:
        cur = con.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS Meetings (
        datestart TEXT NOT NULL,
        dateend TEXT NOT NULL,
        quantity INTEGER,
        option1 INTEGER DEFAULT 0,
        option2 INTEGER DEFAULT 0,
        planned INTEGER DEFAULT 0      
        )""")

    print('Новая база созданна')


if __name__ == '__main__':
    createNewBase()
