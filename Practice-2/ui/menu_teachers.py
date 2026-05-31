from models.teacher import get_all_teachers, get_teacher_by_id, Teacher

def print_teachers_table(teachers):
    if not teachers:
        print("\nПреподаватели не найдены.")
        return
    print("\n" + "-" * 50)
    print(f"{'ID':<5} {'ФИО':<40}")
    print("-" * 50)
    for t in teachers:
        print(f"{t.id:<5} {t.full_name:<40}")
    print("-" * 50)

def list_teachers():
    teachers = get_all_teachers()
    print_teachers_table(teachers)

def add_teacher():
    print("\n--- Добавление преподавателя ---")
    full_name = input("ФИО преподавателя: ").strip()
    if not full_name:
        print("Ошибка: ФИО не может быть пустым.")
        return
    teacher = Teacher(full_name=full_name)
    teacher.save()
    print(f"Преподаватель '{full_name}' успешно добавлен (ID: {teacher.id}).")

def delete_teacher():
    print("\n--- Удаление преподавателя ---")
    try:
        tid = int(input("Введите ID преподавателя для удаления: "))
    except ValueError:
        print("ID должен быть числом.")
        return
    teacher = get_teacher_by_id(tid)
    if not teacher:
        print(f"Преподаватель с ID {tid} не найден.")
        return
    print(f"Удалить преподавателя: {teacher.full_name}?")
    confirm = input("Введите 'да' для подтверждения: ").strip().lower()
    if confirm == 'да':
        teacher.delete()
        print("Преподаватель удалён.")
    else:
        print("Удаление отменено.")

def menu_teachers():
    while True:
        print("\n=== Управление преподавателями ===")
        print("1. Показать всех преподавателей")
        print("2. Добавить преподавателя")
        print("3. Удалить преподавателя")
        print("0. Назад в главное меню")
        choice = input("Выберите действие: ").strip()
        if choice == "1":
            list_teachers()
        elif choice == "2":
            add_teacher()
        elif choice == "3":
            delete_teacher()
        elif choice == "0":
            break
        else:
            print("Неверный ввод.")