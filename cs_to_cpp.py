from keywords import KEYWORDS, KEYWORDS_DATA

class CsToCpp():
	def __init__(self):
		self.class_def = ''
		self.body = []

	def convert_class_header(self, access, return_type, name, params):
		class_header = '%s %s %s'%(KEYWORDS[access], KEYWORDS[return_type], KEYWORDS[name])
		parameters = ''
		for param in params:
			if param in KEYWORDS:
				parameters+=KEYWORDS[param]
				parameters+=' '
				continue
			if param not in KEYWORDS and param != params[-1]:
				parameters+=param
				parameters+=', '
			if param == params[-1]:
				parameters+=param
		class_def = class_header + ' (' + parameters + '){'
		self.class_def = class_def

	def constructor(self, stat):
		const_stat = '%s %s('%(stat['class_name'], stat['variable_name'])
		params = stat['params']
		for param in params:
			if param == params[-1]:
				const_stat += '' + param + ');'
			else:
				const_stat += '' + param + ', '
		self.body.append(const_stat)

	def data_init(self, stat):
		const_stat = '%s %s = %s;'%(stat['data_type'], stat['variable_name'], stat['data'])
		self.body.append(const_stat)

	def try_block(self, stat):
		self.body.append(stat['exc'])


	def object_init(self, stat):
		const_stat = '%s %s = %s.%s('%(stat['data_type'], stat['var_name'], stat['object_name'], stat['function_name'])
		params = stat['params']
		for param in params:
			if param == params[-1]:
				const_stat += '' + param + ');'
			else:
				const_stat += '' + param + ', ' 
		self.body.append(const_stat)

	def if_case(self, stat):
		const_stat = stat['if']
		self.body.append(const_stat)

	def add_curly(self, stat):
		const_stat = stat['curly']
		self.body.append(const_stat)

	def add_list(self, stat):
		const_stat = '%s<%s> %s;'%(KEYWORDS[stat['data_struct']], KEYWORDS_DATA['string'], stat['variable_name'])
		self.body.append(const_stat)

	def add_vec(self, stat):
		const_stat = '%s.%s("%s");'%(stat['object_name'], KEYWORDS[stat['function_name']], stat['param'])
		self.body.append(const_stat)

	def for_loop(self, stat):
		const_stat = '%s(%s %s : %s)'%(KEYWORDS[stat['beg']], KEYWORDS[stat['var']], stat['iterator'], stat['list'])
		self.body.append(const_stat)

	def cout(self, stat):
		options = KEYWORDS[stat['command']]
		const_stat = '%s << %s << %s;'%(options[0], stat['params'][0], options[1])
		self.body.append(const_stat)

	def catch(self, stat):
		const_stat = '%s(%s %s){'%(KEYWORDS[stat['exc']], KEYWORDS[stat['type']], stat['name'])
		self.body.append(const_stat)

	def find_type(self, stat):
		split_string = stat.split()
		try:
			eq = split_string.index('=')
			# case for constructor call
			if split_string[eq+1] == 'new':
				return 1

		# case for data variable assignment
			if split_string[0] in KEYWORDS_DATA.keys():
				key = KEYWORDS_DATA[split_string[0]]
				return 2
		except:
			pass
		
		# case for try
		try:
			t = split_string.index('try')
			return 3
		except:
			pass

		# case for if case
		if 'if' in split_string:
			return 4

		# case for {
		if '{' in split_string:
			return 5

		# case for vector addition
		if 'Add' in split_string:
			return 6

		# for loop
		if 'foreach' in split_string:
			return 7

		if 'Console' in split_string:
			return 8

		if 'catch' in split_string:
			return 9




		

