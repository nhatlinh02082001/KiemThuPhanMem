from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, DateTime, Enum
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.strategy_options import defer
from datetime import datetime
from enum import Enum as UserEnum, unique

from werkzeug.routing import Rule

from quanly import app, db
from flask_login import UserMixin

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

class Gender(UserEnum):
    MALE = 1
    FEMALE = 2

class UserRole(UserEnum):
    ADMIN = 1
    TEACHER = 2
    EMPLOYEE = 3

class User(BaseModel, UserMixin):
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    avatar = Column(String(100))
    user_role = Column(Enum(UserRole), nullable=False)

    def __str__(self):
        return self.username

class School_year(BaseModel):
    name = Column(String(50), nullable=False)
    classes = relationship('Class_room', backref='school_year', lazy=True)
    semester = relationship('Semester', backref='school_year', lazy=True)

    def __str__(self):
        return self.name

class Semester(BaseModel):
    name = Column(String(50), nullable=False)
    year_id = Column(Integer, ForeignKey(School_year.id), nullable=False)

    def __str__(self):
        return self.name

class TypeMark(BaseModel):
    name = Column(String(50), nullable=False)

    def __str__(self):
        return self.name

class Subject(BaseModel):
    name = Column (String(50), nullable=False)

    def __str__(self):
        return self.name

class Mark(BaseModel):
    mark = Column(Float, default=0)
    student_id = Column(Integer, ForeignKey('student.id'), nullable=False, primary_key=True)
    subject_id = Column(Integer, ForeignKey(Subject.id), nullable=False, primary_key=True)
    semester_id = Column(Integer, ForeignKey(Semester.id), nullable=False, primary_key=True)
    type_mark_id = Column(Integer, ForeignKey(TypeMark.id), nullable=False, primary_key=True)


class Grade(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    classes = relationship('Class_room', backref='grade', lazy=False)

    def __str__(self):
        return self.name

class Class_room(BaseModel):
    name = Column(String(20), nullable=False)
    quantity = Column(Integer, default=0)
    students = relationship('Student', backref='Class_room', lazy=False)
    grade_id = Column(Integer, ForeignKey(Grade.id), nullable=False)
    school_year_id = Column(Integer, ForeignKey(School_year.id), nullable=False)
    rules_id = Column(Integer, ForeignKey('rules.id'), default=1)

    def __str__(self):
        return self.name

class Teacher(BaseModel):
    name = Column(String(50), nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    address = Column(String(100))
    email = Column(String(100))
    date_of_birth = Column(DateTime)
    class_id = Column(Integer, ForeignKey(Class_room.id))
    class_room = relationship('Class_room', backref='teacher', lazy=False, uselist=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    user = relationship('User', backref='teacher', uselist=False)

    def __str__(self):
        return self.name

class Employee(BaseModel):
    name = Column(String(50), nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    address = Column(String(100))
    email = Column(String(100))
    date_of_birth = Column(Integer)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)

    def __str__(self):
        return self.name

class Rules(BaseModel):
    class_size = Column(Integer)
    max_age = Column(Integer)
    min_age = Column(Integer)

    def __str__(self):
        return self.id

class Student(BaseModel):
    name = Column(String(50), nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    email = Column(String(50))
    date_of_birth = Column(DateTime)
    phone = Column(String(11))
    address = Column(String(100))
    class_id = Column(Integer, ForeignKey(Class_room.id), default=None)
    rule_id = Column(Integer, ForeignKey(Rules.id), default=1)

    def __str__(self):
        return self.name

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # import hashlib
        #
        # password = str(hashlib.md5('1'.encode('utf-8')).hexdigest())
        # u1 = User(username='admin', password=password, user_role=UserRole.ADMIN,
        #           avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg')
        # u2 = User(username='vy', password=password, user_role=UserRole.TEACHER,
        #           avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg')
        # u3 = User(username='linh', password=password, user_role=UserRole.EMPLOYEE,
        #           avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg')
        #
        # db.session.add_all([u1, u2, u3])
        # db.session.commit()
























































