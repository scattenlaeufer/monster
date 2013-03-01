import time, string, os, sys
from PyQt4 import QtGui
from dialog import ProbCodeDialog, OverwriteDialog
# -*- coding: utf-8 -*-

class Log_Tester:

	def __init__(self,prob_code,level):
		log_file = os.path.join(__file__[:-7],'trial_log/',prob_code,level)
		if os.path.isfile(log_file):
			app = QtGui.QApplication(sys.argv)
			overwrite = OverwriteDialog()
			overwrite.ask()

class Monster_Logger:

	def __init__(self,level,prob_code=''):
		self.log = ''
		if prob_code == '':
			probDialog = ProbCodeDilog()
			prob_code = probDialog.ask()
		prob_dir = os.path.join(__file__[:-7],'trial_log/',prob_code)
		self.log_file = os.path.join(prob_dir,level)
		if os.path.isdir(prob_dir):
			if os.path.isfile(self.log_file):
				app = QtGui.QApplication(sys.argv)
				overwrite = OverwriteDialog()
				overwrite.ask()
		else:
			trial_dir = os.path.join(__file__[:-7],'trial_log')
			if not os.path.isdir(trial_dir):
				os.mkdir(trial_dir)
			os.mkdir(prob_dir)

	def save(self):
		with open(self.log_file,mode='w') as f:
			f.write(self.log)

	def add(self,entry):
		self.log += '\n'
		for i in entry:
			self.log += '\t' + str(i)
		self.save()

	def set_top(self,top):
		self.log += top
		self.save()
