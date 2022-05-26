import re 
from keywords import KEYWORDS, KEYWORDS_DATA

class CSClass():
	def __init__(self, code):
		self.class_access = code[0]
		self.class_return = code[1]
		self.class_name = code[2]
		self.get_params(code)
		self.get_statements(self.body)

	def print(self):
		print('Access:')
		print(self.class_access)
		print('\nReturn type:')
		print(self.class_return)
		print('\nClass Name:')
		print(self.class_name)
		print('\nParams')
		print(self.params)
		print('\nStatements')
		print(self.statements)
		print('\nTokens')
		print(self.tokens)

	def get_params(self, code):
		start = 0
		stop = 0
		for i, val in enumerate(code):
			if val == '(' and start == 0:
				start = i
				continue
			if val.split() == ['){'] and stop == 0:
				stop = i
				continue
			if start and stop:
				break
		params = code[start:stop]
		parameters = [re.split('[^0-9a-zA-Z_,]+', param) for param in params if len(re.split('[^0-9a-zA-Z_,]+', param)) == 1]
		params = [item for sublist in parameters for item in sublist]
		self.params = params
		self.body = code[stop+1:]
		
	def get_statements(self, code):
		words = []
		for elem in code:
			words.append(re.split('([^0-9a-zA-Z_;]+\0)', elem))
		werds = [item.split() for sublist in words for item in sublist]
		final_words = [item for sublist in werds for item in sublist]
		words.clear()
		for i, word in enumerate(final_words):
			if ';' in word:
				temp = word.split(';')
				temp[1] = ';'
				words.append(temp[0])
				words.append(temp[1])
			else:
				words.append(word)
		for word in words:
			if word == '\0':
				words.remove(word)
		len_words = len(words)
		statements = []
		string_words = (' ').join(words)
		final_words = string_words.split(';')
		self.statements = final_words
		tokens = [''.join(c for c in word if c.isalpha()) for word in string_words.split()]
		list_tokens = list(filter(None, tokens))
		self.tokens = list_tokens

	def clean_statements(self, statements):
		# check no of for loops and reiterate the process. same for if and else
		for_string = ''
		body_string = ''
		found = 0
		for i, statement in enumerate(statements):
			if 'foreach' in statement:
				found = i
				for i, e in enumerate(statement):
					if e == '{':
						for_string = statement[:i]
						body_string = statement[i:]
						break
		statements.remove(statements[found])
		statements.insert(found, for_string)
		statements.insert(found+1, body_string)
		if_string = ''
		rest = ''
		found = 0
		for i, statement in enumerate(statements):
			if 'if' in statement:
				found = i
				for i, e in enumerate(statement):
					if e == '{':
						if_string = statement[:i]
						rest = statement[i:]
						break
		statements.remove(statements[found])
		statements.insert(found, if_string)
		statements.insert(found+1, rest)
		self.statements = statements
		declaration = ''
		for i, statement in enumerate(statements):
			if 'try' in statement:
				found = i
				for i, e in enumerate(statement):
					if e == '{':
						declaration = statement[:i+1]
						rest = statement[i+1:]
						break
		statements.remove(statements[found])
		statements.insert(found, declaration)
		statements.insert(found+1, rest)
		found = []
		bracket = ''
		inspected_stats = []
		for i, statement in enumerate(statements):
			if '{' in statement and '{' == statement[0]:
				found.append(i)
		for i, statement in enumerate(statements):
			for f in found:
				if i == f:
					inspected_stats.append(statement)
		new_statement = []
		for i, statement in enumerate(inspected_stats):
			fou = i
			if '{' in statement:
				for i, e in enumerate(statement):
					if e == '{':
						bracket = statement[:i+1]
						rest = statement[i+1:]
						new_statement.append({found[fou]: [bracket, rest]})
						break
		
		for i, stat in enumerate(new_statement):
			for key, value in stat.items():
				if i==0:
					statements.remove(statements[key])
					statements.insert(key, value[0])
					statements.insert(key+1, value[1])
				elif i==1:
					statements.remove(statements[key+1])
					statements.insert(key+1, value[0])
					statements.insert(key+2, value[1])

		found_catch = 0
		for i, stat in enumerate(statements):
			if 'catch' in stat:
				found_catch = i
				catch = stat.index('catch')
				command1 = stat[:catch]
				start = stat.index('{')
				command1 = command1 + stat[catch: start+1]
				command2 = stat[start+1:]
		statements.remove(statements[found_catch])
		statements.insert(found_catch, command1)
		statements.insert(found_catch+1, command2)
		self.statements = statements		
		# for stat in statements:
		# 	print(stat)
		


	def return_data_of_statement(self, type, stat):
		if type == 1:
			split_string = stat.split()
			if 'List' in split_string:
				eq = split_string.index('=')
				data_struct = split_string[0]
				data_type = split_string[2]
				variable_name = split_string[eq-1]
				return {
				'data_struct': data_struct,
				'data_type': data_type,
				'variable_name': variable_name
				}
			else:
				eq = split_string.index('=')
				param_open = split_string.index('(')
				param_end = split_string.index(')')
				class_name = split_string[eq+2]
				# print(class_name)
				variable_name = split_string[eq-1]
				# print(variable_name)
				params = split_string[param_open+1:param_end]
				parameters = [param for param in params if param != ',']
				return {
				'class_name': class_name,
				'variable_name': variable_name,
				'params': parameters
				}

		if type == 2:
			split_string = stat.split()
			data_type = split_string[0]
			variable_name = split_string[1]
			if '.' in split_string and '(' not in split_string:
				dot = split_string.index('.')
				number = split_string[dot-1] + '.' + split_string[dot+1]
				return {
				'data_type': data_type,
				'variable_name': variable_name,
				'data': number
				}
			elif '.' in split_string and '(' in split_string:
				dot = split_string.index('.')
				eq = split_string.index('=')
				data_type = split_string[eq-2]
				var_name = split_string[eq-1]
				object_name = split_string[dot-1]
				function_name = split_string[dot+1]
				param_open = split_string.index('(')
				param_end = split_string.index(')') 
				params = split_string[param_open+1:param_end]
				parameters = [param for param in params if param != ',']
				return {
				'data_type': data_type,
				'var_name': var_name,
				'object_name': object_name,
				'function_name': function_name,
				'params': parameters
				}

			else:
				eq = split_string.index('=')
				data = split_string[eq+1]
				return {
				'data_type': data_type,
				'variable_name': variable_name,
				'data': data
				}

		if type == 3:
			return {
			'exc': stat
			}

		if type == 4:
			stat = stat[1:]
			return {
			'if': stat
			}

		if type == 5:
			return{
			'curly': stat
			}

		if type == 6:
			split_string = stat.split()
			dot = split_string.index('.')
			object_name = split_string[dot-1]
			function_name = split_string[dot+1]
			param_open = split_string.index('("')
			param = split_string[param_open+1]
			return {
			'object_name': object_name, 
			'function_name': function_name,
			'param': param
			}

		if type == 7:
			split_string = stat.split()
			param_open = split_string.index('(')
			param_end = split_string.index(')')
			beg = split_string[param_open-1]
			iterator = split_string[param_open+2]
			var = split_string[param_open+1]
			list_ = split_string[param_end-1]
			return {
			'beg': beg,
			'iterator': iterator,
			'list': list_,
			'var': var
			}
	
		if type == 8:
			split_string = stat.split()
			dot = split_string.index('.')
			command = split_string[dot-1]+'.'+split_string[dot+1]
			param_open = split_string.index('(')
			param_end = split_string.index(')')
			params = split_string[param_open+1:param_end]
			parameters = [param for param in params if param != ',']
			return {
			'command': command,
			'params': parameters
			}
		
		if type == 9:
			split = stat.split()
			split_string = [elem for elem in split if elem != '}']
			exc = split_string[0]
			param_open = split_string.index('(')
			param_end = split_string.index('){')
			type_ = split_string[param_open+1]
			name = split_string[param_end-1]
			return {
			'exc': exc,
			'type': type_,
			'name': name
			}


