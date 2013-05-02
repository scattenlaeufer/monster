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

with open(prob_file,'r') as file:
	data = file.read()

data_lines = data.split('\n')

output = data_lines[0] + '\n'

for line in data_lines:
	line_data = line.split('\t')
	if not (line_data[0] == '' or line_data[0] == 'trial'):
		x = float(line_data[3]) + preset
		y_str = line_data[4].split('.')
		y_a = y_str[1].split(',')
		y = int(y_str[0])*60 + int(y_a[0]) + float(y_a[1]) /(10*len(y_a[1]))
		line_data.append(str(y - x))
		line_out = ''
		for i in line_data:
			line_out += str(i) + '\t'
		output += line_out + '\n'


with open(prob_file+'_resptime','w') as file:
	file.write(output)
