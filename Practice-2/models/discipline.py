from database.db_administrator import get_connection
from models.teacher import get_teacher_by_id  

class Discipline:
    """
    Модель дисциплины (учебного предмета)
    Атрибуты:
        id            - уникальный идентификатор
        name          - название дисциплины (например, "Математика")
        teacher_id    - идентификатор преподавателя, ведущего дисциплину
    """
    def __init__(self, id=None, name=None, teacher_id=None):
        self.id = id
        self.name = name
        self.teacher_id = teacher_id

    def save(self):
        """Сохраняет дисциплину: добавляет новую или обновляет существующую"""
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            # Новая запись
            cursor.execute(
                "INSERT INTO disciplines (name, teacher_id) VALUES (?, ?)",
                (self.name, self.teacher_id)
            )
            self.id = cursor.lastrowid
        else:
            # Обновление существующей
            cursor.execute(
                "UPDATE disciplines SET name = ?, teacher_id = ? WHERE id = ?",
                (self.name, self.teacher_id, self.id)
            )
        conn.commit()
        conn.close()

    def delete(self):
        """Удаляет дисциплину из базы данных по её id"""
        if self.id is not None:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM disciplines WHERE id = ?", (self.id,))
            conn.commit()
            conn.close()

    def get_teacher(self):
        """Возвращает объект Teacher, который ведёт данную дисциплину, или None"""
        if self.teacher_id:
            return get_teacher_by_id(self.teacher_id)
        return None


def get_all_disciplines():
    """Возвращает список всех дисциплин в виде объектов Discipline"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, teacher_id FROM disciplines")
    rows = cursor.fetchall()
    conn.close()
    return [Discipline(id=row[0], name=row[1], teacher_id=row[2]) for row in rows]

def get_discipline_by_id(discipline_id):
    """Возвращает дисциплину по её ID или None, если не найдена"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, teacher_id FROM disciplines WHERE id = ?", (discipline_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Discipline(id=row[0], name=row[1], teacher_id=row[2])
    return None

def get_disciplines_by_teacher(teacher_id):
    """Возвращает список дисциплин, которые ведёт преподаватель с указанным ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, teacher_id FROM disciplines WHERE teacher_id = ?", (teacher_id,))
    rows = cursor.fetchall()
    conn.close()
    return [Discipline(id=row[0], name=row[1], teacher_id=row[2]) for row in rows]