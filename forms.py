from flask_wtf import FlaskForm
from wtforms.validators import Length
from wtforms import StringField, PasswordField, SubmitField
from wtforms.ext.sqlalchemy.orm import QuerySelectField
from models import User

def kjahsdkjha():
    return User.query.all()

class SignUpForm(FlaskForm):
    username = StringField('Enter Username', )
    password = PasswordField('Password...', validators=[Length(min=4, max=50)])
    email = StringField('Your email address')
    users = QuerySelectField('Pick User', query_factory=kjahsdkjha)


class CreatePostForm(FlaskForm):
    title = StringField('Enter Username')
    content = PasswordField('Password...')
    users = QuerySelectField('Pick User', query_factory=kjahsdkjha)
