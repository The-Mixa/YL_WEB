from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField
from wtforms import SubmitField, IntegerField, EmailField

from wtforms.validators import DataRequired


class DepartmentsForm(FlaskForm):
    title = TextAreaField('Название департамента', validators=[DataRequired()])
    chief = IntegerField('Chief id', validators=[DataRequired()])
    members = StringField('Сотрудники')
    email = EmailField('Электронная почта')
    submit = SubmitField('Submit')
