from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, FieldList
from wtforms import SubmitField, IntegerField, BooleanField

from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    title = TextAreaField('Job Title', validators=[DataRequired()])
    team_leader_id = IntegerField('Team Leader id', validators=[DataRequired()])
    work_size = IntegerField('work Size', validators=[DataRequired()])
    collaborators = StringField('Сотрудники')
    categories = StringField('Категория', validators=[DataRequired()])
    is_finished = BooleanField('Is job is finished?')
    submit = SubmitField('Submit')