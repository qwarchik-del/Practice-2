from models.student import get_all_students
from models.grade import get_grades_by_student
from statistics import mean

def report_average_score():
    students = get_all_students()
    print("\n=== Средний балл каждого студента ===")
    for s in students:
        grades = get_grades_by_student(s.id)
        if grades:
            avg = mean([g.grade_value for g in grades])
            print(f"{s.full_name} (группа {s.group_name}): средний балл = {avg:.2f}")
        else:
            print(f"{s.full_name}: оценок нет")

def report_debtors():
    # Студенты, имеющие хотя бы одну оценку 2
    print("\n=== Должники (оценка 2) ===")
    # ... логика выборки ...