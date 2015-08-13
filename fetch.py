#!/usr/bin/env python3
__author__='DGideas';
#Release:Dorado
import DGStorage as DGS;
import sys;
import fileinput;
s=DGS.DGStorage();
s.createdb('/root/weibo/WeiboPredict/train');
s.selectdb('/root/weibo/WeiboPredict/train');
i=1;
with open('train.txt') as f:
	for line in f:
		split=line.split('\t');
		print(i);
		i=i+1;
		s.add(split[1],line);