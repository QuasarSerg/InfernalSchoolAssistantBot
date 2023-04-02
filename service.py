import session_parameters as sp
import datetime
import school_api
import model


def init_session_parameters():
    sp.CURRENT_USER = get_current_user()
    sp.STUDENTS = get_students()
    sp.SUBJECTS = get_subjects()


def get_current_user():
    context_resp = school_api.get_me_context()

    try:
        school_id = context_resp.get('schools')[0].get('id')
        name = context_resp.get('schools')[0].get('name')
        school = model.School(school_id, name)

        edu_group_id = context_resp['eduGroups'][0].get('id')
        edu_group_id_str = context_resp['eduGroups'][0].get('id_str')
        edu_group = model.EduGroup(edu_group_id, edu_group_id_str)

        user = model.User(context_resp.get('userId'),
                          context_resp.get('personId'),
                          context_resp.get('shortName'),
                          school,
                          edu_group)
        return user
    except Exception as e:
        print(e)


def get_students():
    students_resp = school_api.get_students(sp.CURRENT_USER.edu_group.edu_group_id)

    students = []
    for student in students_resp:
        student = model.Student(student.get('id'), student.get('userId'), student.get('shortName'), student.get('sex'))
        students.append(student)

    return students


def get_subjects():
    subjects_resp = school_api.get_subjects(sp.CURRENT_USER.edu_group.edu_group_id)

    subjects = []
    for subj in subjects_resp:
        subject = model.Subject(subj.get('id'), subj.get('name'), subj.get('knowledgeArea'))
        subjects.append(subject)

    return subjects


def get_homeworks_10_days():
    days = 10
    start_date = datetime.datetime.today()
    end_date = start_date + datetime.timedelta(days)
    school = sp.CURRENT_USER.school.school_id

    homeworks = school_api.get_homeworks(start_date, end_date, school)

    return get_homework_message(start_date, end_date, homeworks)


def get_homework_tomorrow():
    school = sp.CURRENT_USER.school.school_id
    start_date = datetime.datetime.today()
    end_date = start_date

    homeworks = school_api.get_homeworks(start_date, end_date, school)

    return get_homework_message(start_date, end_date, homeworks)


def get_homework_message(start_date, end_date, homeworks):
    title = sp.ICON_BOOKS + ' Домашнее задание на период ' \
                            '' + start_date.strftime('%d.%m.%Y') + ' - ' + end_date.strftime('%d.%m.%Y') + ': \n\n'
    homeworks_list = []
    for subject in homeworks.get('subjects'):
        work = list(filter(lambda w: w.get('subjectId') == subject.get('id'), homeworks.get('works'))).__getitem__(0)
        homeworks_list.append('\t' + sp.ICON_SMALL_BLUE_DIAMOND + ' [' + subject.get('name') + '] ' + work.get('text'))
    homeworks_message = '\n'.join(homeworks_list)

    return title + homeworks_message


def get_grades_in_3_days():
    days = 2
    end_date = datetime.datetime.today()
    start_date = end_date - datetime.timedelta(days)

    period = start_date.strftime('%d.%m.%Y') + ' - ' + end_date.strftime('%d.%m.%Y')
    title = sp.ICON_GRADUATION_CAP + ' Оценки за период ' + period + ': \n\n'

    grades_list = []
    lessons = school_api.get_lessons(start_date, end_date, sp.CURRENT_USER.edu_group.edu_group_id)
    marks = school_api.get_lessons_marks(lessons)
    for mark in marks:
        date_subject = mark.date[0:10] + ' [' + mark.lesson.subject.name + ']'
        grade = date_subject + ' ' + mark.student.short_name + ' - ' + mark.value + get_mark_icon(mark.value)
        grades_list.append(grade)
    grades_list.sort()
    grades = '\n'.join(grades_list)

    return title + grades


def get_person_grades_in_10_days():
    days = 10
    end_date = datetime.datetime.today()
    start_date = end_date - datetime.timedelta(days)

    period = start_date.strftime('%d.%m.%Y') + ' - ' + end_date.strftime('%d.%m.%Y')
    title = sp.ICON_GRADUATION_CAP + ' Оценки ученика ' + sp.CURRENT_USER.short_name + ' за период ' + period + ': \n\n'

    marks = school_api.get_persons_schools_marks(start_date, end_date, sp.CURRENT_USER.person_id,
                                                 sp.CURRENT_USER.school.school_id)
    lessons_ids = list(map(lambda m: m.get('lesson_str'), marks))
    lessons = school_api.get_lessons_many(lessons_ids)

    grades_list = []
    for mark in marks:
        lesson = list(filter(lambda l: l.get('id_str') == mark.get('lesson_str'), lessons)).__getitem__(0)
        student = list(filter(lambda s: s.student_id == mark.get('person'), sp.STUDENTS)).__getitem__(0)

        mark_icon = get_mark_icon(mark.get('value'))
        date_subject = mark.get('date')[0:10] + ' [' + lesson.get('subject').get('name') + ']'
        grade = '\t' + date_subject + ' ' + lesson.get('title')[0:70] + ' - ' + mark.get('value') + mark_icon
        grades_list.append(grade)
    grades_list.sort()
    grades = '\n'.join(grades_list)

    return title + grades


def get_mark_icon(value):
    value = str(value)
    if value.startswith('5'):
        icon = sp.ICON_FIRST_PLACE_MEDAL
    elif value.startswith('4'):
        icon = sp.ICON_SECOND_PLACE_MEDAL
    elif value.startswith('3'):
        icon = sp.ICON_THIRD_PLACE_MEDAL
    elif value.startswith('ЗЧ'):
        icon = sp.ICON_WHITE_HEAVY_CHECK_MARK
    else:
        icon = sp.ICON_DOWN_POINTING_RED_TRIANGLE

    return icon
