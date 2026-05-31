from database.db_administrator import get_connection

class Group:
    """
    Модель группы студентов (только для просмотра).
    Атрибуты:
        id        - уникальный идентификатор
        name      - название группы (например, П-31)
        specialty - специальность
    """
    def __init__(self, id=None, name=None, specialty=None):
        self.id = id
        self.name = name
        self.specialty = specialty

def get_all_groups():
    """Возвращает список всех групп."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, specialty FROM groups")
    rows = cursor.fetchall()
    conn.close()
    return [Group(id=row[0], name=row[1], specialty=row[2]) for row in rows]

def get_group_by_id(group_id):
    """Возвращает группу по ID или None, если не найдена."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, specialty FROM groups WHERE id = ?", (group_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Group(id=row[0], name=row[1], specialty=row[2])
    return None