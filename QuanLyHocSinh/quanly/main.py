import flask_login
from flask import render_template, request, redirect, url_for
from quanly import app, utils, login, controllers
from flask_login import login_user, logout_user
from quanly.models import UserRole

app.add_url_rule('/', 'index', controllers.index)
app.add_url_rule('/login', 'login', controllers.login_my_user, methods=['get', 'post'])
app.add_url_rule('/logout', 'logout', controllers.logout_my_user)
app.add_url_rule('/employee', 'employee', controllers.employee)
app.add_url_rule('/teacher', 'teacher', controllers.teacher_display)
app.add_url_rule('/tiep-nhan-hoc-sinh', 'add-student', controllers.add_student, methods=['get', 'post'])
app.add_url_rule('/them-hoc-sinh-vao-lop', 'add-student-to-class', controllers.make_class_list, methods=['get', 'post'])
app.add_url_rule('/danh-sach-hoc-sinh', 'list-student', controllers.load_list_student)
app.add_url_rule('/xem-diem/mon-hoc/<int:subject_id>/hoc-ky/<int:semester_id>', 'mark-display', controllers.mark_display, methods=['get', 'post'])
app.add_url_rule('/nhap-diem/mon-hoc/<int:subject_id>/hoc-sinh/<int:student_id>', 'input-mark', controllers.input_mark, methods=['get', 'post'])
app.add_url_rule('/login-admin', 'admin-login', controllers.admin_login, methods=['get', 'post'])
app.add_url_rule('/cap-nhat-thong-tin-hoc-sinh/<int:student_id>', 'update-info', controllers.update_info_student, methods=['get', 'post'])
app.add_url_rule('/diem-trung-binh', 'mark-average', controllers.mark_average)

@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


if __name__ == '__main__':
    from quanly.admin import *

    app.run(debug=True)