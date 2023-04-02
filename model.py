class School:
    def __init__(self, school_id, name):
        self.school_id = school_id
        self.name = name


class EduGroup:
    def __init__(self, edu_group_id, edu_group_id_str):
        self.edu_group_id = edu_group_id
        self.edu_group_id_str = edu_group_id_str


class User:
    def __init__(self, user_id=None, person_id=None, short_name=None, school=None, edu_group=None):
        self.user_id = user_id
        self.person_id = person_id
        self.short_name = short_name
        self.school = school
        self.edu_group = edu_group


class Student:
    def __init__(self, student_id=None, user_id=None, short_name=None, sex=None):
        self.student_id = student_id
        self.user_id = user_id
        self.short_name = short_name
        self.sex = sex


class Subject:
    def __init__(self, subject_id=None, name=None, knowledge_area=None):
        self.subject_id = subject_id
        self.name = name
        self.knowledge_area = knowledge_area


class Lesson:
    def __init__(self, lesson_id=None, lesson_id_str=None, title=None, date=None, subject=Subject):
        self.lesson_id = lesson_id
        self.lesson_id_str = lesson_id_str
        self.title = title
        self.date = date
        self.subject = subject


class Mark:
    def __init__(self, date=None, lesson=Lesson, student=Student, value=None):
        self.date = date
        self.lesson = lesson
        self.student = student
        self.value = value
