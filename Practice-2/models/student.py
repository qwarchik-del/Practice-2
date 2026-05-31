from database.db_administrator import get_connection

class Student:
    def __init__(self, id=None, full_name=None, group_name=None, enrollment_year=None):
        self.id = id
        self.full_name = full_name
        self.group_name = group_name
        self.enrollment_year = enrollment_year

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute('''
                INSERT INTO students (full_name, group_name, enrollment_year)
                VALUES (?, ?, ?)
            ''', (self.full_name, self.group_name, self.enrollment_year))
            self.id = cursor.lastrowid
        else:
            cursor.execute('''
                UPDATE students SET full_name=?, group_name=?, enrollment_year=?
                WHERE id=?
            ''', (self.full_name, self.group_name, self.enrollment_year, self.id))
        conn.commit()
        conn.close()

    def delete(self):
        if self.id is not None:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE id=?", (self.id,))
            conn.commit()
            conn.close()

def get_all_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name, group_name, enrollment_year FROM students")
    rows = cursor.fetchall()
    conn.close()
    return [Student(id=r[0], full_name=r[1], group_name=r[2], enrollment_year=r[3]) for r in rows]

def get_student_by_id(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name, group_name, enrollment_year FROM students WHERE id=?", (student_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Student(id=row[0], full_name=row[1], group_name=row[2], enrollment_year=row[3])
    return None