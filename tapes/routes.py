from flask import Flask, render_template, url_for, request, flash, redirect
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.sql.schema import MetaData
from sqlalchemy.sql import text
from sqlalchemy.orm import load_only
from tapes.forms import LoginForm, RegistrationForm, PeerEvalForm, TaquestionnaireForm
from tapes import app, db
from tapes.models import Courses, EvalForm, User, Teams, PAQresponse, Reportissue
import csv
from io import StringIO
from flask import Response, stream_with_context
from tapes.models import User, RhysTestTable, Courses, TAQresponse, users_teams, Teams, PAQresponse, Reportissue, users_courses

app.secret_key = "fda23fc6a02f3e96325173c45746b9b1df4e591de873d3f1"

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()
        flash("Registration successful")
        return redirect(url_for("home"))

    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash("Login successful!")
            return redirect(url_for("home"))
        flash("Invalid email address or password.")

        return render_template("login.html", form=form)

    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash("Logout successful")
    return redirect(url_for("home"))


@app.route("/allocation")
def allocation():
    user = current_user
    return render_template("allocation.html", user=user)


@app.route("/question_rec")
def question_rec():
    form = LoginForm()
    return render_template("question_rec.html", form=form)


@app.route("/question_alloc")
def question_alloc():
    form = LoginForm()
    return render_template("question_alloc.html", form=form)


@app.route("/team_allo_questionnaire_setup")
def team_allo_questionnaire_setup():
    return render_template("team_allo_question_setup.html")


@app.route("/allocation_course_select")
def allocation_course_select():
    user = current_user
    return render_template("allocation_course_select.html", user=user)


@app.route("/team_allo_module_main/<course>")
def team_allo_module_main(course):
    #Checks to see if there are already teams for the current module
    CourseObject = Courses.query.filter_by(title=course).first()
    teamQuery = Teams.query.filter_by(course_id=CourseObject.id).all()
    teamCheck = len(teamQuery)
    return render_template("team_allo_module_main.html", course=course, teamCheck=teamCheck)


@app.route("/team_allo_module_main/<course>/<teamCheck>/deleteteams")
def delete_teams(course, teamCheck):
    CourseObject = Courses.query.filter_by(title=course).first()
    if teamCheck != 0:
        ListOfStudents = User.query.filter(User.courses.any(title=course)).filter(User.is_module_leader == 0).all()
        for student in ListOfStudents:
            for team in student.teams:
                if team.course_id == CourseObject.id:
                    User.remove_team(student, team)
                else:
                    continue
        Teams.query.filter_by(course_id = CourseObject.id).delete()
        db.session.commit()
        flash("Teams have been deleted!")
        return redirect(f"/team_allo_module_main/{CourseObject.title}")
    else:
        return render_template("team_allo_module_main.html", course=course, teamCheck=teamCheck)


@app.route("/team_allocation/<course>", methods=["GET", "POST"])
def team_allocation_setup(course):
    if request.method == "POST":
        size = request.form["size"]
        priority = request.form["priority"]
        return redirect(
            url_for("team_allo_results", size=size, priority=priority, course=course)
        )
    else:
        return render_template("team_allocation.html", course=course)


@app.route("/team_allo_results/<course>/<size>/<priority>", methods=["GET", "POST"])
def team_allo_results(course, size, priority):
  #Access students from database
  students = User.query.filter(User.courses.any(title=course)).filter(User.is_module_leader == 0).all()
  #Converts received size variable from string to int
  size = int(size)
  #Calculates the number of teams needed based off students in database and the inputted size selection
  NumOfTeams = (len(students))//size
  #Initialises lists
  ListOfTeams = []
  ListOfKeys = []
  #Creates list of groups based off priority
  if priority == "experience":
    HasExp = User.query.filter(User.courses.any(title=course)).filter(User.taq_responses.any(experienced=1)).filter(User.is_module_leader == 0).all()
    NoExp = User.query.filter(User.courses.any(title=course)).filter(User.taq_responses.any(experienced=0)).filter(User.is_module_leader == 0).all()
    PreListOfGroups = []
    PreListOfGroups.append(HasExp)
    PreListOfGroups.append(NoExp)
  elif priority == "degree":
    #Changed (degree="BSc") to int values
    BSc = User.query.filter(User.courses.any(title=course)).filter(User.taq_responses.any(degree="BSc")).filter(User.is_module_leader == 0).all()
    BA = User.query.filter(User.courses.any(title=course)).filter(User.taq_responses.any(degree="BA")).filter(User.is_module_leader == 0).all()
    BEng = User.query.filter(User.courses.any(title=course)).filter(User.taq_responses.any(degree="BEng")).filter(User.is_module_leader == 0).all()
    LLB = User.query.filter(User.courses.any(title=course)).filter(User.taq_responses.any(degree="LLB")).filter(User.is_module_leader == 0).all()
    PreListOfGroups = []
    PreListOfGroups.append(BSc)
    PreListOfGroups.append(BA)
    PreListOfGroups.append(BEng)
    PreListOfGroups.append(LLB)
  elif priority == "age":
    #18-24 = 0, 25-34 = 1, 35-54 = 2, 55-64 = 3, 65+ = 4, NoSay = 5
    EighteenTo24 = User.query.filter(User.courses.any(title=course)).filter(User.taq_responses.any(age=0)).filter(User.is_module_leader == 0).all()
    TwentyFiveTo34 = User.query.filter(User.courses.any(title=course)).filter(User.taq_responses.any(age=1)).filter(User.is_module_leader == 0).all()
    ThirtyFiveTo54 = User.query.filter(User.courses.any(title=course)).filter(User.taq_responses.any(age=2)).filter(User.is_module_leader == 0).all()
    FiftyFiveTo64 = User.query.filter(User.courses.any(title=course)).filter(User.taq_responses.any(age=3)).filter(User.is_module_leader == 0).all()
    SixtyFivePlus = User.query.filter(User.courses.any(title=course)).filter(User.taq_responses.any(age=4)).filter(User.is_module_leader == 0).all()
    NotSay = User.query.filter(User.courses.any(title=course)).filter(User.taq_responses.any(age=5)).filter(User.is_module_leader == 0).all()
    PreListOfGroups = []
    PreListOfGroups.append(EighteenTo24)
    PreListOfGroups.append(TwentyFiveTo34)
    PreListOfGroups.append(ThirtyFiveTo54)
    PreListOfGroups.append(FiftyFiveTo64)
    PreListOfGroups.append(SixtyFivePlus)
    PreListOfGroups.append(NotSay)
  #Removes any groups from the list that have no students
  ListOfGroups = [x for x in PreListOfGroups if x != []]
  #Creates the a list of key names for the dictionary, e.g. "Team 1" (Need to add +1 to NumOfTeams as not going from index 0 anymore)
  for i in range(1, NumOfTeams+1):
    TeamName = "Team " + str(i)
    ListOfKeys.append(TeamName)
  #Creates the correct number of teams (list elements) in ListOfTeams
  ListOfTeams = [[] for i in range(NumOfTeams)]
  #Creates the dictionary of teams - Team Name : Members
  ZipObj = zip(ListOfKeys, ListOfTeams)
  DictOfTeams = dict(ZipObj)
  #Team Allocator
  SoFar = 0
  for group in ListOfGroups:
    GroupCounter = 0
    while GroupCounter <= len(group):
      for k, Key in enumerate(DictOfTeams):
        if GroupCounter == len(group):
          GroupCounter = GroupCounter + 1
          SoFar = k
          break
        elif k == 0 and SoFar == len(DictOfTeams):
          SoFar = 0
          DictOfTeams[Key].append(group[GroupCounter])
          GroupCounter = GroupCounter + 1
          SoFar = SoFar + 1
        elif k != SoFar:
          continue
        else:
          DictOfTeams[Key].append(group[GroupCounter])
          GroupCounter = GroupCounter + 1
          SoFar = SoFar + 1
  CourseObject = Courses.query.filter_by(title=course).first()
  GridSize =  max(len(v) for v in DictOfTeams.values())
  for team in DictOfTeams.keys():
    addTeam = Teams(title=team, course_id=CourseObject.id)
    db.session.add(addTeam)
    db.session.commit()
  for teams, members in DictOfTeams.items():
    TeamLookup = Teams.query.filter_by(title=teams, course_id=CourseObject.id).first()
    for member in members:
      statement = users_teams.insert().values(teams_id = TeamLookup.id, user_id = member.id)
      db.session.execute(statement)
      db.session.commit()
  return render_template('team_allo_results.html', students=students, ListOfGroups=ListOfGroups, NumOfTeams=NumOfTeams, size=size, priority=priority, DictOfTeams=DictOfTeams, course=course, CourseObject=CourseObject, GridSize=GridSize)


#Calculate marks section
#Leader selects the course
@app.route("/leader_select_courses/<username>")
@login_required
def leader_select_courses(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template("leader_select_courses.html", user=user)


# Leader selects the team
@app.route("/leader_select_team/<username>/<course>")
@login_required
def leader_select_team(username, course):
    user = User.query.filter_by(username=username).first_or_404()
    chosenCourse = Courses.query.filter_by(title=course).first_or_404()
    teams = Teams.query.all()
    return render_template(
        "leader_select_team.html",
        username=username,
        course=course,
        user=user,
        chosenCourse=chosenCourse,
        teams=teams,
    )


# Calculate Marks page loads
@app.route("/leader_calculate_marks/<username>/<course>/<team>")
def leader_calculate_marks(username, course, team):
    user = User.query.filter_by(username=username).first_or_404()
    chosenCourse = Courses.query.filter_by(title=course).first_or_404()
    chosenTeam = Teams.query.filter_by(title=team).first_or_404()
    answerList = PAQresponse.query.filter_by(team=chosenTeam.title).all()
    teamMembers = chosenTeam.users

    return render_template(
        "leader_calculate_marks.html",
        username=username,
        course=course,
        user=user,
        chosenCourse=chosenCourse,
        team=chosenTeam.title,
    )


# Calculate Marks page function that calculates final marks
@app.route("/calculate/<username>/<course>/<team>", methods=["POST"])
def calculate(username, course, team):
    # Input feilds for grade band, group mark and operation
    groupMark = request.form["group_mark"]
    excellent = request.form["excellent"]
    good = request.form["good"]
    poor = request.form["poor"]
    no_contrbution = request.form["no_contrbution"]
    operation = request.form["operation"]
    # Imports contribution marks and creates loop that outputs username and final mark for each student
    user = User.query.filter_by(username=username).first_or_404()
    chosenCourse = Courses.query.filter_by(title=course).first_or_404()
    chosenTeam = Teams.query.filter_by(title=team).first_or_404()
    answerList = PAQresponse.query.filter_by(team=chosenTeam.title).all()
    teamMembers = chosenTeam.users
    userMarks = []
    for user in teamMembers:
        markList = []
        studentMarks = PAQresponse.query.filter_by(
            targetUser=user.username, team=chosenTeam.title
        ).all()
        for mark in studentMarks:
            markList.append(mark.q1)
            markList.append(mark.q2)
        total = 0
        for mark in markList:
            total = total + mark
        average = round(total / len(markList))
        # Calculates final mark, from the group mark, contribution 'mark' and the grade band e.g. 4, excellent band set to 120%
        if operation == "mean":
            if average == 4:
                score = int(groupMark) / 100 * int(excellent)
            elif average == 3:
                score = int(groupMark) / 100 * int(good)
            elif average == 2:
                score = int(groupMark) / 100 * int(poor)
            elif average == 1:
                score = int(groupMark) / 100 * int(no_contrbution)
        finalMark = int(round(score, 0))
        userMarks.append([user.username, finalMark])

    return render_template("leader_calculate_marks.html", userMarks=userMarks)

#----------------------------------------------------------------
@app.route("/reportissue/<username>", methods=["GET", "POST"])
@login_required
def reportissue(username):
    user = User.query.filter_by(username=username).first_or_404()
    courses = Courses.query.all()
    teams = Teams.query.all()
    if request.method == "POST":
        content = request.form.get("content")
        team = request.form.get("team")
        course = request.form.get("course")
        re = Reportissue(username=username, content=content, team=team, course=course)
        db.session.add(re)
        db.session.commit()
        flash("Submit successfully ! ")
        return redirect(url_for("home"))
    return render_template("reportissue.html", user=user, courses=courses, teams=teams)


@app.route("/view_issue/")
@login_required
def view_issue():
    issues = Reportissue.query.all()
    return render_template(
        "view_issue.html",
        issues=issues,
    )

@app.route("/moduleteam/")
@login_required
def moduleteam():
    issues = Reportissue.query.all()
    return render_template(
        "moduleteam.html",
        issues=issues,
    )

# Task 4 - Peer Evaluation Questionnaire
# List the courses associated with the logged in student
@app.route("/courses/<username>")
@login_required
def courses(username):
    user = User.query.filter_by(username=username).first_or_404() # Returns the logged in user row in Users table
    return render_template("courses.html", user=user)


# List the teams within a chosen course for the logged in student
@app.route("/teams/<username>/<course>")
@login_required
def teams(username, course):
    user = User.query.filter_by(username=username).first_or_404()
    courseID = Courses.query.filter_by(title=course).first_or_404() # Returns id of course chosen on 'courses.html'
    teams = Teams.query.filter_by(course_id=courseID.id).first_or_404() # Returns list of all teams associated with that course
    generalTeamQuery = Teams.query.filter_by(course_id=courseID.id).first_or_404()
    emptyList = 0
    for user in generalTeamQuery.users:
        if user.username != username:
            emptyList += 1
    return render_template(
        "teams.html",
        username=username,
        course=course,
        user=user,
        courseID=courseID,
        teams=teams,
        emptyList=emptyList
    )


# List the team members within a chosen team and course for the logged in student
@app.route("/teamlist/<team>/<username>/<course>")
@login_required
def teamlist(team, username, course):
    teamID = Teams.query.filter_by(title=team).first_or_404()
    listOfUsernames = [] # Empty array to place the names of each user within the team.

    for member in teamID.users:
        listOfUsernames.append(member.username) # Add names to the empty array

    displayedList = [] #List of names that will appear on the html page

    for member in listOfUsernames:
        # Loop through the names and query the database to check whether there is already a row in the table
        dbCheck = PAQresponse.query.filter_by(username=username, team=team, targetUser=member).all()
        if not dbCheck: # If there is not a row then a questionnaire still needs to be filled out for that name
            displayedList.append(member) # Append that name to the displayed list
    return render_template(
        "teamlist.html",
        username=username,
        course=course,
        team=team,
        teamID=teamID,
        displayedList=displayedList
    )


# Show questionnaire relating to the chosen team member from the previously chosen team list and submit relevant data
@app.route("/paquestionnaire/<teammember>/<team>/<username>/<course>", methods=["GET", "POST"])
@login_required
def paquestionnaire(teammember, team, username, course):
    # nummberOfQuestions = Eval_form.query.filterby(course_id=course).first_or_404() # This should return a integer from 2-6 
    form = PeerEvalForm()
    # teamMemberName = User.query.filter_by(id=teammember).first_or_404()
    if form.validate_on_submit():
        response = PAQresponse(  # The data that will be submitted to the database
            username=username,
            targetUser=teammember,
            team=team,
            q1=form.radio_one.data,
            q2=form.radio_two.data,
            # nummberOfQuestions=nummberOfQuestions,
        )
        print(form.data)
        db.session.add(response)
        db.session.commit()
        flash("Form submission successful")
        return redirect(url_for("teamlist", course=course, team=team, username=username))
    return render_template("paquestionnaire.html", form=form)


# End Task 4

@app.route("/select_team")
@login_required
def select_team():
    course = Courses.query.all()
    return render_template(
        "select_team.html",
        course=course,
    )


@app.route("/team_information/<course>")
def team_information(course):
    users = User.query.filter(User.courses.any(title=course)).filter(User.is_module_leader == 0).all()
    #teamID = Teams.query.filter_by(title=team).first_or_404()
    courseID = Courses.query.filter_by(title=course).first_or_404()
    for user in users:
       for team in user.teams:
            if team.course_id == courseID.id:
               print(team.title)
            else: 
                continue
    return render_template(
        "team_information.html",
        users=users,
        course=course,
        courseID=courseID
    )
    return render_template("team_information.html", user=user, course=course)


@app.route("/user_csv/<course>")
def user_csv(course):
    def generate(course):
        user_data = (
            User.query.filter(User.courses.any(title=course))
            .filter(User.is_module_leader == 0)
            .all()
        )
        courseID = Courses.query.filter_by(title=course).first_or_404()

        data = StringIO()
        w = csv.writer(data)
        # writer
        datas = []
        course_title = ["Course", course, "", ""]
        datas.append(course_title)
        title = ["ID", "Name", "Email","Team"]
        datas.append(title)
        for row in user_data:
            temp = [row.id, row.username, row.email]
            for team in row.teams:
                if team.course_id == courseID.id:
                    temp.append(team.title)
                else: 
                    continue
            datas.append(temp)

        for item in datas:
            w.writerow(item)
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

    response = Response(
        stream_with_context(generate(course)), mimetype="text/csv"
    )  # file format
    response.headers.set(
        "Content-Disposition", "attachment", filename="user.csv"
    )  # file name
    return response


# For TAQ - List the courses associated with the logged in student
@app.route("/taqcourses/<username>")
@login_required
def taqcourses(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template("taqcourses.html", user=user)

#---------------------------------------
@app.route("/taquestionnaire/<username>/<course>", methods=["GET", "POST"])
@login_required
def taquestionnaire(username, course):
    course = Courses.query.filter_by(title=course).first_or_404()
    form = TaquestionnaireForm()
    if form.validate_on_submit():
        response = TAQresponse(  # The data that will be submitted to the database
            username=username,
            courseID=course.id,
            experienced=form.radio_one.data,
            degree=form.radio_two.data,
            age=form.radio_three.data,
        )
        print(form.data)
        db.session.add(response)
        db.session.commit()
        flash("Form submission successful")
        return redirect(url_for("home"))
    return render_template("taquestionnaire.html", form=form)



@app.route("/evaluation_course_select/")
@login_required
def evaluation_course_select():
    user = current_user
    return render_template("evaluation_course_select.html",user = user)

@app.route("/question_select/<course>", methods=["GET", "POST"])
@login_required
def question_select(course):
    Q = EvalForm.query.filter_by(title=course).order_by(EvalForm.id.desc()).first()

    user = current_user
    Q1 = (str_op(PeerEvalForm.radio_one))
    Q2 = (str_op(PeerEvalForm.radio_two))
    Q3 = (str_op(PeerEvalForm.radio_three))
    Q4 = (str_op(PeerEvalForm.radio_four))
    Q5 = (str_op(PeerEvalForm.radio_five))
    Q6 = (str_op(PeerEvalForm.radio_six))
    if check_selection(course) == False:

    
        if request.method == "POST":
            q_list = request.form.getlist("Question")
            print(q_list)
            if '1' in q_list:
                Q1_a = True
            elif '1' not in q_list:
                Q1_a = False
            if '2' in q_list:
                Q2_a = True
            elif '2' not in q_list:
                Q2_a = False
            if '3' in q_list:
                Q3_a = True
            elif '3' not in q_list:
                Q3_a = False
            if '4' in q_list:
                Q4_a = True
            elif '4' not in q_list:
                Q4_a = False
            if '5' in q_list:
                Q5_a = True
            elif '5' not in q_list:
                Q5_a = False
            if '6' in q_list:
                Q6_a = True
            elif '6' not in q_list:
                Q6_a = False
    
            re = EvalForm(title=course, q1=Q1_a, q2=Q2_a, q3=Q3_a, q4=Q4_a, q5=Q5_a, q6=Q6_a)
            db.session.add(re)
            db.session.commit()
            flash("Submition is successful!")
        #return redirect(url_for("evaluation_course_select"))
    elif check_selection(course) == True:
        return redirect(url_for("question_information",course=course, user=user, Q1=Q1, Q2=Q2, Q3=Q3, Q4=Q4, Q5=Q5, Q6=Q6, Q=Q))
    return render_template("question_select.html", course=course, user=user, Q1=Q1, Q2=Q2, Q3=Q3, Q4=Q4, Q5=Q5, Q6=Q6)
        
def check_selection(course): 
    Q = EvalForm.query.filter_by(title=course).order_by(EvalForm.id.desc()).first()
    if (Q.q1 or Q.q2 or Q.q3 or Q.q4 or Q.q5 or Q.q6) == True:
        return True
    elif (Q.q1 or Q.q2 or Q.q3 or Q.q4 or Q.q5 or Q.q6) == False:
        return False

def str_op (Question):
    st = ""
    st = str(Question.args)
    st = st[:-3]
    st = st[2:]
    return st

@app.route("/question_information/<course>", methods=["GET","POST"])
@login_required
def question_information(course):
    user = current_user
    Q1 = (str_op(PeerEvalForm.radio_one))
    Q2 = (str_op(PeerEvalForm.radio_two))
    Q3 = (str_op(PeerEvalForm.radio_three))
    Q4 = (str_op(PeerEvalForm.radio_four))
    Q5 = (str_op(PeerEvalForm.radio_five))
    Q6 = (str_op(PeerEvalForm.radio_six))
    Q = EvalForm.query.filter_by(title=course).order_by(EvalForm.id.desc()).first()
    return render_template("question_information.html", course=course, user=user, Q1=Q1, Q2=Q2, Q3=Q3, Q4=Q4, Q5=Q5, Q6=Q6, Q=Q)

@app.route("/reset_questions/<course>", methods=["GET","POST"])
@login_required
def reset_questions(course):
    Q1_a = False
    Q2_a = False
    Q3_a = False
    Q4_a = False
    Q5_a = False
    Q6_a = False
    re = EvalForm(title=course, q1=Q1_a, q2=Q2_a, q3=Q3_a, q4=Q4_a, q5=Q5_a, q6=Q6_a)
    db.session.add(re)
    db.session.commit()
    flash("Reset is successful!")
    return render_template("reset_questions.html", course=course)

