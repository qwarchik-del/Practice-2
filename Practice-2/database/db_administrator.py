import sqlite3

# Имя файла базы данных
DB_NAME = "student_progress.db"

def get_connection():
    """Возвращает соединение с базой данных."""
    return sqlite3.connect(DB_NAME)

def initialize_db():
    """Создаёт все таблицы, если они ещё не существуют."""
    conn = get_connection()
    cursor = conn.cursor()

    # Таблица "Группы"
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,          -- название группы (например, П-31)
            specialty TEXT                      -- специальность
        )
    ''')

    # Таблица "Студенты"
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            enrollment_year INTEGER,
            group_name TEXT
        )
    ''')

    # Таблица "Преподаватели"
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL
        )
    ''')

    # Таблица "Дисциплины"
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS disciplines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            teacher_id INTEGER,
            FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE SET NULL
        )
    ''')

    # Таблица "Оценки" (успеваемость)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            discipline_id INTEGER,
            grade_value INTEGER CHECK (grade_value BETWEEN 2 AND 5),
            date_received TEXT NOT NULL,            -- дата в формате YYYY-MM-DD
            FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
            FOREIGN KEY (discipline_id) REFERENCES disciplines(id) ON DELETE CASCADE
        )
    ''')

    # Таблица "Посещаемость"
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            discipline_id INTEGER,
            date TEXT NOT NULL,
            status TEXT CHECK (status IN ('present', 'absent', 'late')),
            FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
            FOREIGN KEY (discipline_id) REFERENCES disciplines(id) ON DELETE CASCADE
        )
    ''')

    #Таблица "Расписание"
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER NOT NULL,
            discipline_id INTEGER NOT NULL,
            teacher_id INTEGER NOT NULL,
            day_of_week TEXT NOT NULL,
            lesson_number INTEGER NOT NULL,
            FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE,
            FOREIGN KEY (discipline_id) REFERENCES disciplines(id) ON DELETE CASCADE,
            FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()
    print(f"База данных '{DB_NAME}' успешно инициализирована.")