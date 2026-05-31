import sqlite3
from database.db_administrator import get_connection, initialize_db
from datetime import datetime, timedelta
import random

def clear_tables():

    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA foreign_keys = OFF")
    tables = ['schedule', 'attendance', 'grades', 'students', 'disciplines', 'teachers', 'groups']
    for table in tables:
        cursor.execute(f"DELETE FROM {table}")
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}'")
    cursor.execute("PRAGMA foreign_keys = ON")
    conn.commit()
    conn.close()
    print("Таблицы очищены.")

def populate_groups():
    groups_data = [
        ("П-31", "Программирование"),
        ("П-32", "Программирование"),
        ("ИС-21", "Информационные системы"),
        ("ИС-22", "Информационные системы"),
    ]
    conn = get_connection()
    cursor = conn.cursor()
    for name, specialty in groups_data:
        cursor.execute(
            "INSERT INTO groups (name, specialty) VALUES (?, ?)",
            (name, specialty)
        )
    conn.commit()
    conn.close()
    print(f"Добавлено {len(groups_data)} групп.")

def populate_teachers():
    teachers_data = [
        "Иванов Иван Иванович",
        "Петрова Мария Сергеевна",
        "Сидоров Алексей Владимирович",
        "Кузнецова Елена Дмитриевна",
    ]
    conn = get_connection()
    cursor = conn.cursor()
    for full_name in teachers_data:
        cursor.execute(
            "INSERT INTO teachers (full_name) VALUES (?)",
            (full_name,)
        )
    conn.commit()
    conn.close()
    print(f"Добавлено {len(teachers_data)} преподавателей.")

def populate_students():
    students_data = [
        ("Антонов Антон Антонович", "П-31", 2024),
        ("Борисова Елена Павловна", "П-31", 2024),
        ("Васильев Дмитрий Сергеевич", "П-31", 2024),
        ("Григорьева Анна Игоревна", "П-32", 2024),
        ("Дмитриев Роман Алексеевич", "П-32", 2024),
        ("Егорова Ксения Владимировна", "ИС-21", 2023),
        ("Жуков Андрей Петрович", "ИС-21", 2023),
        ("Зайцева Мария Ивановна", "ИС-22", 2023),
        ("Ильин Павел Сергеевич", "ИС-22", 2023),
    ]
    conn = get_connection()
    cursor = conn.cursor()
    for full_name, group_name, year in students_data:
        cursor.execute(
            "INSERT INTO students (full_name, group_name, enrollment_year) VALUES (?, ?, ?)",
            (full_name, group_name, year)
        )
    conn.commit()
    conn.close()
    print(f"Добавлено {len(students_data)} студентов.")

def populate_disciplines():
    # Получаем ID преподавателей
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT teacher_id, full_name FROM teachers")
    teachers = cursor.fetchall()
    teacher_map = {name: id for id, name in teachers}
    conn.close()

    disciplines_data = [
        ("Основы программирования", teacher_map.get("Иванов Иван Иванович")),
        ("Базы данных", teacher_map.get("Петрова Мария Сергеевна")),
        ("Веб-технологии", teacher_map.get("Сидоров Алексей Владимирович")),
        ("Операционные системы", teacher_map.get("Кузнецова Елена Дмитриевна")),
        ("Математика", teacher_map.get("Петрова Мария Сергеевна")),
    ]
    conn = get_connection()
    cursor = conn.cursor()
    for name, teacher_id in disciplines_data:
        cursor.execute(
            "INSERT INTO disciplines (name, teacher_id) VALUES (?, ?)",
            (name, teacher_id)
        )
    conn.commit()
    conn.close()
    print(f"Добавлено {len(disciplines_data)} дисциплин.")

def populate_grades():
    # Получаем студентов и дисциплины
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM students")
    student_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT id FROM disciplines")
    discipline_ids = [row[0] for row in cursor.fetchall()]
    conn.close()

    if not student_ids or not discipline_ids:
        print("Нет студентов или дисциплин, оценки не добавлены.")
        return

    grades_data = []
    start_date = datetime(2025, 9, 1)
    end_date = datetime(2026, 1, 31)
    date_range = (end_date - start_date).days

    for _ in range(50):  # 50 случайных оценок
        student_id = random.choice(student_ids)
        disc_id = random.choice(discipline_ids)
        grade_value = random.choice([3, 4, 5])
        random_days = random.randint(0, date_range)
        grade_date = (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")
        grades_data.append((student_id, disc_id, grade_value, grade_date))

    conn = get_connection()
    cursor = conn.cursor()
    for data in grades_data:
        cursor.execute(
            "INSERT INTO grades (student_id, discipline_id, grade_value, date_received) VALUES (?, ?, ?, ?)",
            data
        )
    conn.commit()
    conn.close()
    print(f"Добавлено {len(grades_data)} оценок.")

def populate_attendance():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM students")
    student_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT id FROM disciplines")
    discipline_ids = [row[0] for row in cursor.fetchall()]
    conn.close()

    if not student_ids or not discipline_ids:
        print("Нет студентов или дисциплин, посещаемость не добавлена.")
        return

    attendance_data = []
    start_date = datetime(2025, 9, 1)
    end_date = datetime(2026, 1, 31)
    date_range = (end_date - start_date).days

    statuses = ['present', 'absent', 'late']
    weights = [0.7, 0.2, 0.1]  # 70% присутствует, 20% отсутствует, 10% опоздал

    for _ in range(200):  # 200 записей
        student_id = random.choice(student_ids)
        disc_id = random.choice(discipline_ids)
        status = random.choices(statuses, weights=weights)[0]
        random_days = random.randint(0, date_range)
        date = (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")
        attendance_data.append((student_id, disc_id, date, status))

    conn = get_connection()
    cursor = conn.cursor()
    for data in attendance_data:
        cursor.execute(
            "INSERT INTO attendance (student_id, discipline_id, date, status) VALUES (?, ?, ?, ?)",
            data
        )
    conn.commit()
    conn.close()
    print(f"Добавлено {len(attendance_data)} записей посещаемости.")

def populate_schedule():
    # Получаем группы, дисциплины, преподавателей
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM groups")
    groups = cursor.fetchall()
    group_ids = [g[0] for g in groups]
    cursor.execute("SELECT id FROM disciplines")
    discipline_ids = [d[0] for d in cursor.fetchall()]
    cursor.execute("SELECT teacher_id FROM teachers")
    teacher_ids = [t[0] for t in cursor.fetchall()]
    conn.close()

    if not group_ids or not discipline_ids:
        print("Нет групп или дисциплин, расписание не добавлено.")
        return

    days = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб']
    lesson_numbers = [1, 2, 3, 4]

    schedule_data = []
    # Для каждой группы добавим 8-12 занятий
    for group_id in group_ids:
        num_lessons = random.randint(8, 12)
        for _ in range(num_lessons):
            disc_id = random.choice(discipline_ids)
            teacher_id = random.choice(teacher_ids)
            day = random.choice(days)
            lesson = random.choice(lesson_numbers)
            schedule_data.append((group_id, disc_id, teacher_id, day, lesson))

    # Удаляем возможные дубли (одна группа, одна дисциплина, день и пара)
    unique_data = list(set(schedule_data))

    conn = get_connection()
    cursor = conn.cursor()
    for data in unique_data:
        cursor.execute(
            "INSERT INTO schedule (group_id, discipline_id, teacher_id, day_of_week, lesson_number) VALUES (?, ?, ?, ?, ?)",
            data
        )
    conn.commit()
    conn.close()
    print(f"Добавлено {len(unique_data)} записей расписания.")

def populate_all():
    """Заполняет базу данных всеми тестовыми данными."""
    print("Начало заполнения базы данных...")
    clear_tables()
    populate_groups()
    populate_teachers()
    populate_students()
    populate_disciplines()
    populate_grades()
    populate_attendance()
    populate_schedule()
    print("База данных успешно заполнена тестовыми данными.")

if __name__ == "__main__":
    # Сначала создаём таблицы, если их нет
    initialize_db()
    populate_all()