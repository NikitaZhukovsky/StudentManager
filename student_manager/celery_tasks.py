from celery import shared_task
import json
import os
from django.db import transaction


@shared_task
def update_daily_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, "data.json")

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        return "Не удалось прочитать файл data.json"

    from students.models import Student
    from courses.models import Course
    from assignments.models import Assignment
    from submissions.models import Submission

    try:
        with transaction.atomic():

            for student in data.get("students", []):
                Student.objects.update_or_create(
                    id=student["id"],
                    defaults={
                        "full_name": student["full_name"],
                        "email": student["email"]
                    }
                )

            for course in data.get("courses", []):
                Course.objects.update_or_create(
                    id=course["id"],
                    defaults={
                        "title": course["title"],
                        "code": course["code"]
                    }
                )

            for enroll in data.get("course_enrollments", []):
                student = Student.objects.get(id=enroll["student_id"])
                course = Course.objects.get(id=enroll["course_id"])
                course.students.add(student)

            for assignment in data.get("assignments", []):
                course = Course.objects.get(id=assignment["course_id"])
                Assignment.objects.update_or_create(
                    id=assignment["id"],
                    defaults={
                        "title": assignment["title"],
                        "description": assignment.get("description", ""),
                        "course": course,
                        "due_date": assignment["due_date"]
                    }
                )

            for submission in data.get("submissions", []):
                student = Student.objects.get(id=submission["student_id"])
                assignment = Assignment.objects.get(id=submission["assignment_id"])

                date = submission["submitted_at"]
                if "T" in date:
                    date = date.split("T")[0]

                Submission.objects.update_or_create(
                    id=submission["id"],
                    defaults={
                        "student": student,
                        "assignment": assignment,
                        "file_path": submission["file_path"],
                        "submitted_at": date
                    }
                )

            return "Данные обновлены"

    except Exception as error:
        return f" Ошибка: {error}"

