# -*- coding: utf-8 -*-
from PyQt4 import QtGui
import sys

class ProbCodeDialog(QtGui.QWidget):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)

	def ask(self):
		text, ok = QtGui.QInputDialog.getText(self, 'Probandencode', 'Probandencode:')

		if ok:
			if str(text) == '':
				return 'test'
			else:
				return str(text)
		else:
			exit()


class PreSetDialog(QtGui.QWidget):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)

	def ask(self):
		text, ok = QtGui.QInputDialog.getText(self, 'Preset', 'Wann kam "ta"? (min.s,ms)')

		if ok:
			if text == '':
				return 0
			else:
				s = str(text).split('.')
				s1 = s[1].split(',')
				sa = int(s[0])*60
				sb = int(s1[0])
				sc = float(s1[1])/(10**len(s1[1]))
				s2 = sa + sb + sc
				#print(str(text) + '\t' + str(sa) + '\t' + str(sb) + '\t' + str(sc) + '\t' + str(s2))
				return s2
		else:
			exit()


class OverwriteDialog(QtGui.QWidget):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)

	def ask(self):
		reply = QtGui.QMessageBox.question(self, u'Überschreiben?', u"Willst du die vorhandenen\nProbandendaten überschreiben?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
		if reply != QtGui.QMessageBox.Yes:
			exit()
