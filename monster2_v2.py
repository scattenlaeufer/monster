#!/usr/bin/python2

import argparse
from level.stages import Monster2_V2

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='the second version of monster1')
	parser.add_argument('--debug',action='store_true',default=False,help='run in debug mode')
	args = parser.parse_args()

	monster = Monster2_V2(debug=args.debug)
