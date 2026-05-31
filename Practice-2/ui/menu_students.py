from models.student import get_all_students, get_student_by_id, Student

def print_students_table(students):
    """Выводит список студентов в виде таблицы."""
    if not students:
        print("\nСтуденты не найдены.")
        return
    print("\n" + "-" * 70)
    print(f"{'ID':<5} {'ФИО':<30} {'Группа':<15} {'Год поступления':<10}")
    print("-" * 70)
    for s in students:
        year = str(s.enrollment_year) if s.enrollment_year else ""
        print(f"{s.id:<5} {s.full_name:<30} {s.group_name:<15} {year:<10}")
    print("-" * 70)

def list_students():
    """Показать всех студентов."""
    students = get_all_students()
    print_students_table(students)

def add_student():
    """Добавить нового студента."""
    print("\n--- Добавление студента ---")
    full_name = input("ФИО студента: ").strip()
    if not full_name:
        print("Ошибка: ФИО не может быть пустым.")
        return
    group_name = input("Группа: ").strip()
    enrollment_year = input("Год поступления: ").strip()
    try:
        year_int = int(enrollment_year) if enrollment_year else None
    except ValueError:
        print("Год поступления должен быть числом. Запись не добавлена.")
        return

    student = Student(full_name=full_name, group_name=group_name, enrollment_year=year_int)
    student.save()
    print(f"Студент '{full_name}' успешно добавлен (ID: {student.id}).")

def delete_student():
    """Удалить студента по ID."""
    print("\n--- Удаление студента ---")
    try:
        sid = int(input("Введите ID студента для удаления: "))
    except ValueError:
        print("ID должен быть числом.")
        return

    student = get_student_by_id(sid)
    if not student:
        print(f"Студент с ID {sid} не найден.")
        return

    print(f"Вы действительно хотите удалить студента: {student.full_name}?")
    confirm = input("Введите 'да' для подтверждения: ").strip().lower()
    if confirm == 'да':
        student.delete()
        print("Студент удалён.")
    else:
        print("Удаление отменено.")

def menu_students():
    """Главное меню управления студентами."""
    while True:
        print("\n=== Управление студентами ===")
        print("1. Показать всех студентов")
        print("2. Добавить студента")
        print("3. Удалить студента")
        print("0. Назад в главное меню")
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            list_students()
        elif choice == "2":
            add_student()
        elif choice == "3":
            delete_student()
        elif choice == "0":
            break
        else:
            print("Неверный ввод. Попробуйте снова.")