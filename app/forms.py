from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo



class PostForm(FlaskForm):
    title = StringField("Title", validators = [DataRequired()])
    img_url = StringField("Image URL", validators = [DataRequired()])
    caption = StringField("Caption", validators = [])
    
    submit = SubmitField()


class SearchForm(FlaskForm):
    shoha = StringField('ANYTHING CAN GO HERE', validators=[DataRequired()])

    send_it = SubmitField()

