#!/usr/bin/env python3

import json
import os
import sys


dataset_dir = '../RosettaCodeData/Task'
language_path = './languages.json'
source_path = './sources.json'
compile_all = False
instrument_cmd = './instrument.sh {}'


# Colors
PURPLE = '\033[0;35m'
BLUE = '\033[1;34m'
GREEN = '\033[1;32m'
NC = '\033[0;0m'
def print_colored(msg, color):
	print(color + msg + NC)


class Language:
	def fetch_languages():
		return json.load(open(language_path))
		
	def from_extension(language_set, extension):
		for language_name in language_set:
			if language_set[language_name]['extension'] == extension:
				return language_set[language_name]


class Source:
	def __init__(self, file_in, language_set):
		(_, extension) = os.path.splitext(file_in)
		# Source inherits its language's properties
		self.lang_properties = Language.from_extension(language_set, extension)
		file_in_full = os.path.join(dataset_dir, file_in)
		(source_dir, _) = os.path.split(file_in_full)
		file_out_full = self.lang_properties['file_out'].format(source_dir)
		self.properties = dict({'file_in': file_in_full, 'file_out': file_out_full})
	
	def __init__(self, file_in, language_set, properties):
		(_, extension) = os.path.splitext(file_in)
		# Source inherits its language's properties
		self.lang_properties = Language.from_extension(language_set, extension)
		self.properties = properties
		file_in_full = os.path.join(dataset_dir, file_in)
		(source_dir, _) = os.path.split(file_in_full)
		file_out_full = self.lang_properties['file_out'].format(source_dir)
		self.properties['file_in'] = file_in_full
		self.properties['file_out'] = file_out_full
		
	# Look for property into intrinsic properties, then into inherited properties from language
	def get_property(self, property):
		if property in self.properties:
			return self.properties[property]
		elif property in self.lang_properties:
			return self.lang_properties[property]
		else:
			return None
	
	# Generate list of sources
	def fetch_sources():
		language_set = Language.fetch_languages()
		sources = []
		json_categories = json.load(open(source_path))
		for category, json_sources in json_categories.items():
			for _, properties in json_sources.items():
				# Get intrinsic properties
				#TODO: duplicate with dict()?
				source = Source(properties['file_in'], language_set, properties)
				# Append source to list
				sources.append(source)
		return sources
	
	def print(self):
		print(self.lang_properties)
		print(self.properties)


def compile(source):
	# Get properties
	file_in = source.get_property('file_in')
	file_out = source.get_property('file_out')
	compiler_cmd = source.get_property('compiler_cmd')
	compiler_args = source.get_property('compiler_args')
	# Build command line
	cmd = compiler_cmd.format(file_in, file_out, compiler_args)
	# Compile
	print_colored(cmd, BLUE)
	os.system(cmd)

def instrument(source):
	cmd = instrument_cmd.format(source.get_property('file_out'))
	print_colored(cmd, GREEN)
	os.system(cmd)

# Remove every file except source file within every directory under dataset directory
def clean():
	language_set = Language.fetch_languages()
	for folder in os.listdir(dataset_dir):
		path = os.path.join(dataset_dir, folder)
		for language_name in language_set:
			path2 = os.path.join(path, language_name)
			for file in os.listdir(path2):
				(_, ext) = os.path.splitext(file)
				file_full = os.path.join(path2, file)
				if ext != language_set[language_name]['extension'] and os.path.isfile(file_full):
					print("removing '" + file_full + "'")
					os.remove(file_full)

# Get first file with correct extension
def get_first_file(path, file_ext):
	for f in os.listdir(path):
		f = os.path.join(path, f)
		if os.path.isfile(f):
			(_, ext) = os.path.splitext(f)
			if ext == file_ext:
				return f
	return None

def main():
	sources = []
	#clean()
	if compile_all:
		# Compile every source under source_path
		#TODO: update this block (outdated)
		language_set = Language.fetch_languages()
		for language, l in lang.items():
			for _, t in tasks.items():
				(cmd, file_out, file_ext) = l
				path = os.path.join(dataset_dir, t, language)
				file_in = get_first_file(path, file_ext)
				file_out = os.path.join(path, file_out)
				cmd = cmd.format(file_in, file_out)
				
				source = Source(file_in, language)
				sources.append(source)

				#src = Source(file_in, lang_folder)
				#src.print2()
				Source.fetch_sources()
				#print((file_in))
				#compile(cmd, file_in, file_out)
	else:
		# Fetch every source specified in source_path
		sources = Source.fetch_sources()
	
	# Process list of sources
	for source in sources:
		print('\n\n')
		#source.print()
		compile(source)
		instrument(source)
		

if __name__ == '__main__':
	main()
