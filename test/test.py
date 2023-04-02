import service


service.init_session_parameters()
homeworks = service.get_grades_in_3_days()
print(homeworks)
