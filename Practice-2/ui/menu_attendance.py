from models.attendance import (
    get_all_attendance, get_attendance_by_id, get_attendance_by_student,
    get_attendance_summary, Attendance
)
from models.student import get_all_students, get_student_by_id
from models.discipline import get_all_disciplines, get_discipline_by_id

def print_attendance_table(records):
    """Выводит список записей посещаемости в виде таблицы."""
    if not records:
        print("\nЗаписи посещаемости не найдены.")
        return

    # Загружаем справочники для отображения имён
    students = {s.id: s.full_name for s in get_all_students()}
    disciplines = {d.id: d.name for d in get_all_disciplines()}

    print("\n" + "-" * 80)
    print(f"{'ID':<5} {'Студент':<30} {'Дисциплина':<25} {'Дата':<12} {'Статус':<10}")
    print("-" * 80)
    for r in records:
        student_name = students.get(r.student_id, f"ID {r.student_id}")
        disc_name = disciplines.get(r.discipline_id, f"ID {r.discipline_id}")
        status_ru = {
            'present': 'Присутствовал',
            'absent': 'Отсутствовал',
            'late': 'Опоздал'
        }.get(r.status, r.status)
        print(f"{r.id:<5} {student_name:<30} {disc_name:<25} {r.date:<12} {status_ru:<10}")
    print("-" * 80)

def list_all_attendance():
    """Показать все записи посещаемости."""
    records = get_all_attendance()
    print_attendance_table(records)

def list_attendance_by_student():
    """Показать посещаемость конкретного студента с краткой статистикой."""
    # Выбор студента
    students = get_all_students()
    if not students:
        print("\nНет студентов. Сначала добавьте студентов.")
        return
    print("\nСписок студентов:")
    for s in students:
        print(f"  {s.id}: {s.full_name} (группа {s.group_name})")
    try:
        sid = int(input("Введите ID студента: "))
    except ValueError:
        print("ID должен быть числом.")
        return

    if not get_student_by_id(sid):
        print("Студент не найден.")
        return

    records = get_attendance_by_student(sid)
    if records:
        print_attendance_table(records)
    else:
        print("У этого студента пока нет записей посещаемости.")

    # Вывод статистики
    summary = get_attendance_summary(sid)
    print(f"\nСтатистика посещаемости:")
    print(f"  Присутствовал: {summary['present']}")
    print(f"  Отсутствовал: {summary['absent']}")
    print(f"  Опоздал: {summary['late']}")
    print(f"  Всего занятий: {summary['total']}")
    print(f"  Процент присутствия: {summary['present_percent']}%")

def add_attendance():
    """Добавить новую запись о посещаемости."""
    print("\n--- Добавление записи посещаемости ---")

    # Выбор студента
    students = get_all_students()
    if not students:
        print("Нет студентов. Сначала добавьте студентов.")
        return
    print("Студенты:")
    for s in students:
        print(f"  {s.id}: {s.full_name} (группа {s.group_name})")
    try:
        student_id = int(input("ID студента: "))
    except ValueError:
        print("ID должен быть числом.")
        return

    # Выбор дисциплины
    disciplines = get_all_disciplines()
    if not disciplines:
        print("Нет дисциплин. Сначала добавьте дисциплины.")
        return
    print("Дисциплины:")
    for d in disciplines:
        print(f"  {d.id}: {d.name}")
    try:
        disc_id = int(input("ID дисциплины: "))
    except ValueError:
        print("ID должен быть числом.")
        return

    # Дата
    date = input("Дата занятия (ГГГГ-ММ-ДД): ").strip()
    if not date:
        print("Дата не может быть пустой.")
        return

    # Статус
    print("Статус:")
    print("  1. Присутствовал (present)")
    print("  2. Отсутствовал (absent)")
    print("  3. Опоздал (late)")
    status_choice = input("Выберите статус (1-3): ").strip()
    status_map = {
        '1': 'present',
        '2': 'absent',
        '3': 'late'
    }
    if status_choice not in status_map:
        print("Неверный выбор статуса.")
        return
    status = status_map[status_choice]

    attendance = Attendance(
        student_id=student_id,
        discipline_id=disc_id,
        date=date,
        status=status
    )
    try:
        attendance.save()
        print(f"Запись посещаемости добавлена (ID: {attendance.id})")
    except ValueError as e:
        print(f"Ошибка: {e}")

def delete_attendance():
    """Удалить запись посещаемости по ID."""
    print("\n--- Удаление записи посещаемости ---")
    try:
        aid = int(input("Введите ID записи для удаления: "))
    except ValueError:
        print("ID должен быть числом.")
        return

    record = get_attendance_by_id(aid)
    if not record:
        print(f"Запись с ID {aid} не найдена.")
        return

    confirm = input(f"Удалить запись {aid}? (введите 'да' для подтверждения): ").strip().lower()
    if confirm == 'да':
        record.delete()
        print("Запись удалена.")
    else:
        print("Удаление отменено.")

def menu_attendance():
    """Главное меню управления посещаемостью."""
    while True:
        print("\n=== Управление посещаемостью ===")
        print("1. Показать все записи посещаемости")
        print("2. Показать посещаемость студента")
        print("3. Добавить запись о посещаемости")
        print("4. Удалить запись о посещаемости")
        print("0. Назад")
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            list_all_attendance()
        elif choice == "2":
            list_attendance_by_student()
        elif choice == "3":
            add_attendance()
        elif choice == "4":
            delete_attendance()
        elif choice == "0":
            break
        else:
            print("Неверный ввод. Попробуйте снова.")