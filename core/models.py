#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlalchemy
from sqlalchemy import create_engine,UniqueConstraint,Index,func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,ForeignKey,Table
from sqlalchemy.orm import relationship,sessionmaker
from conf import setting

engine = create_engine(setting.DB_PATH)
Base = declarative_base()
#建立班级表与学生表多对多关联
classes_m2m_student = Table('classes_m2m_student', Base.metadata,
                        Column('classes_id',Integer,ForeignKey('classes.id')),
                        Column('student_id',Integer,ForeignKey('student.id')),
                        )


class Classes(Base):
    #班级表
    __tablename__ = 'classes'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    id = Column(Integer, primary_key=True)
    name = Column(String(32),unique=True)
    student = relationship('Student', secondary=classes_m2m_student, backref='classes')

    def __repr__(self):
        return self.name

class Student(Base):
    #学生表
    __tablename__ = 'student'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    password = Column(String(32))
    qq = Column(String(16),unique=True)

    def __repr__(self):
        return 'name:%s qq:%s'%(self.name,self.qq)


class Record(Base):
    #学习记录表
    __tablename__ = 'record'
    #添加联合唯一,声明字符集(utf8)
    __table_args__ = (UniqueConstraint('course_week', 'student_id','classes_id', name='uix_id_name'),
        Index('ix_id_name', 'course_week', 'student_id','classes_id'),{
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
    })

    id = Column(Integer, primary_key=True)
    course_week = Column(Integer)
    student_id = Column(Integer, ForeignKey('student.id'))
    classes_id = Column(Integer, ForeignKey('classes.id'))
    homework = Column(String(16),default='no')
    score = Column(Integer,default=0)
    student = relationship("Student", backref="record")
    classes = relationship("Classes", backref="record")

    def __repr__(self):
        return 'week:%s student:%s classes:%s homework:%s score:%s'%\
               (self.course_week,self.student.name,self.classes.name,self.homework,self.score)


Base.metadata.create_all(engine)
Session_class = sessionmaker(bind=engine)
Session = Session_class()