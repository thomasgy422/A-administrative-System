from operator import __irshift__
from tapes import db, app
from tapes.models import User
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import csv
from sqlalchemy import create_engine, Table, Column, Integer, MetaData

user_id= []
names = []
courses = []
students = []
leader = []

with open("class_list.csv", newline="") as csvfile:
    file = csv.reader(csvfile, delimiter=" ", quotechar='|')
    for row in file:
        full_name = ""
        id_found = False
        names_found = False
        is_student = False
        is_leader = False

        user_id= []
        names = []
        courses = []
        students = []
        leader = []
        

        for each_word in row:
            lower_word = each_word.lower()
            if id_found == False:
                if lower_word.isnumeric():
                    user_id.append(lower_word)
                    id_found = True
                    continue
                    
            if names_found == False:
                if lower_word[0:3] == "cmt":
                    names.append(full_name.strip())
                    names_found = True
                else:
                    full_name = full_name + lower_word + " "
                
            if id_found:
                if names_found:
                    if lower_word == "student":
                        students.append(lower_word)
                        is_student = True
                        for items in user_id:
                            insert_query = c21022750_mvp_database.insert()
                        for items in names:
                            print(items)
                        for items in courses:
                            print(items)
                        for items in leader:
                            print(items)






                    elif lower_word == "leader":
                        leader.append(lower_word)
                        is_leader = True
                    else:
                        courses.append(lower_word)

 
 