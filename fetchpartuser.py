#!/usr/bin/env python3
__author__='DGideas';
#Release:Dorado
import sys;
import fileinput;
import codecs;
i=1;
u=codecs.open('upredict.txt','a','utf8');
ucache=[];
with open('predict.txt') as f:
	for line in f:
		split=line.split('\t');
		if split[0] not in ucache:
			ucache.append(split[0]);
			u.write(split[0]+'\n');
			print(str(i));
			i=i+1
