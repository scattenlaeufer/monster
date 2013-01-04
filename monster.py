#!/usr/bin/python2

import sys
from level.stages import Monster1

if __name__ == '__main__':
	if len(sys.argv) > 1:
		probcode = sys.argv[len(sys.argv)-1]
	else:
		probcode = 'test'
	monster = Monster1(probcode)
