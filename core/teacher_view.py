#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from core.models import *

def check_classes():
    #查看班级
    classes_obj = Session.query(Classes).all()
    for i in classes_obj:
        print(i)
        for l in i.student:
            print(l)


def check_student():
    #查看学生
    student_onj = Session.query(Student).all()
    for i in student_onj:
        print('%s 班级:'%i,end='')
        for l in i.classes:
            print(l,end=' ')
        print()


def check_record():
    #查看上课记录和成绩
    record_obj = Session.query(Record).all()
    for i in record_obj:
        print(i)


def create_classes():
    #创建班级
    name = input('请输入名字:').strip()
    try:
        if name:
            classes_obj = Classes(name=name)
            Session.add(classes_obj)
            Session.commit()
            print('创建成功')
        else:
            print('不能为空')
    except sqlalchemy.exc.IntegrityError:
        print('创建失败,班级名重复')


def join_classes():
    #加入班级
    classes_name = input('请输入班级:').strip()
    student_qq = input('请输入qq:').strip()
    classes_obj = Session.query(Classes).filter(Classes.name==classes_name).first()
    student_obj = Session.query(Student).filter(Student.qq==student_qq).first()
    if classes_obj and student_obj:
        classes_obj.student.append(student_obj)
        Session.add_all([classes_obj])
        Session.commit()
        print('添加成功')
    else:
        print('输入错误')


def create_record():
    #创建学习记录
    course = input('请输入第几周:')
    classes = input('请输入班级名:')
    student = input('请输入学生qq:')
    try:
        if course.isdigit() and classes and student.isdigit():
            classes_obj = Session.query(Classes).filter(Classes.name==classes).first()
            student_obj = Session.query(Student).filter(Student.qq==student).first()
            record_obj = Record(course_week=int(course),classes_id=classes_obj.id,student_id=student_obj.id)
            Session.add(record_obj)
            Session.commit()
            print('创建成功')
        else:
            print('输入错误')
    except Exception:
        print('输入错误')


def alter_score():
    #修改成绩
    classes = input('请输入班级名:')
    student = input('请输入学生qq:')
    course = input('请输入第几周:')
    if classes and student.isdigit() and course.isdigit():
        classes_obj = Session.query(Classes).filter(Classes.name == classes).first()
        student_obj = Session.query(Student).filter(Student.qq == student).first()
        record_obj = \
            Session.query(Record).filter\
                (Record.course_week==int(course)).filter\
                (Record.student_id==student_obj.id).filter(Record.classes_id==classes_obj.id).first()
        if record_obj.homework == 'no':
            print('没有提交作业')
            return
        score = input('请输入分数:')
        if score.isdigit():
            record_obj.score = int(score)
            Session.commit()
            print('修改成功')
        else:
            print('输入错误,必须是数字')


def main():
    handle_choice = {'1': check_classes, '2': check_student, '3': check_record
        , '4': create_classes, '5': join_classes, '6': create_record, '7': alter_score}
    while True:
        handle = input('1.查看班级\n2.查看学生\n'
                       '3.查看上课记录和成绩\n4.创建班级\n5.加入班级\n6.创建上课记录\n7.修改成绩\n-->')
        if handle in handle_choice:
            handle_choice[handle]()
main()