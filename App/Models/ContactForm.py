from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

# TODO: The current models are not tailored for this project. Please modify them to suit your specific requirements.


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired('Name')])
    email = StringField('E-mail', validators=[DataRequired('E-mail'), Email('Email')])
    subject = StringField('Subject', validators=[DataRequired('Subject')])
    message = TextAreaField('Message', validators=[DataRequired('Message')])
    submit = SubmitField("Submit")

class ForgotForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired('E-mail'), Email('Email is invalid')])
    submit = SubmitField("Submit")
