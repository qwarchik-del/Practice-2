import sqlite3
from config import DB_NAME
from models.schedule import Schedule, get_all_schedules, get_schedule_by_id

# ----- Вспомогательные функции для получения имён (без импорта других моделей) -----
def _get_group_name(group_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM groups WHERE id = ?', (group_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else str(group_id)

def _get_discipline_name(discipline_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM disciplines WHERE id = ?', (discipline_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else str(discipline_id)

def _get_teacher_name(teacher_id):
    if teacher_id is None:
        return '---'
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT full_name FROM teachers WHERE teacher_id = ?', (teacher_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else '---'

def _get_all_groups():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM groups ORDER BY name')
    rows = cursor.fetchall()
    conn.close()
    return rows

def _get_all_disciplines():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM disciplines ORDER BY name')
    rows = cursor.fetchall()
    conn.close()
    return rows

def _get_all_teachers():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT teacher_id, full_name FROM teachers ORDER BY full_name')
    rows = cursor.fetchall()
    conn.close()
    return rows


# ----- Функции меню -----
def print_schedule_table(schedules):
    """Выводит список записей расписания в виде таблицы."""
    if not schedules:
        print("\nРасписание пусто.")
        return
    print("\n" + "-" * 80)
    print(f"{'ID':<4} {'Группа':<12} {'Дисциплина':<20} {'Преподаватель':<20} {'День':<4} {'Пара':<4}")
    print("-" * 80)
    for s in schedules:
        group_name = _get_group_name(s.group_id)
        disc_name = _get_discipline_name(s.discipline_id)
        teacher_name = _get_teacher_name(s.teacher_id)
        print(f"{s.id:<4} {group_name:<12} {disc_name:<20} {teacher_name:<20} {s.day_of_week:<4} {s.lesson_number:<4}")
    print("-" * 80)

def list_schedules():
    """Показать всё расписание."""
    schedules = get_all_schedules()
    print_schedule_table(schedules)

def add_schedule():
    """Добавить новую запись расписания."""
    print("\n--- Добавление записи расписания ---")

    groups = _get_all_groups()
    if not groups:
        print("Нет групп. Сначала добавьте группы.")
        return
    print("Группы:")
    for gid, name in groups:
        print(f"  {gid}: {name}")
    try:
        group_id = int(input("ID группы: "))
    except ValueError:
        print("ID должен быть числом.")
        return

    disciplines = _get_all_disciplines()
    if not disciplines:
        print("Нет дисциплин. Сначала добавьте дисциплины.")
        return
    print("Дисциплины:")
    for did, name in disciplines:
        print(f"  {did}: {name}")
    try:
        disc_id = int(input("ID дисциплины: "))
    except ValueError:
        print("ID должен быть числом.")
        return

    teachers = _get_all_teachers()
    teacher_id = None
    if teachers:
        print("Преподаватели (можно оставить пустым):")
        for tid, name in teachers:
            print(f"  {tid}: {name}")
        inp = input("ID преподавателя (или Enter): ").strip()
        if inp:
            try:
                teacher_id = int(inp)
            except ValueError:
                print("Некорректный ID, преподаватель не будет привязан.")

    day = input("День недели (пн, вт, ср, чт, пт, сб): ").strip().lower()
    if day not in ('пн', 'вт', 'ср', 'чт', 'пт', 'сб'):
        print("Некорректный день.")
        return

    try:
        lesson = int(input("Номер пары (1-6): "))
    except ValueError:
        print("Номер пары должен быть числом.")
        return

    schedule = Schedule(
        group_id=group_id,
        discipline_id=disc_id,
        teacher_id=teacher_id,
        day_of_week=day,
        lesson_number=lesson
    )
    try:
        schedule.save()
        print(f"Запись расписания добавлена (ID: {schedule.id})")
    except Exception as e:
        print(f"Ошибка: {e}")

def delete_schedule():
    """Удалить запись расписания по ID."""
    print("\n--- Удаление записи расписания ---")
    try:
        sid = int(input("Введите ID записи для удаления: "))
    except ValueError:
        print("ID должен быть числом.")
        return
    s = get_schedule_by_id(sid)
    if not s:
        print(f"Запись с ID {sid} не найдена.")
        return
    confirm = input(f"Удалить запись {sid}? (введите 'да' для подтверждения): ").strip().lower()
    if confirm == 'да':
        s.delete()
        print("Запись удалена.")
    else:
        print("Удаление отменено.")

def menu_schedule():
    """Главное меню управления расписанием."""
    while True:
        print("\n=== Управление расписанием ===")
        print("1. Показать всё расписание")
        print("2. Добавить занятие")
        print("3. Удалить занятие")
        print("0. Назад")
        choice = input("Выберите действие: ").strip()
        if choice == "1":
            list_schedules()
        elif choice == "2":
            add_schedule()
        elif choice == "3":
            delete_schedule()
        elif choice == "0":
            break
        else:
            print("Неверный ввод. Попробуйте снова.")