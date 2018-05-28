#!/usr/bin/env python3

import json
import os
import sys
import argparse


dataset_dir = '../RosettaCodeData/Task'
language_path = './languages.json'
source_path = './sources.json'
compile_all = False
instrument_cmd = './instrument.sh {} {} {} {}'


# Colors
PURPLE = '\033[0;35m'
BLUE = '\033[1;34m'
GREEN = '\033[1;32m'
RED = '\033[0;31m'
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
	def __init__(self, file_in, language_set, category=None, properties=None):
		(_, extension) = os.path.splitext(file_in)
		# Source inherits its language's properties
		self.lang_properties = Language.from_extension(language_set, extension)
		self.properties = properties
		file_in_full = os.path.join(dataset_dir, file_in)
		(source_dir, _) = os.path.split(file_in_full)
		file_out_full = self.lang_properties['file_out'].format(source_dir)
		self.properties['file_in'] = file_in_full
		self.properties['file_out'] = file_out_full
		self.category = category
		
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
				source = Source(properties['file_in'], language_set, category, properties)
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

def instrument(source=None, index=None, binary_path=None):
	# Targeting mode
	if binary_path != None:
		cmd = instrument_cmd.format('"' + binary_path + '"', '""', '""', 'fistouille')
	# Steam engine mode
	else:
		cmd = instrument_cmd.format('"' + source.get_property('file_out') + '"', source.category, index, '""')
	print_colored(cmd, GREEN)
	os.system(cmd)

# Remove every file except source files within every directory under dataset directory
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

def reset_max_graph_size():
	try:
		os.remove("../dataset/callgrind/maxsize")
		os.remove("../dataset/cologrind/maxsize")
	except:
		pass

def main():
	# Arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("--infile", dest="in_file", help="Input file (targeting mode)")
	parser.add_argument("--compile", "-c", dest="compile", \
	 action="store_const", const=True, default=False, \
	 help="Compile sources")
	parser.add_argument("--instrument", "-i", dest="instrument", \
	 action="store_const", const=True, default=False, \
	 help="Instrument binaries")
	args = parser.parse_args()
	# If neither -c nor -i is specified, process both by default
	if not(args.compile or args.instrument):
		args.compile = True
		args.instrument = True
	if (args.in_file != None):
		args.targeting_mode = True
	else:
		args.targeting_mode = False
	
	sources = []
	
	# Targeting mode
	if args.targeting_mode:
		print_colored("Screw you, man. SCREW-YOU! >:[", RED)
		instrument(binary_path=args.in_file)
	
	# Steam engine mode
	else:
		if not(compile_all):
			# Fetch every source specified in source_path
			sources = Source.fetch_sources()
		else:
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
	
		# Process list of sources
		reset_max_graph_size()
		index = 0
		for source in sources:
			print('\n\n')
			if args.compile:
				compile(source)
			if args.instrument:
				instrument(source=source, index=index)
				index += 1
	
	exit(0)

if __name__ == '__main__':
	main()
