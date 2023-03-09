from functools import wraps

import flask_login
from flask import render_template, request, redirect, url_for
from quanly import app, utils, login
from flask_login import login_user, logout_user, current_user, login_manager, login_required
from quanly.decorator import annonynous_user
from quanly.models import UserRole, Gender


def index():
    logout_user()
    return render_template('index.html')

@annonynous_user
def login_my_user():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = utils.check_login(username=username, password=password)
        if user and user.user_role == UserRole.TEACHER:
            login_user(user=user)
            teacher = utils.get_teacher_by_user_id(user.id)
            # return render_template("teacher.html", user=user, teacher=teacher)
            return redirect('/teacher')
        elif user and user.user_role == UserRole.EMPLOYEE:
            login_user(user=user)
            # return render_template("employee.html", user=user)
            return redirect('/employee')
        else:
            err_msg = 'Tài khoản hoặc mật khẩu không chính xác'

    return render_template('login.html', err_msg=err_msg)

def admin_login():
    msg = ''
    if request.method.__eq__('POST'):
        username = request.form['username']
        password = request.form['password']
        user  = utils.check_login(username=username, password=password)
        if user and user.user_role == UserRole.ADMIN:
            login_user(user=user)
            return redirect('/admin/')
        else:
            msg = 'Tài khoản hoặc mật khẩu không chính xác'
    return render_template('admin-login.html', msg=msg)

def logout_my_user():
    logout_user()
    return redirect('/')

# nghiệp vụ nhân viên
@login_required
def employee():
    return render_template('employee.html')

@login_required
def teacher_display():
    subjects = utils.get_subject()
    return render_template('teacher.html', subjects=subjects)

@login_required
def add_student():
    msg = ''
    flag = 0 # để hiện thị message box
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        sex = request.form.get('gender')
        address = request.form.get('address')
        phone = request.form.get('phone')
        email = request.form.get('email')
        date_of_birth = request.form.get('date_of_birth')
        gender = None

        if sex.__eq__('male'):
            gender = Gender.MALE
        else:
            gender = Gender.FEMALE
        try:
            if utils.check_age(date_of_birth=date_of_birth):
                utils.add_or_update_student(name=name,
                                            gender=gender,
                                            date_of_birth=date_of_birth,
                                            address=address,
                                            phone=phone,
                                            email=email)
                msg = 'Tiếp nhận học sinh thành công'
            else:
                msg = 'Chỉ tuyển học sinh từ 15 đến 20 tuổi'
                flag = 1
        except Exception as e:
            msg = 'Lỗi hệ thống ' + str(e)
            flag = 1

    return render_template('add-student.html', msg=msg, flag=flag)

@login_required
def make_class_list():
    grade_list = utils.get_list_grade()
    class_room_list = utils.get_list_class_room()
    students = utils.get_student_not_class()
    class_school_year = utils.get_class_school_year()

    msg = ''
    flag = 0
    if request.method.__eq__('POST'):
        classes = request.form.get('classes')
        student = request.form.get('student')
        try:
            if utils.check_size_class(classes):
                utils.add_student_class(classes, student)
                class_room_name = utils.get_class_room_by_id(classes)
                student_name = utils.get_student_by_id(student)
                utils.quantity_class_by_id(classes)
                msg = 'Thêm học sinh ' + student_name.name + ' vào lớp ' + class_room_name.name + 'thành công'
            else:
                msg = 'Thêm học vào lớp thất bại'
                flag = 1
        except Exception as e:
            msg = 'Lỗi hệ thống ' + str(e)
            flag = 1

    return render_template('make-class-list.html',
                           grade_list=grade_list,
                           class_room_list=class_room_list,
                           students=students,
                           msg=msg,
                           flag=flag,
                           class_school_year=class_school_year)

@login_required
def load_list_student():
    # lấy current user hiện tại,
    cur = current_user.id
    # # từ current user lấy teacher thông qua user_id làm khòa ngoại
    user_teacher = utils.get_teacher_by_user_id(cur)

    students = utils.get_student_by_class_id(user_teacher.class_id)
    class_room = utils.get_class_room_by_id(user_teacher.class_id)

    return render_template('list-student.html',
                           students=students,
                           class_room=class_room,
                           Gender=Gender,
                           cur=cur,
                           user_teacher=user_teacher)

@login_required
def mark_display(subject_id, semester_id):
    cur = current_user.id
    # # từ current user lấy teacher thông qua user_id làm khòa ngoại
    user_teacher = utils.get_teacher_by_user_id(cur)
    semester = utils.get_semester()
    semester_name = utils.get_semester_by_id(semester_id)
    school_year_name = utils.get_school_year_by_id(semester_name.id)

    students = utils.get_student_by_class_id(user_teacher.class_id)
    marks_15 = utils.get_subject_mark_student_15_minute(subject_id, user_teacher.class_id, semester_id=semester_id)
    marks_45 = utils.get_subject_mark_student_45_minute(subject_id, user_teacher.class_id, semester_id=semester_id)
    marks_final = utils.get_subject_mark_student_final(subject_id, user_teacher.class_id, semester_id=semester_id)
    subject = utils.get_subject_by_id(subject_id)


    return render_template("mark-display.html",
                           students=students,
                           marks_15=marks_15,
                           marks_45=marks_45,
                           marks_final=marks_final,
                           subject=subject,
                           semester=semester,
                           semester_name=semester_name,
                           school_year_name=school_year_name)

@login_required
def input_mark(subject_id, student_id):
    subject = utils.get_subject_by_id(subject_id)
    type_mark = utils.get_type_mark()
    semester = utils.get_semester()
    student = utils.get_student_by_id(student_id)

    msg = ''
    flag = 0
    if request.method.__eq__('POST'):
        try:
            mark = request.form.get('mark')
            typemark_id = request.form.get('type_mark')
            semester_id = request.form.get('semester')

            if float(mark) < 0 or float(mark) > 10:
                msg = 'Điểm số phải nằm trong khoảng 0 đến 10'
                flag = 1
            else:
                if utils.check_mark(subject_id=subject_id, student_id=student.id, type_mark_id=int(typemark_id)):
                    utils.add_mark_student(mark=mark,
                                       student_id=student_id,
                                       subject_id=subject_id,
                                       type_mark_id=typemark_id,
                                       semester_id=semester_id)
                    msg = 'Nhập điểm phút thành công'
                else:
                    msg = 'Đã đủ cột điểm'
                    flag =2
        except Exception as e:
            msg = 'Lỗi' + str(e)
            flag = 1
    return render_template('input-mark.html',
                           subject=subject,
                           type_mark=type_mark,
                           semester=semester,
                           student=student,
                           msg=msg,
                           flag=flag)

def update_info_student(student_id):
    msg = ''
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        sex = request.form.get('gender')
        address = request.form.get('address')
        phone = request.form.get('phone')
        email = request.form.get('email')
        date_of_birth = request.form.get('date_of_birth')
        gender = None

        if sex.__eq__('male'):
            gender = Gender.MALE
        else:
            gender = Gender.FEMALE

        if utils.check_age(date_of_birth=date_of_birth):
            try:
                utils.update_info_student(student_id=student_id,
                                          name=name,
                                          date_of_birth=date_of_birth,
                                          gender=gender,
                                          phone=phone,
                                          address=address,
                                          email=email)
                return redirect(url_for('list-student'))
            except Exception as e:
                msg = 'Lỗi hệ thống' + str(e)
        else:
            msg = 'Độ tuổi không hợp lệ'

    return render_template('update-info-student.html', student=utils.get_student_by_id(id=student_id), gender=Gender,
                           msg=msg)

def mark_average():
    return render_template("mark-average.html")






