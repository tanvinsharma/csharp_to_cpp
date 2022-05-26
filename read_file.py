import re

def read_file(file):
	with open(file) as f:
		read_data = f.read()
		# all_found = re.split('[0-9a-zA-Z_]+', read_data)
		# keywords_found = re.split('[^0-9a-zA-Z_]+', read_data)
		keywords_found = re.split('([^0-9a-zA-Z_]+)', read_data)
		keywords_found_clean = [elem for elem in keywords_found if elem != ' ']
		return keywords_found_clean

# stuff = read_file('cs_code.cs')
# for elem in stuff:
# 	print(elem.split())
