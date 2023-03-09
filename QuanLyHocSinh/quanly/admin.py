from flask import redirect
from flask_login import current_user, logout_user

from quanly import app, db
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from quanly.models import Employee, Teacher, User, UserRole, Class_room, Grade, Subject, School_year

class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class AuthenticatedBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

class EmployeeView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['name']
    column_labels ={
        'name': 'Họ và tên',
        'day_of_birth': 'Ngày sinh',
        'gender': 'Giới tính',
        'address': 'Địa chỉ',
        'email': 'email'
    }

class TeacherView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['name']
    column_labels = {
        'name': 'Họ và tên',
        'gender': 'Giới tính',
        'day_of_birth': 'Ngày sinh',
        'address': 'Địa chỉ',
        'email': 'email'
    }

class UserView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['username']
    column_labels = {
        'username': 'Tên đăng nhập',
        'password': 'Mật khẩu',
        'avatar': 'Ảnh đại diện'
    }

class ClassView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['name']
    column_labels = {
        'id': 'Mã lớp',
        'name': 'Tên lớp',
        'quantity': 'Số lượng',
        'school_year': 'Năm học',
        'grade': 'Khối'
    }

class GradeView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['name']
    column_labels = {
        'id': 'Mã khối',
        'name': 'Tên khối'
    }

class SubjectView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['name']
    column_labels = {
        'id': 'Mã môn học',
        'name': 'Tên môn học'
}

class LogoutView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        logout_user()

        return redirect('/')

class NamHocView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['name']
    column_labels = {
        'id': 'Mã năm học',
        'name': 'Năm học'
    }

admin = Admin(app=app, name="Quản lý", template_mode='bootstrap4')

admin.add_view(AuthenticatedModelView(User, db.session, name='Người dùng'))
admin.add_view(EmployeeView(Employee, db.session, name='Nhân viên'))
admin.add_view(TeacherView(Teacher, db.session, name='Giáo viên'))
admin.add_view(SubjectView(Subject, db.session, name='Môn học'))
admin.add_view(ClassView(Class_room, db.session, name='Lớp học'))
admin.add_view(GradeView(Grade, db.session, name='Khối'))
admin.add_view(NamHocView(School_year, db.session, name='Năm học'))
admin.add_view(LogoutView(name='Đăng xuất'))
