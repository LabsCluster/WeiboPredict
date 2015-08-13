import codecs;
with codecs.open('predict.txt','r','utf8') as f:
	f=f.readlines()[0].split('\t');
	print(f);