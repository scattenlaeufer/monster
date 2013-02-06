#!/usr/bin/python2

import sys
from level.stages import Monster3

if __name__ == '__main__':
	if len(sys.argv) > 1:
		probcode = sys.argv[len(sys.argv)-1]
	else:
		probcode = 'test'
	monster = Monster3(probcode)
