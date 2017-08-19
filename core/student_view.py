#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from core.models import *

def login():
    #学生登录
    qq = input('请输入qq:')
    password = input('请输入密码:')
    if qq.isdigit():
        student_onj = Session.query(Student).filter(Student.qq==int(qq)).filter(Student.password==password).first()
        if student_onj:
            return student_onj
        else:
            print('不存在')

def register():
    #学生注册
    name = input('请输入名字:').strip()
    password = input('请输入密码:').strip()
    qq = input('请输入qq:').strip()
    try:
        if name and password and qq.isdigit():
            student_obj = Student(name=name,password=password,qq=qq)
            Session.add(student_obj)
            Session.commit()
            print('注册成功')
        else:
            print('输入错误')
    except sqlalchemy.exc.IntegrityError:
        print('注册失败qq号重复')


def homework(student):
    #提交作业
    classes = input('请输入班级名')
    course = input('请输入第几周')
    if classes and course.isdigit():
        classes_obj = Session.query(Classes).filter(Classes.name==classes).first()
        record_obj = Session.query(Record).filter\
            (Record.classes_id==classes_obj.id,Record.course_week==int(course),Record.student_id==student.id).first()
        record_obj.homework = 'yes'
        Session.commit()
        print('提交成功')
    else:
        print('输入错误')


def score(student):
    #查看成绩
    classes = input('请输入班级')
    if classes:
        classes_obj = Session.query(Classes).filter(Classes.name == classes).first()
        record_obj = Session.query(Record).filter(Record.student_id==student.id,Record.classes_id==classes_obj.id).all()
        for i in record_obj:
            print('第%s周成绩:%s'%(i.course_week,i.score))
        record_obj = Session.query(Record.student_id).filter\
            (Record.classes_id==classes_obj.id).group_by(Record.student_id).order_by(func.sum(Record.score).desc()).all()
        print('在班上排名:%s'%(record_obj.index((student.id,))+1))
    else:
        print('输入不能为空')


def operation(student):
    handle_choice = {'1': homework, '2': score}
    while True:
        handle = input('1.提交作业\n2.查看成绩\n-->')
        if handle in handle_choice:
            handle_choice[handle](student)


def main():
    while True:
        login_or_register = input('1.login\n2.register\n-->')
        if login_or_register == '1':
            student = login()
            if student:
                operation(student)
        elif login_or_register == '2':
            register()
        else:
            print('输入错误')


main()