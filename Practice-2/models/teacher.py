from database.db_administrator import get_connection

class Teacher:
    def __init__(self, id=None, full_name=None):
        """
        Модель преподавателя
        :param id: уникальный идентификатор (None для нового)
        :param full_name: ФИО преподавателя
        """
        self.id = id
        self.full_name = full_name

    def save(self):
        """Сохраняет преподавателя: добавляет нового или обновляет существующего"""
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute('''
                INSERT INTO teachers (full_name)
                VALUES (?)
            ''', (self.full_name,))
            self.id = cursor.lastrowid
        else:
            cursor.execute('''
                UPDATE teachers SET full_name = ?
                WHERE id = ?
            ''', (self.full_name, self.id))
        conn.commit()
        conn.close()

    def delete(self):
        """Удаляет преподавателя из базы данных"""
        if self.id is not None:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM teachers WHERE id = ?", (self.id,))
            conn.commit()
            conn.close()

def get_all_teachers():
    """Возвращает список всех преподавателей"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT teacher_id, full_name FROM teachers")
    rows = cursor.fetchall()
    conn.close()
    return [Teacher(id=row[0], full_name=row[1]) for row in rows]

def get_teacher_by_id(teacher_id):
    """Возвращает преподавателя по ID или None, если не найден"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT teacher_id, full_name FROM teachers WHERE teacher_id = ?", (teacher_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Teacher(id=row[0], full_name=row[1])
    return None