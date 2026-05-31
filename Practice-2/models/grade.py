from database.db_administrator import get_connection

class Grade:
    """
    Модель оценки студента по дисциплине.
    Атрибуты:
        id               - уникальный идентификатор оценки
        student_id       - идентификатор студента
        discipline_id    - идентификатор дисциплины
        grade_value      - оценка (целое число, обычно 2,3,4,5)
        date_received    - дата получения оценки (строка в формате ГГГГ-ММ-ДД)
    """
    def __init__(self, id=None, student_id=None, discipline_id=None, grade_value=None, date_received=None):
        self.id = id
        self.student_id = student_id
        self.discipline_id = discipline_id
        self.grade_value = grade_value
        self.date_received = date_received

    def save(self):
        """
        Сохраняет текущий объект оценки в базу данных.
        Если self.id == None - выполняет INSERT (добавление новой записи).
        Иначе - выполняет UPDATE для существующей записи.
        """
        conn = get_connection()
        cursor = conn.cursor()

        if self.id is None:
            cursor.execute('''
                INSERT INTO grades (student_id, discipline_id, grade_value, date_received)
                VALUES (?, ?, ?, ?)
            ''', (self.student_id, self.discipline_id, self.grade_value, self.date_received))
            self.id = cursor.lastrowid
        else:
            cursor.execute('''
                UPDATE grades
                SET student_id = ?, discipline_id = ?, grade_value = ?, date_received = ?
                WHERE id = ?
            ''', (self.student_id, self.discipline_id, self.grade_value, self.date_received, self.id))

        conn.commit()
        conn.close()

    def delete(self):
        """
        Удаляет оценку из базы данных по её id.
        """
        if self.id is not None:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM grades WHERE id = ?', (self.id,))
            conn.commit()
            conn.close()



def get_all_grades():
    """
    Возвращает список всех оценок в виде объектов Grade.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, student_id, discipline_id, grade_value, date_received FROM grades')
    rows = cursor.fetchall()
    conn.close()

    return [Grade(id=row[0], student_id=row[1], discipline_id=row[2],
                  grade_value=row[3], date_received=row[4]) for row in rows]


def get_grade_by_id(grade_id):
    """
    Возвращает оценку с указанным id, либо None, если не найдена.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, student_id, discipline_id, grade_value, date_received FROM grades WHERE id = ?', (grade_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return Grade(id=row[0], student_id=row[1], discipline_id=row[2],
                     grade_value=row[3], date_received=row[4])
    return None


def get_grades_by_student(student_id):
    """
    Возвращает список оценок, полученных конкретным студентом.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, student_id, discipline_id, grade_value, date_received
        FROM grades
        WHERE student_id = ?
        ORDER BY date_received DESC
    ''', (student_id,))
    rows = cursor.fetchall()
    conn.close()

    return [Grade(id=row[0], student_id=row[1], discipline_id=row[2],
                  grade_value=row[3], date_received=row[4]) for row in rows]


def get_grades_by_discipline(discipline_id):
    """
    Возвращает список всех оценок по определённой дисциплине.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, student_id, discipline_id, grade_value, date_received
        FROM grades
        WHERE discipline_id = ?
        ORDER BY date_received DESC
    ''', (discipline_id,))
    rows = cursor.fetchall()
    conn.close()

    return [Grade(id=row[0], student_id=row[1], discipline_id=row[2],
                  grade_value=row[3], date_received=row[4]) for row in rows]


def get_average_grade_for_student(student_id):
    """
    Возвращает средний балл студента по всем оценкам (число с плавающей точкой),
    либо None, если оценок нет.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT AVG(grade_value)
        FROM grades
        WHERE student_id = ?
    ''', (student_id,))
    avg = cursor.fetchone()[0]
    conn.close()
    return round(avg, 2) if avg is not None else None