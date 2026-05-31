from models.discipline import get_all_disciplines, get_discipline_by_id, Discipline
from models.teacher import get_all_teachers

def print_disciplines_table(disciplines):
    """Выводит список дисциплин в виде таблицы."""
    if not disciplines:
        print("\nДисциплины не найдены.")
        return
    print("\n" + "-" * 60)
    print(f"{'ID':<5} {'Название':<30} {'ID преподавателя':<15} {'Преподаватель':<20}")
    print("-" * 60)
    for d in disciplines:
        teacher_name = ""
        if d.teacher_id:
            # Пытаемся получить ФИО преподавателя
            from models.teacher import get_teacher_by_id
            teacher = get_teacher_by_id(d.teacher_id)
            teacher_name = teacher.full_name if teacher else ""
        print(f"{d.id:<5} {d.name:<30} {str(d.teacher_id or ''):<15} {teacher_name:<20}")
    print("-" * 60)

def list_disciplines():
    """Показать все дисциплины."""
    disciplines = get_all_disciplines()
    print_disciplines_table(disciplines)

def add_discipline():
    """Добавить новую дисциплину."""
    print("\n--- Добавление дисциплины ---")
    name = input("Название дисциплины: ").strip()
    if not name:
        print("Ошибка: название не может быть пустым.")
        return

    # Показать список преподавателей для выбора
    teachers = get_all_teachers()
    teacher_id = None
    if teachers:
        print("\nСписок преподавателей:")
        for t in teachers:
            print(f"  ID {t.id}: {t.full_name}")
        choice = input("Введите ID преподавателя (или оставьте пустым, если не нужно): ").strip()
        if choice:
            try:
                tid = int(choice)
                # Проверим, существует ли такой преподаватель
                from models.teacher import get_teacher_by_id
                if get_teacher_by_id(tid):
                    teacher_id = tid
                else:
                    print(f"Преподаватель с ID {tid} не найден. Дисциплина будет создана без преподавателя.")
            except ValueError:
                print("Некорректный ID. Дисциплина будет создана без преподавателя.")
    else:
        print("Преподаватели отсутствуют. Дисциплина будет создана без привязки к преподавателю.")

    discipline = Discipline(name=name, teacher_id=teacher_id)
    discipline.save()
    print(f"Дисциплина '{name}' успешно добавлена (ID: {discipline.id}).")

def delete_discipline():
    """Удалить дисциплину по ID."""
    print("\n--- Удаление дисциплины ---")
    try:
        did = int(input("Введите ID дисциплины для удаления: "))
    except ValueError:
        print("ID должен быть числом.")
        return

    discipline = get_discipline_by_id(did)
    if not discipline:
        print(f"Дисциплина с ID {did} не найдена.")
        return

    print(f"Вы действительно хотите удалить дисциплину: {discipline.name}?")
    confirm = input("Введите 'да' для подтверждения: ").strip().lower()
    if confirm == 'да':
        discipline.delete()
        print("Дисциплина удалена.")
    else:
        print("Удаление отменено.")

def menu_disciplines():
    """Главное меню управления дисциплинами."""
    while True:
        print("\n=== Управление дисциплинами ===")
        print("1. Показать все дисциплины")
        print("2. Добавить дисциплину")
        print("3. Удалить дисциплину")
        print("0. Назад в главное меню")
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            list_disciplines()
        elif choice == "2":
            add_discipline()
        elif choice == "3":
            delete_discipline()
        elif choice == "0":
            break
        else:
            print("Неверный ввод. Попробуйте снова.")