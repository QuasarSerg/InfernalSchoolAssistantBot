import json

from resources import config as cfg
import session_parameters as sp
import requests
import model

headers = {'Accept': 'application/json', "Access-Token": cfg.SCHOOL_API_ACCESS_TOKEN, "User-Agent": 'School-Agent'}

headers_patch = headers.copy()
headers_patch.__setitem__('Content-Type', 'application/json-patch+json')


def get_homeworks(start_date, end_date, school):
    params = {'startDate': start_date.strftime('%Y-%m-%d'), "endDate": end_date.strftime('%Y-%m-%d')}
    response = requests.get(f'{cfg.BASE_URL}/users/me/school/{school}/homeworks', headers=headers, params=params)

    return response.json()


def get_me_context():
    response = requests.get(f'{cfg.BASE_URL}/users/me/context', headers=headers)

    return response.json()


def get_students(edu_group):
    response = requests.get(f'{cfg.BASE_URL}/edu-groups/{edu_group}/students', headers=headers)

    return response.json()


def get_subjects(edu_group):
    response = requests.get(f'{cfg.BASE_URL}/edu-groups/{edu_group}/subjects', headers=headers)

    return response.json()


def get_lessons(start_date, end_date, group):
    start_date_f = start_date.strftime('%Y-%m-%d')
    end_date_f = end_date.strftime('%Y-%m-%d')
    response = requests.get(f'{cfg.BASE_URL}/edu-groups/{group}/lessons/{start_date_f}/{end_date_f}', headers=headers)

    lessons = []
    for les in response.json():
        subject = list(filter(lambda s: s.subject_id == les.get('subject').get('id'), sp.SUBJECTS)).__getitem__(0)
        lesson = model.Lesson(les.get('id'), les.get('id_str'), les.get('title'), les.get('date'), subject)
        lessons.append(lesson)

    return lessons


def get_lessons_marks(lessons):
    lessons_ids = list(map(lambda les: les.lesson_id, lessons))
    response = requests.post(f'{cfg.BASE_URL}/lessons/marks', headers=headers_patch, data=json.dumps(lessons_ids))

    marks = []
    for mark in response.json():
        cur_lesson = list(filter(lambda l: l.lesson_id_str == mark.get('lesson_str'), lessons)).__getitem__(0)
        cur_student = list(filter(lambda s: s.student_id == mark.get('person'), sp.STUDENTS)).__getitem__(0)
        mark = model.Mark(mark.get('date'), cur_lesson, cur_student, mark.get('value'))
        marks.append(mark)

    return marks


def get_persons_schools_marks(start_date, end_date, person, school):
    start_date_f = start_date.strftime('%Y-%m-%d')
    end_date_f = end_date.strftime('%Y-%m-%d')
    response = requests.get(f'{cfg.BASE_URL}/persons/{person}/schools/{school}/marks/{start_date_f}/{end_date_f}',
                            headers=headers)

    return response.json()


def get_lessons_many(lessons_ids):
    response = requests.post(f'{cfg.BASE_URL}/lessons/many', headers=headers_patch, data=json.dumps(lessons_ids))

    return response.json()
