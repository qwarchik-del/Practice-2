from models.group import get_all_groups

def list_group_names():
    """Выводит только названия всех групп."""
    groups = get_all_groups()
    if not groups:
        print("\nГруппы не найдены.")
        return
    print("\n=== Список групп ===")
    for i, group in enumerate(groups, 1):
        print(f"{i}. {group.name}")
    print(f"\nВсего групп: {len(groups)}")

def menu_groups():
    """Меню просмотра названий групп."""
    while True:
        print("\n=== Просмотр групп ===")
        print("1. Показать названия групп")
        print("0. Назад")
        choice = input("Выберите действие: ").strip()
        if choice == "1":
            list_group_names()
        elif choice == "0":
            break
        else:
            print("Неверный ввод. Попробуйте снова.")