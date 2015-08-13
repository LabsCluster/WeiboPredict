#!/usr/bin/env python3
__author__='DGideas';
#Release:Dorado
import sys;
import fileinput;
import codecs;
i=1;
with open('predict.txt') as f:
	for line in f:
		print(str(i));
		i=i+1;
