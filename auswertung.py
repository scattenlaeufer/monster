#!/usr/bin/python2

import sys, os
from helpers.dialog import ProbCodeDialog, PreSetDialog
from PyQt4 import QtGui

app = QtGui.QApplication(sys.argv)
prob_dia = ProbCodeDialog()
prob_code = prob_dia.ask()

preset_dia = PreSetDialog()
preset = preset_dia.ask()

prob_file = os.path.join('helpers','trial_log',prob_code,'morse1','test')

with open(os.path.join('helpers','trial_log',prob_code,'morse1','in'),'r') as file:
	_input = file.read()

y = []
_input_line = _input.split('\n')
for i in _input_line:
	if i != '':
		if '\r' in i:
			i = i[:-1]
		y_str = i.split('.')
		y_a = y_str[1].split(',')
		y.append(int(y_str[0])*60 + int(y_a[0]) + float(y_a[1]) /(10**len(y_a[1])))

with open(prob_file,'r') as file:
	data = file.read()

data_lines = data.split('\n')

output = data_lines[0] + '_m\ttime_r\ttime_response\n'

n = 0

for line in data_lines:
	line_data = line.split('\t')
	if not (line_data[0] == '' or line_data[0] == 'trial'):
		if line_data[-1] == '' or line_data[-1] == '\r':
			line_data = line_data[:-1]
#		print(line_data)
		x = float(line_data[3]) + preset
		print(str(y[n]) + '\t' + str(x) + '\t' + str(float(line_data[3])) + '\t' + str(preset))
		line_data.append(y[n])
#		print(y[n])
		line_data.append(str(y[n] - x))
		line_out = ''
#		print('\n')
		for i in line_data:
			line_out += str(i) + '\t'
#			print(i)
#		print('\n')
#		print(line_out + '\n')
		output += line_out + '\n'
		n += 1

print(output)

with open(prob_file+'_resptime','w') as file:
	file.write(output)
