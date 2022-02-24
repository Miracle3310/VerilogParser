#!/usr/bin/python

import re
import os

# regex compile
regex_module = re.compile('(module)(\s+)(\w+)')

regex_ports = re.compile('''
(input|output)        #0
(\s+)                 #1
(wire|reg\s+)?        #2
(\[\w+\-1\:0\]\s+)?   #3
(\w+)                 #4
''', re.VERBOSE)

directory = os.getcwd()
# open the design file
file_design = input('Please enter the file name:')
with open(directory+'/'+file_design, 'r') as file_obj:
    comment = file_obj.read()

# regex match module name
module_obj = regex_module.search(comment)
print(module_obj.group())
# regex match ports name
groups_ports = regex_ports.findall(comment)
print('\nnumber of ports:', len(groups_ports))

# write the instantiation templete to an assigned file
file_tb = input('Please enter the top file name:')
with open(directory+'/'+file_tb, 'a') as file_obj2:
    if module_obj is not None:
        file_obj2.write(module_obj.group(3)+' uut\n(\n')

        num = len(groups_ports)
        for i in range(num):
            if i == num-1:
                file_obj2.write('.'+groups_ports[i][4]+'  ()\n')
            else:
                file_obj2.write('.'+groups_ports[i][4]+'  (),\n')
        file_obj2.write(');\n')
