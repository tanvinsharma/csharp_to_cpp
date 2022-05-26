from cs_syntax import CSClass
from cs_to_cpp import CsToCpp
from read_file import read_file
import sys

program_name = sys.argv[0]
arguments = sys.argv[1:]
print('File executed:', program_name)
print('File passed: ', arguments)
cs_file = arguments[0]
keywords_found = read_file(cs_file)
cpp_bodies = []
for file in arguments:
    cs = CSClass(keywords_found)

    statements = cs.statements
    cs.clean_statements(statements)

    cpp = CsToCpp()
    # header parsed
    cpp.convert_class_header(cs.class_access, cs.class_return, cs.class_name, cs.params)

    # total_statements = len(statements)
    # for i in range(total_statements):
    #     try:
    #         closed = []
    #         if '}' in statements[i]:
    #             for i, elem in enumerate(statements[i]):
    #                 if elem == '}':
    #                     closed.append(i)
    #         no_of_brackets = len(closed)
    #         brack = ''
    #         for i in range(no_of_brackets):
    #             brack += '} \n '
    #         cpp.body.append(brack)
    #     except:
    #         pass
    #     type = cpp.find_type(statements[i])
    #     stat = cs.return_data_of_statement(type, statements[i])
    #     if type == 1:
    #         try:
    #             cpp.constructor(stat)
    #         except:
    #             pass
    #         try:
    #             cpp.add_list(stat)
    #         except:
    #             pass
    #     if type == 2:
    #         try:
    #             cpp.data_init(stat)
    #         except:
    #             pass
    #         try:
    #             cpp.object_init(stat)
    #         except:
    #             pass
    #     if type == 3:
    #         cpp.try_block(stat)
    #     if type == 4:
    #         cpp.if_case(stat)
    #     if type == 5:
    #         cpp.add_curly(stat)
    #     if type == 6:
    #         cpp.add_vec(stat)
    #     if type == 7:
    #         cpp.for_loop(stat)
    #     if type == 8:
    #         cpp.cout(stat)
    #     if type == 9:
    #         cpp.catch(stat)

    # final_body = [elem for elem in cpp.body if elem != '\0']
    # print(final_body)
    type = cpp.find_type(statements[0])
    stat = {}
    if type == 1:
        stat = cs.return_data_of_statement(1, statements[0])
        cpp.constructor(stat)

    type = cpp.find_type(statements[1])
    stat = {}
    if type == 2:
        stat = cs.return_data_of_statement(2, statements[1])
        cpp.data_init(stat)

    type = cpp.find_type(statements[2])
    stat = {}
    if type == 3:
        stat = cs.return_data_of_statement(3, statements[2])
        cpp.try_block(stat)

    type = cpp.find_type(statements[3])
    stat = {}
    if type == 2:
        stat = cs.return_data_of_statement(2, statements[3])
        cpp.object_init(stat)

    type = cpp.find_type(statements[4])
    stat = {}
    if type == 4:
        stat = cs.return_data_of_statement(4, statements[4])
        cpp.if_case(stat)

    type = cpp.find_type(statements[5])
    stat = {}
    if type == 5:
        stat = cs.return_data_of_statement(5, statements[5])
        cpp.add_curly(stat)

    type = cpp.find_type(statements[6])
    stat = {}
    if type == 1:
        stat = cs.return_data_of_statement(1, statements[6])
        cpp.add_list(stat)

    type = cpp.find_type(statements[7])
    stat = {}
    if type == 6:
        stat = cs.return_data_of_statement(6, statements[7])
        cpp.add_vec(stat)

    type = cpp.find_type(statements[8])
    stat = {}
    if type == 6:
        stat = cs.return_data_of_statement(6, statements[8])
        cpp.add_vec(stat)

    type = cpp.find_type(statements[9])
    stat = {}
    if type == 6:
        stat = cs.return_data_of_statement(6, statements[9])
        cpp.add_vec(stat)

    type = cpp.find_type(statements[10])
    stat = {}
    if type == 6:
        stat = cs.return_data_of_statement(6, statements[10])
        cpp.add_vec(stat)

    type = cpp.find_type(statements[11])
    stat = {}
    if type == 7:
        stat = cs.return_data_of_statement(7, statements[11])
        cpp.for_loop(stat)

    type = cpp.find_type(statements[12])
    stat = {}
    if type == 5:
        stat = cs.return_data_of_statement(5, statements[12])
        cpp.add_curly(stat)

    type = cpp.find_type(statements[13])
    stat = {}
    if type == 8:
        stat = cs.return_data_of_statement(8, statements[13])
        cpp.cout(stat)

    type = cpp.find_type(statements[14])
    stat = {}

    closed = []
    if '}' in statements[14]:
        for i, elem in enumerate(statements[14]):
            if elem == '}':
                closed.append(i)
    no_of_brackets = len(closed)
    brack = ''
    for i in range(no_of_brackets):
        brack += '} \n '
    cpp.body.append(brack)
    # print(cpp.body)

    if type == 9:
        stat = cs.return_data_of_statement(9, statements[14])
        cpp.catch(stat)

    type = cpp.find_type(statements[15])
    stat = {}
    if type == 8:
        stat = cs.return_data_of_statement(8, statements[13])
        cpp.cout(stat)

    closed = []
    if '}' in statements[14]:
        for i, elem in enumerate(statements[16]):
            if elem == '}':
                closed.append(i)
    no_of_brackets = len(closed)
    brack = ''
    for i in range(no_of_brackets):
        brack += '} \n '
    cpp.body.append(brack)

    cpp_bodies.append(cpp.body)

for i, body in enumerate(cpp_bodies):
    cpp_file = open("cpp_test_%d.cpp"%(i), "w")
    cpp_file.write(cpp.class_def + '\n')
    for element in body:
        if element[-1] == ';':
            cpp_file.write(element + '\n')
        else:
            cpp_file.write(element)


