# -*- coding: utf-8 -*-
from PyQt4 import QtGui
import sys

class ProbCodeDialog(QtGui.QWidget):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)

	def ask(self):
		text, ok = QtGui.QInputDialog.getText(self, 'Probandencode', 'Probandencode:')

		if ok:
			if text == '':
				return 'test'
			else:
				return str(text)
		else:
			exit()


class OverwriteDialog(QtGui.QWidget):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)

	def ask(self):
		reply = QtGui.QMessageBox.question(self, u'Überschreiben?', u"Willst du die vorhandenen\nProbandendaten überschreiben?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
		if reply != QtGui.QMessageBox.Yes:
			exit()
