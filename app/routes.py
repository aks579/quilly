from flask import jsonify, redirect, url_for, render_template, send_from_directory
from app import app
import os
import markdown
from app.config import *
import re
from app import tags
from app.forms import NoteForm, DeleteNoteForm

folder = app.config['FOLDER']
attachments = app.config['ATTACHMENTS']

@app.route('/')
def index():
	markdown_files = tags.get_all_notes()
	markdown_dict = {f.replace("_", " "): f for f in markdown_files}  
	heading = 'All Notes'

	#return jsonify({'files': markdown_files})
	return render_template('index.html', heading = heading, content = markdown_dict, tags=tags.get_all_unique_tags(), type = 'index')


@app.route('/tags/<tag>',methods = ['GET'])
def read_tags(tag):
	tags_set, notes_set = tags.get_tags_and_notes_list(tag)
	markdown_dict = {f.replace("_", " "): f for f in notes_set}  
	heading = f'Notes tagged #{tag}'
	return render_template('index.html', heading = heading, content = markdown_dict, tags=tags_set, type = 'index')


@app.route('/<file>',methods = ['GET'])
def read(file):
	file_path = f"{folder}/{file}.md"
	try:
		with open(file_path, 'r') as f:
			file_content = f.read()
			heading = file.replace("_", " ")
			#file_content = file_content.replace(f"# {heading}\n", "")

			mermaid_pattern = r'```mermaid(.*?)```'
			file_content = re.sub(mermaid_pattern, r'<pre class="mermaid">\1</pre>', file_content, flags=re.DOTALL)

			file_content = markdown.markdown(file_content,extensions=['tables','fenced_code', 'codehilite'])

			file_content = re.sub(r'Tags : \[(.*?)\]', replace_tags, file_content)

			return render_template('index.html', heading = heading, file = file, content = file_content, tags=tags.get_all_unique_tags(), type = 'read')
	except (FileNotFoundError, IOError) as e:
		print(f"An error occurred while reading the file: {e}")
		return redirect(url_for('index'))

@app.route('/create',methods = ['GET', 'POST'])
def create():
	form = NoteForm()
	if form.validate_on_submit():
		file_name = form.title.data.replace("/","").replace(" ","_")
		file_path = f"{folder}/{file_name}.md"	
		try:	
			with open(file_path, 'w') as f: 
				f.write(f"# {form.title.data}\n")
				f.write(form.note.data)
			tags.modify_tags(form.note.data, file_name, file_name)
		except IOError as e:
			print(f"An error occurred while writing to file: {e}")
			return redirect(url_for('index'))
		return redirect(url_for('read',file=file_name))
	return render_template('note.html', form = form, tags=tags.get_all_unique_tags(), type = 'create')

@app.route('/<file>/edit',methods = ['GET', 'POST'])
def edit(file):
	file_path = f"{folder}/{file}.md"
	form = NoteForm()
	if form.validate_on_submit():
		edit_file_name = form.title.data.replace("/","").replace(" ","_")
		edit_file_path = f"{folder}/{edit_file_name}.md"	
		if file_path != edit_file_path:
			os.rename(file_path, edit_file_path)
		try:	
			with open(edit_file_path, 'w') as f: 
				f.write(f"# {form.title.data}\n")
				f.write(form.note.data)
			tags.modify_tags(form.note.data, file, edit_file_name)
		except IOError as e:
			print(f"An error occurred while writing to file: {e}")
			return redirect(url_for('index'))
		return redirect(url_for('read',file=edit_file_name))
	try:
		form.title.data = file.replace("_"," ")
		with open(file_path, 'r') as f:
			file_content = f.read()
			file_content = file_content.replace(f"# {form.title.data}\n", "")
		form.note.data = file_content
	except (FileNotFoundError, IOError) as e:
		print(f"An error occurred while reading the file: {e}")
		return redirect(url_for('index'))
	return render_template('note.html', form = form, tags=tags.get_all_unique_tags(), type = 'edit')

@app.route('/<file>/delete',methods = ['GET', 'POST'])
def delete(file):
	file_path = f"{folder}/{file}.md"
	heading = file.replace("_", " ")
	form = DeleteNoteForm()
	if form.validate_on_submit():
		try:
			if os.path.exists("file_path"):
				tags.delete(file)
				os.remove(file_path)
		except IOError as e:
			print(f"An error occurred while writing to file: {e}")
		return redirect(url_for('index'))
	return render_template('delete-confirmation.html', file=file, heading = heading, form = form, tags=tags.get_all_unique_tags(), type = 'delete')

@app.route('/attachments/<path:filename>')
def serve_attachments(filename):
	path = f"../{attachments}" if attachments == 'data' else attachments
	return send_from_directory(path, filename)

def replace_tags(match):
	tag_list = match.group(1).split()
	replaced_tags = []
	for tag in tag_list:
		tag = tag.strip()
		replaced_tags.append(f'<a href="tags/{tag}">{tag}</a>')
	tags = ' '.join(replaced_tags)
	return f'Tags : {tags}'