#!/usr/bin/python
import sys
import re
#import subprocess

def usage():
	''' Display the correct script usage and the file formats to input via command line.'''
	print
	print "* The script takes as input two files. One containing a list of variables and one containing the router config template."
	print "* "
	print "* Example:"
	print "* config_maker.py <variables.txt> <template.txt>"
	print "* "
	print "* Variables file format:"
	print "* <hostname> = "
	print "* <enable_secret_password> = "
	print "* <enable_password> = "
	print "* etc."
	print "* "
	print "* Configuration template file format:"
	print "* hostname <hostname>"
	print "* !"
	print "* boot-start-marker"
	print "* boot-end-marker"
	print "* !"
	print "* !"
	print "* enable secret <enable_secret_password>"
	print "* enable password <enable_password>"
	print "* etc."
	print "* "
	print "* The script creates a new file named as the router hostname containing the configuration to be applied."
	print
	

def variable_extractor(text):
	''' Find all the variables in the text and append them to a dictionary (and to a list for match verification) '''
	matches = []
	variables_dict = {}
	text_lines = text.strip().split("\n")
	
	for line in text_lines:
		match = re.search(r"(<.*>)\s=(.*)", line)
		if match:
			variable = match.group(1)
			value = match.group(2).strip()
			variables_dict[variable] = value
			matches.append(value)
		else:
			continue
		
		# Example: match1 = re.search(r"<hostname>\s=(.*)", text)
        #          variables_dict["hostname"] = match1.group(1).strip()
        #          matches.append(match1.group(1).strip())
		
	
	# Verify the variables are not empty
	for match in matches:
		if match == "":
			print "At least one parameter was not entered. Check the configuration carefully before apply it."
	
	
	
	return variables_dict
		
		

def template_modifer(variables_dict, template_string):
	''' One by one substitute all the variables taken from the dictionary into the template. '''
	for variable,value in variables_dict.items():
		template_string = re.sub(variable, value, template_string)
		# Example: sub1 = re.sub("<hostname>", variables_dict["hostname"], template_string)
		
	return template_string

	


if __name__ == '__main__':

	# Inform the user about the correct usage
	if len(sys.argv) != 3:
		usage()
		sys.exit()

		
	try:
		# Open the file containing the list of variables, read it and extract its content. The variables will be placed on a dictionary.
		variable_file = open(sys.argv[1], "r")
		
		variables_string = variable_file.read()
		
		variable_file.close()
		
		variables_dict = variable_extractor(variables_string)
		
		
		# Open the template file, read its content and modify it using the variables stored in the dictionary.
		template_file = open(sys.argv[2], "r")
		
		template_string = template_file.read()
		
		template_file.close()
		
		new_template_string = template_modifer(variables_dict,template_string)
		
		
		# Open a new file and write the new template. Filename will be the hostname.
		new_template_file = open(variables_dict["<hostname>"], "w")
	
		new_template_file.write(new_template_string)
		new_template_file.write("\n")

		new_template_file.close()
	
		print 'New configuration file "%s" created.' % variables_dict["<hostname>"]

	
	except IOError:
		print "Error in opening a file. Please check them and try again."
		sys.exit()

