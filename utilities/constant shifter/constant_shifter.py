import sys
sys.dont_write_bytecode = True

from os.path import split as path_split, exists as path_exists

print('Every slot number in "module_constants.py" will be shifted by 1.')
print('Type start line and end line. Numbering lines started at 1. The end line will be including.')

start, end = map(int, input("Input start and end line separated by space:").split())

with open('module_constants.py', "r", encoding='utf-8') as file:
	lines = file.readlines()
with open('module_constants_back.py', "w", encoding='utf-8') as file:
	file.writelines(lines)

start -= 1
for i in range(start, end):
	s = lines[i]
	array = s.split()
	if type(array) is list:
		if len(array) > 1:
			if array[1] == "=":
				slot = int(array[2])
				lines[i] = s.replace(str(slot), str(slot + 1), 1)

with open('module_constants.py', "w", encoding='utf-8') as file:
	file.writelines(lines)
