from celery import shared_task
import json
from pathlib import Path
from django.db import transaction


@shared_task
def update_daily_data():
    """Обновление данных из JSON файла"""
    # Ленивый импорт моделей (избегаем AppRegistryNotReady)
    from django.apps import apps
    Student = apps.get_model('students', 'Student')
    Course = apps.get_model('courses', 'Course')
    Assignment = apps.get_model('assignments', 'Assignment')
    Submission = apps.get_model('submissions', 'Submission')

    json_path = Path(__file__).resolve().parent.parent / "data.json"

    if not json_path.exists():
        return "Файл не найден"

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        return "Ошибка чтения файла"

    try:
        with transaction.atomic():
            # Студенты
            for s in data.get('students', []):
                Student.objects.update_or_create(
                    id=s['id'],
                    defaults={'full_name': s['full_name'], 'email': s['email']}
                )

            # Курсы
            for c in data.get('courses', []):
                Course.objects.update_or_create(
                    id=c['id'],
                    defaults={'title': c['title'], 'code': c['code']}
                )

            # Записи на курсы (ManyToMany)
            enrolls = {}
            for e in data.get('course_enrollments', []):
                enrolls.setdefault(e['course_id'], []).append(e['student_id'])

            for course_id, student_ids in enrolls.items():
                try:
                    course = Course.objects.get(id=course_id)
                    current = set(course.students.values_list('id', flat=True))
                    new = set(student_ids)
                    if new - current:
                        course.students.add(*list(new - current))
                    if current - new:
                        course.students.remove(*list(current - new))
                except Course.DoesNotExist:
                    continue

            # Задания
            for a in data.get('assignments', []):
                try:
                    course = Course.objects.get(id=a['course_id'])
                    Assignment.objects.update_or_create(
                        id=a['id'],
                        defaults={
                            'title': a['title'],
                            'description': a.get('description', ''),
                            'course': course,
                            'due_date': a['due_date']
                        }
                    )
                except Course.DoesNotExist:
                    continue

            # Сданные работы
            for sub in data.get('submissions', []):
                try:
                    student = Student.objects.get(id=sub['student_id'])
                    assignment = Assignment.objects.get(id=sub['assignment_id'])

                    date = sub['submitted_at']
                    if 'T' in date:
                        date = date.split('T')[0]

                    Submission.objects.update_or_create(
                        id=sub['id'],
                        defaults={
                            'student': student,
                            'assignment': assignment,
                            'file_path': sub['file_path'],
                            'submitted_at': date
                        }
                    )
                except (Student.DoesNotExist, Assignment.DoesNotExist):
                    continue

            return "OK"

    except Exception as e:
        return f"Ошибка: {str(e)}"

