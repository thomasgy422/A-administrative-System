from datetime import datetime
from sqlalchemy.orm import backref
from tapes import db, login_manager, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import flask_login as login

users_courses = db.Table('users_courses',
                        db.Column('user_id', db.Integer,
                        db.ForeignKey('user.id')),
                        db.Column('courses_id', db.Integer,
                        db.ForeignKey('courses.id'))
)

users_teams = db.Table('users_teams',
                        db.Column('user_id', db.Integer,
                        db.ForeignKey('user.id')),
                        db.Column('teams_id', db.Integer,
                        db.ForeignKey('teams.id'))
)

users_taqresponses = db.Table('users_taqresponses',
                        db.Column('user_id', db.Integer,
                        db.ForeignKey('user.id')),
                        db.Column('taq_responses_id', db.Integer,
                        db.ForeignKey('ta_qresponse.id'))
)


class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    teams = db.relationship('Teams', backref='course', lazy='dynamic')

    def __repr__(self):
        return f"Course({self.id}, {self.title})"

class Teams(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))

    def __repr__(self):
        return f"Team({self.id}, {self.title}, {self.course_id})"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128)) # can we delete alongside the functions below?
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_module_leader = db.Column(db.Boolean, nullable=False, default=False)
    courses = db.relationship('Courses', secondary=users_courses, backref=db.backref('users'), lazy='dynamic')
    teams = db.relationship('Teams', secondary=users_teams, backref=db.backref('users'), lazy='dynamic')
    taq_responses = db.relationship('TAQresponse', secondary=users_taqresponses, backref=db.backref('users'), lazy='dynamic')

    def __repr__(self):
        return f"User({self.id}, {self.username}, {self.email})"

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash, password)

    def remove_team(self, team):
        self.teams.remove(team)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class PAQresponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    targetUser = db.Column(db.String(120), nullable=False)
    team = db.Column(db.String(120), nullable=False)
    q1 = db.Column(db.Integer, nullable=False)
    q2 = db.Column(db.Integer, nullable=False)

class TAQresponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), db.ForeignKey('user.username'))
    courseID = db.Column(db.Integer, db.ForeignKey('courses.id'))
    experienced = db.Column(db.Integer, nullable=False, default=False)
    degree = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"({self.id}, {self.username}, {self.experienced}, {self.degree})"

class RhysTestTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    experienced = db.Column(db.Boolean, nullable=False, default=False)
    degree = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"({self.id}, {self.name}, {self.degree})"

class Reportissue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    course = db.Column(db.String(120), nullable=False)
    team = db.Column(db.String(120), nullable=False)
    content = db.Column(db.String(255), nullable=False)

class EvalForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), db.ForeignKey('courses.title'))
    q1 = db.Column(db.Boolean, nullable=False)
    q2 = db.Column(db.Boolean, nullable=False)
    q3 = db.Column(db.Boolean, nullable=False)
    q4 = db.Column(db.Boolean, nullable=False)
    q5 = db.Column(db.Boolean, nullable=False)
    q6 = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"({self.id}, {self.title}, {self.q1}, {self.q2}, {self.q3}, {self.q4}, {self.q5}, {self.q6})"
