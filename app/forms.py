from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField

from wtforms import validators, ValidationError

def check_title_length(form, field):
	if len(field.data) > 100:
		raise ValidationError('Please keep the size of title upto 100 characters')

class NoteForm(FlaskForm):
	title = StringField("Title",[validators.DataRequired("Please enter the title."), check_title_length])
	note = TextAreaField()
	submit = SubmitField("Create")

class DeleteNoteForm(FlaskForm):
	submit = SubmitField("Delete")