import os
import re
import json
from app import app
from app.config import *

data = {}  # Dictionary to store tag-file associations

#markdown_dir = FOLDER if FOLDER != "" else "data"
markdown_dir = app.config['FOLDER']


def load_tags_data():
	for filename in os.listdir(markdown_dir):
		if filename.endswith('.md'):
			file_path = os.path.join(markdown_dir, filename)
			with open(file_path, 'r') as file:
				content = file.read()
				tags_match = re.search(r'Tags\s*:\s*\[([^\]]+)\]', content)
				if tags_match:
					tags = tags_match.group(1).split()
					data[file_path.replace(f'{markdown_dir}/', '').replace('.md', '')] = tags
				else:
					data[file_path.replace(f'{markdown_dir}/', '').replace('.md', '')] = []

	# Save the data using JSON
	with open('tags.json', 'w') as json_file:
		json.dump(data, json_file)

def get_all_notes():
	with open('tags.json', 'r') as json_file:
		loaded_data = json.load(json_file)	
	return list(loaded_data.keys())

# To load the data back
#with open('tags.json', 'r') as json_file:
#	loaded_data = json.load(json_file)
def get_all_unique_tags():
	tags_set = set()
	with open('tags.json', 'r') as json_file:
		loaded_data = json.load(json_file)
	for key, value in loaded_data.items():
		tags_set.update(value)
	return tags_set


def get_tags_and_notes_list(tag):
	tags_set = set()
	notes_set = set()
	with open('tags.json', 'r') as json_file:
		loaded_data = json.load(json_file)
	for key, value in loaded_data.items():
		tags_set.update(value)
		if tag in value:
			notes_set.add(key)
	return tags_set, notes_set

def modify_tags(content, file_name, new_file_name):
	with open('tags.json', 'r') as json_file:
		loaded_data = json.load(json_file)
	tags_match = re.search(r'Tags\s*:\s*\[([^\]]+)\]', content)
	if tags_match:
		tags = tags_match.group(1).split()
	else:
		tags = []
	if file_name == new_file_name:
		loaded_data[file_name] = tags
	else:
		loaded_data.pop(file_name)
		loaded_data[new_file_name] = tags
	with open('tags.json', 'w') as json_file:
		json.dump(loaded_data, json_file)

def delete(file_name):
	with open('tags.json', 'r') as json_file:
		loaded_data = json.load(json_file)
	loaded_data.pop(file_name)
	with open('tags.json', 'w') as json_file:
		json.dump(loaded_data, json_file)