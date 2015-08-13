#!/usr/bin/env python3
__author__='DGideas';
import sys;
import fileinput;
import codecs;
r=codecs.open('weibo_result_data.txt','a','utf8');
i=1
with open('predict.txt') as f:
	for line in f:
		split=line.split('\t');
		r.write(split[0]+'\t'+split[1]+'\t'+'0,0,0'+'\n');
		print(i);
		i=i+1;