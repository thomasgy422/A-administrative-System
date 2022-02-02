from operator import sub
from flask_wtf import FlaskForm, Form
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    TextAreaField,
    TextField,
    RadioField,
)
from wtforms.fields.core import BooleanField, IntegerField
from wtforms.validators import (
    DataRequired,
    InputRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
    Regexp,
)
#from tapes.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(message="Please enter your username"),
            Length(min=3, max=15),
        ],
    )
    email = StringField(
        "Email",
        validators=[DataRequired(message="Please enter your email address"), Email()],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Please enter your password"),
            Regexp(
                "^.{5,15}$",
                message="Your password must be between 5 and 15 characters long.",
            ),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(
                message="Please confirm that the password provided is correct"
            ),
            EqualTo("password"),
        ],
    )
    marketing_field = BooleanField("Do you want to subscribe to CatFacts?")
    submit = SubmitField("Register")
    # recaptcha = RecaptchaField() # new
    """
    def valididate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(
                "Username already exists. Please use a different username, or use these details to login."
            )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(
                "The provided email already exists. Please use a different email address, or use these details to login."
            )
    """

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class TextForm(FlaskForm):
    question = StringField("Question", validators=[DataRequired()])


class IntForm(FlaskForm):
    question = IntegerField("Please enter a value", validators=[DataRequired()])


class BoolForm(FlaskForm):
    question = BooleanField("Yes/No", validators=[DataRequired()])


class SubmitForm(FlaskForm):
    submit = SubmitField("Submit answers")


class PeerEvalForm(FlaskForm):
    radio_one = RadioField(
        "How would you rate your colleague’s level of group participation?",
        choices=[
            ("4", "Excellent"),
            ("3", "Good"),
            ("2", "Poor"),
            ("1", "No Contribution"),
        ],
        coerce=str,
        validators=[DataRequired()]
    )

    radio_two = RadioField(
        "How would you rate your colleague’s time management and responsibility?",
        choices=[
            ("4", "Excellent"),
            ("3", "Good"),
            ("2", "Poor"),
            ("1", "No Contribution"),
        ],
        coerce=str,
        validators=[DataRequired()]
    )
    
    radio_three = RadioField(
        "Can your colleagues finish the task on time?",
        choices=[
            ("3", "always"),
            ("2", "sometimes"),
            ("1", "never"),
        ],
        coerce=str,
        validators=[DataRequired()]
    )

    radio_four = RadioField(
        "Did your colleague's advice help you?",
        choices=[
            ("3", "always"),
            ("2", "sometimes"),
            ("1", "never"),
        ],
        coerce=str,
        validators=[DataRequired()]
    )

    radio_five = RadioField(
        "Are colleagues friendly and cooperative?",
        choices=[
            ("2", "yes"),
            ("1", "no"),
        ],
        coerce=str,
        validators=[DataRequired()]
    ) 

    radio_six = RadioField(
        "Are your colleagues able to finish tasks independently?",
        choices=[
            ("2", "yes"),
            ("1", "no"),
        ],
        coerce=str,
        validators=[DataRequired()]
    )

    submit = SubmitField("Submit")

      
class TaquestionnaireForm(FlaskForm):
    radio_one = RadioField(
        "Do you have any prior programming experience?",
        choices=[
            ("0", "No"), 
            ("1", "Yes"),
        ],
        coerce=str,
        validators=[DataRequired()],
    )

    radio_two = RadioField(
        "What disciplinary background do you come from?",
        choices=[
            ("BSc", "BSc"), 
            ("BA", "BA"),
            ("BEng", "BEng"),
            ("LLB", "LLB"),
        ],
        coerce=str,
        validators=[DataRequired()],
    )

    radio_three = RadioField(
        "Please select your age.",
        choices=[
            ("0", "18-24 years"), 
            ("1", "25-34 years"),
            ("2", "35-54 years"),
            ("3", "55-64 years"),
            ("4", "65+ years"),
            ("5", "Prefer not to say"),
        ],
        coerce=str,
        validators=[DataRequired()],
    )

    submit = SubmitField("Submit")

