from database.db_administrator import get_connection
from models.student import get_student_by_id
from models.discipline import get_discipline_by_id

class Attendance:
    """
    Модель посещаемости студента по дисциплине.
    Атрибуты:
        id            - уникальный идентификатор
        student_id    - ID студента
        discipline_id - ID дисциплины
        date          - дата занятия (строка в формате ГГГГ-ММ-ДД)
        status        - статус посещения: 'present', 'absent', 'late'
    """
    def __init__(self, id=None, student_id=None, discipline_id=None, date=None, status=None):
        self.id = id
        self.student_id = student_id
        self.discipline_id = discipline_id
        self.date = date
        self.status = status

    def save(self):
        """Сохраняет запись о посещаемости (добавление или обновление)."""
        if not self.student_id or not self.discipline_id or not self.date or not self.status:
            raise ValueError("student_id, discipline_id, date и status обязательны")
        if self.status not in ('present', 'absent', 'late'):
            raise ValueError("status должен быть 'present', 'absent' или 'late'")
        # Проверка существования студента и дисциплины
        if not get_student_by_id(self.student_id):
            raise ValueError(f"Студент с ID {self.student_id} не существует")
        if not get_discipline_by_id(self.discipline_id):
            raise ValueError(f"Дисциплина с ID {self.discipline_id} не существует")

        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute('''
                INSERT INTO attendance (student_id, discipline_id, date, status)
                VALUES (?, ?, ?, ?)
            ''', (self.student_id, self.discipline_id, self.date, self.status))
            self.id = cursor.lastrowid
        else:
            cursor.execute('''
                UPDATE attendance
                SET student_id = ?, discipline_id = ?, date = ?, status = ?
                WHERE id = ?
            ''', (self.student_id, self.discipline_id, self.date, self.status, self.id))
        conn.commit()
        conn.close()

    def delete(self):
        """Удаляет запись о посещаемости."""
        if self.id is not None:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM attendance WHERE id = ?", (self.id,))
            conn.commit()
            conn.close()

def get_all_attendance():
    """Возвращает список всех записей посещаемости."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, student_id, discipline_id, date, status
        FROM attendance
        ORDER BY date DESC, student_id
    ''')
    rows = cursor.fetchall()
    conn.close()
    return [Attendance(id=row[0], student_id=row[1], discipline_id=row[2],
                       date=row[3], status=row[4]) for row in rows]

def get_attendance_by_id(attendance_id):
    """Возвращает запись посещаемости по ID или None."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, student_id, discipline_id, date, status
        FROM attendance WHERE id = ?
    ''', (attendance_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Attendance(id=row[0], student_id=row[1], discipline_id=row[2],
                          date=row[3], status=row[4])
    return None

def get_attendance_by_student(student_id):
    """Возвращает список записей посещаемости для конкретного студента."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, student_id, discipline_id, date, status
        FROM attendance WHERE student_id = ?
        ORDER BY date DESC
    ''', (student_id,))
    rows = cursor.fetchall()
    conn.close()
    return [Attendance(id=row[0], student_id=row[1], discipline_id=row[2],
                       date=row[3], status=row[4]) for row in rows]

def get_attendance_by_discipline(discipline_id):
    """Возвращает список записей посещаемости для конкретной дисциплины."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, student_id, discipline_id, date, status
        FROM attendance WHERE discipline_id = ?
        ORDER BY date DESC
    ''', (discipline_id,))
    rows = cursor.fetchall()
    conn.close()
    return [Attendance(id=row[0], student_id=row[1], discipline_id=row[2],
                       date=row[3], status=row[4]) for row in rows]

def get_attendance_by_student_and_discipline(student_id, discipline_id):
    """Возвращает все записи посещаемости студента по конкретной дисциплине."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, student_id, discipline_id, date, status
        FROM attendance
        WHERE student_id = ? AND discipline_id = ?
        ORDER BY date
    ''', (student_id, discipline_id))
    rows = cursor.fetchall()
    conn.close()
    return [Attendance(id=row[0], student_id=row[1], discipline_id=row[2],
                       date=row[3], status=row[4]) for row in rows]

def get_attendance_summary(student_id, discipline_id=None):
    """
    Возвращает словарь со статистикой посещаемости студента.
    Если discipline_id указана – только по ней, иначе по всем дисциплинам.
    """
    conn = get_connection()
    cursor = conn.cursor()
    if discipline_id:
        cursor.execute('''
            SELECT status, COUNT(*) FROM attendance
            WHERE student_id = ? AND discipline_id = ?
            GROUP BY status
        ''', (student_id, discipline_id))
    else:
        cursor.execute('''
            SELECT status, COUNT(*) FROM attendance
            WHERE student_id = ?
            GROUP BY status
        ''', (student_id,))
    rows = cursor.fetchall()
    conn.close()
    summary = {'present': 0, 'absent': 0, 'late': 0}
    for status, count in rows:
        summary[status] = count
    total = sum(summary.values())
    summary['total'] = total
    if total > 0:
        summary['present_percent'] = round(summary['present'] / total * 100, 2)
    else:
        summary['present_percent'] = 0.0
    return summary