from models.grade import Grade, get_all_grades, get_grade_by_id
from models.student import get_all_students, get_student_by_id
from models.discipline import get_all_disciplines, get_discipline_by_id

def print_grades_table(grades):
    """Выводит список оценок в виде таблицы."""
    if not grades:
        print("\nОценки не найдены.")
        return

    # Подготовим словари для быстрого получения имени студента и дисциплины
    students = {s.id: s.full_name for s in get_all_students()}
    disciplines = {d.id: d.name for d in get_all_disciplines()}

    print("\n" + "-" * 80)
    print(f"{'ID':<5} {'Студент':<30} {'Дисциплина':<25} {'Оценка':<8} {'Дата':<12}")
    print("-" * 80)
    for g in grades:
        student_name = students.get(g.student_id, f"ID {g.student_id}")
        discipline_name = disciplines.get(g.discipline_id, f"ID {g.discipline_id}")
        print(f"{g.id:<5} {student_name:<30} {discipline_name:<25} {g.grade_value:<8} {g.date_received:<12}")
    print("-" * 80)

def list_grades():
    """Показать все оценки."""
    grades = get_all_grades()
    print_grades_table(grades)

def add_grade():
    """Добавить новую оценку."""
    print("\n--- Добавление оценки ---")

    # Проверка наличия студентов
    students = get_all_students()
    if not students:
        print("Нет ни одного студента. Сначала добавьте студента.")
        return
    print("\nСписок студентов:")
    for s in students:
        print(f"  ID {s.id}: {s.full_name} (группа {s.group_name})")
    try:
        student_id = int(input("Введите ID студента: ").strip())
        if not get_student_by_id(student_id):
            print("Студент с таким ID не найден.")
            return
    except ValueError:
        print("ID должен быть числом.")
        return

    # Проверка наличия дисциплин
    disciplines = get_all_disciplines()
    if not disciplines:
        print("Нет ни одной дисциплины. Сначала добавьте дисциплину.")
        return
    print("\nСписок дисциплин:")
    for d in disciplines:
        print(f"  ID {d.id}: {d.name}")
    try:
        discipline_id = int(input("Введите ID дисциплины: ").strip())
        if not get_discipline_by_id(discipline_id):
            print("Дисциплина с таким ID не найдена.")
            return
    except ValueError:
        print("ID должен быть числом.")
        return

    # Оценка (2-5)
    try:
        grade_value = int(input("Введите оценку (от 2 до 5): ").strip())
        if grade_value < 2 or grade_value > 5:
            print("Оценка должна быть в диапазоне 2-5.")
            return
    except ValueError:
        print("Оценка должна быть целым числом.")
        return

    # Дата в формате ГГГГ-ММ-ДД
    date_received = input("Введите дату в формате ГГГГ-ММ-ДД: ").strip()
    if not date_received:
        print("Дата не может быть пустой.")
        return

    grade = Grade(
        student_id=student_id,
        discipline_id=discipline_id,
        grade_value=grade_value,
        date_received=date_received
    )
    grade.save()
    print(f"Оценка успешно добавлена (ID: {grade.id}).")

def delete_grade():
    """Удалить оценку по ID."""
    print("\n--- Удаление оценки ---")
    try:
        gid = int(input("Введите ID оценки для удаления: ").strip())
    except ValueError:
        print("ID должен быть числом.")
        return

    grade = get_grade_by_id(gid)
    if not grade:
        print(f"Оценка с ID {gid} не найдена.")
        return

    print(f"Вы действительно хотите удалить оценку (ID {gid})?")
    confirm = input("Введите 'да' для подтверждения: ").strip().lower()
    if confirm == 'да':
        grade.delete()
        print("Оценка удалена.")
    else:
        print("Удаление отменено.")

def menu_grades():
    """Главное меню управления оценками."""
    while True:
        print("\n=== Управление оценками ===")
        print("1. Показать все оценки")
        print("2. Добавить оценку")
        print("3. Удалить оценку")
        print("0. Назад в главное меню")
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            list_grades()
        elif choice == "2":
            add_grade()
        elif choice == "3":
            delete_grade()
        elif choice == "0":
            break
        else:
            print("Неверный ввод. Попробуйте снова.")