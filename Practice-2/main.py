from database.db_administrator import initialize_db   
from ui.menu import show_main_menu
from ui.menu_students import menu_students
from ui.menu_teachers import menu_teachers
from ui.menu_disciplines import menu_disciplines
from ui.menu_grades import menu_grades
from ui.menu_groups import menu_groups
from ui.menu_attendance import menu_attendance
from ui.menu_schedule import menu_schedule

def main():
    initialize_db()
    while True:
        choice = show_main_menu()
        if choice == "1":
            menu_students()
        elif choice == "2":
            menu_teachers()
        elif choice == "3":
            menu_disciplines()
        elif choice == "4":
            menu_grades()
        elif choice == "5":
            menu_schedule()
        elif choice == "6":
            menu_attendance()
        elif choice == "7":
            menu_groups()
        elif choice == "0":
            print("Работа завершена.")
            break
        else:
            print("Неверный ввод.")

if __name__ == "__main__":
    main()