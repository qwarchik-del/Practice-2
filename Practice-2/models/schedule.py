import sqlite3
from config import DB_NAME

class Schedule:
    """Модель расписания (одна запись)."""
    def __init__(self, id=None, group_id=None, discipline_id=None,
                 teacher_id=None, day_of_week=None, lesson_number=None):
        self.id = id
        self.group_id = group_id
        self.discipline_id = discipline_id
        self.teacher_id = teacher_id
        self.day_of_week = day_of_week
        self.lesson_number = lesson_number

    def save(self):
        """Сохраняет запись (добавляет или обновляет)."""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute('''
                INSERT INTO schedule (group_id, discipline_id, teacher_id, day_of_week, lesson_number)
                VALUES (?, ?, ?, ?, ?)
            ''', (self.group_id, self.discipline_id, self.teacher_id,
                  self.day_of_week, self.lesson_number))
            self.id = cursor.lastrowid
        else:
            cursor.execute('''
                UPDATE schedule
                SET group_id = ?, discipline_id = ?, teacher_id = ?, day_of_week = ?, lesson_number = ?
                WHERE id = ?
            ''', (self.group_id, self.discipline_id, self.teacher_id,
                  self.day_of_week, self.lesson_number, self.id))
        conn.commit()
        conn.close()

    def delete(self):
        """Удаляет запись из БД."""
        if self.id is not None:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM schedule WHERE id = ?', (self.id,))
            conn.commit()
            conn.close()


def get_all_schedules():
    """Возвращает список всех записей расписания (объекты Schedule)."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, group_id, discipline_id, teacher_id, day_of_week, lesson_number
        FROM schedule
        ORDER BY id
    ''')
    rows = cursor.fetchall()
    conn.close()
    schedules = []
    for row in rows:
        schedules.append(Schedule(
            id=row[0],
            group_id=row[1],
            discipline_id=row[2],
            teacher_id=row[3],
            day_of_week=row[4],
            lesson_number=row[5]
        ))
    return schedules

def get_schedule_by_id(schedule_id):
    """Возвращает запись расписания по ID или None."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, group_id, discipline_id, teacher_id, day_of_week, lesson_number
        FROM schedule
        WHERE id = ?
    ''', (schedule_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Schedule(
            id=row[0],
            group_id=row[1],
            discipline_id=row[2],
            teacher_id=row[3],
            day_of_week=row[4],
            lesson_number=row[5]
        )
    return None
