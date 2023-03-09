import hashlib
from datetime import datetime, date

from flask import session
from sqlalchemy import func

from quanly import app, db
from quanly.models import User, Teacher, Rules, Student, Grade, Class_room, Subject, School_year, Semester, Mark, \
    TypeMark


def check_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()

def get_user_by_id(user_id):
    return User.query.get(user_id)

# def get_teacher_by_user_id(id):
#     return Teacher.query.get(id)

def check_age(date_of_birth):
    if date_of_birth:
        year = datetime.strptime(date_of_birth, "%Y-%m-%d").year
        today = date.today()
        age = today.year - year
        rule = Rules.query.get(1)
        if age.__ge__(rule.min_age) and age.__le__(rule.max_age):
            return True

def check_size_class(class_id):
    c = Class_room.query.get(class_id)
    rules = Rules.query.get(c.rules_id)
    max_size = rules.class_size
    soluong = c.quantity
    if soluong <= max_size:
        return True

    return False

def check_mark(subject_id, student_id, type_mark_id):
    check = Mark.query.filter(Mark.student_id.__eq__(student_id))\
                    .filter(Mark.subject_id.__eq__(subject_id))\
                    .filter(Mark.type_mark_id.__eq__(type_mark_id))\
                    .count()

    if type_mark_id == 1:
        if check < 5:
            return True
    elif type_mark_id == 2:
        if check < 3:
            return True
    elif type_mark_id == 3:
        if check < 1:
            return True
    return False

def quantity_class_by_id(class_id):
    student = Student.query.filter(Student.class_id.__eq__(class_id)).count()
    c = Class_room.query.get(class_id)
    c.quantity = student
    db.session.commit()

def add_or_update_student(name, gender, date_of_birth, address, phone, email, **kwargs):
    student = Student(name=name, gender=gender,
                      date_of_birth=date_of_birth,
                      address=address,
                      phone=phone,
                      email=email)
    db.session.add(student)
    db.session.commit()

def add_student_class(class_id, student_id):
    student = get_student_by_id(student_id)
    student.class_id = class_id
    db.session.commit()

def add_mark_student(mark, student_id, subject_id, type_mark_id, semester_id=1):
    mark = Mark(mark=mark,
                student_id=student_id,
                subject_id=subject_id,
                semester_id=semester_id,
                type_mark_id=type_mark_id)
    db.session.add(mark)
    db.session.commit()

def get_type_mark():
    return TypeMark.query.all()

def get_semester():
    return Semester.query.all()

def get_list_grade():
    return Grade.query.all()

def get_list_class_room():
    return Class_room.query.all()

def get_student_by_id(id):
    return Student.query.get(id)

def get_student_not_class():
    return Student.query.filter(Student.class_id == None).all()

def get_class_room_by_id(class_id):
    return Class_room.query.get(class_id)

def get_student_by_class_id(class_id):
    return Student.query.filter(Student.class_id == class_id).all()

def get_teacher_by_id(id):
    return Teacher.query.get(id)

def get_teacher_by_user_id(user_id):
    return Teacher.query.filter(Teacher.user_id== user_id).first()

def get_subject():
    return Subject.query.all()

def get_subject_by_id(id):
    return Subject.query.get(id)

def get_semester():
    return Semester.query.all()

def get_semester_by_id(id):
    return Semester.query.get(id)

def get_school_year_by_id(id):
    return School_year.query.get(id)

def get_subject_mark_student_15_minute(subject_id, class_id, semester_id):
    query = Mark.query\
                    .join(Student, Mark.student_id == Student.id)\
                    .join(TypeMark, Mark.type_mark_id == TypeMark.id) \
                    .add_columns(Student.id, Student.name, Mark.mark, TypeMark.name, Student.class_id, Mark.subject_id,Mark.type_mark_id) \
                    .filter(Mark.subject_id == subject_id)\
                    .filter(Mark.type_mark_id == 1)\
                    .filter(Student.class_id == class_id)\
                    .filter(Mark.semester_id == semester_id)
    return query

def get_subject_mark_student_45_minute(subject_id, class_id, semester_id):
    query = Mark.query \
        .join(Student, Mark.student_id == Student.id) \
        .join(TypeMark, Mark.type_mark_id == TypeMark.id) \
        .add_columns(Student.id, Student.name, Mark.mark, TypeMark.name, Student.class_id, Mark.subject_id, Mark.type_mark_id) \
        .filter(Mark.subject_id == subject_id) \
        .filter(Mark.type_mark_id == 2) \
        .filter(Student.class_id == class_id) \
        .filter(Mark.semester_id == semester_id)
    return query

def get_subject_mark_student_final(subject_id, class_id, semester_id):
    query = Mark.query \
        .join(Student, Mark.student_id == Student.id) \
        .join(TypeMark, Mark.type_mark_id == TypeMark.id) \
        .add_columns(Student.id, Student.name, Mark.mark, TypeMark.name, Student.class_id, Mark.subject_id, Mark.type_mark_id) \
        .filter(Mark.subject_id == subject_id) \
        .filter(Mark.type_mark_id == 3) \
        .filter(Student.class_id == class_id) \
        .filter(Mark.semester_id == semester_id)
    return query

def get_class_school_year():
    join_query = Class_room.query\
                        .join(School_year, School_year.id == Class_room.school_year_id)

    return join_query

def update_info_student(student_id, name=None, date_of_birth=None, gender=None, phone=None, address=None, email=None):
    student = get_student_by_id(student_id)
    if name: student.name = name
    if date_of_birth: student.date_of_birth = date_of_birth
    if gender: student.gender = gender
    if phone: student.phone = phone
    if email: student.email = email
    if address: student.address = address

    db.session.add(student)
    db.session.commit()






