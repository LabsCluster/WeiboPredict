import codecs;
usr=[];
thisusr=[];
i=0;
newusr=0;
newusrarray=[];
p=codecs.open('fork.txt','a','utf8');
with open('upredict.txt') as f:
	for line in f:
		try:
			usr.append(line); #Put predict user to memory
		except:
			print('Fetch an error');
			pass; #avoid the last line 
with open('utrain.txt') as f:
	for line in f:
		if line!='':
			if line in usr:
				if line not in thisusr:
					print(i);
					i=i+1;
					line=line.replace('\n',''); # this is a very serious problem
					p.write(line+'\n');
					thisusr.append(line); #note this usr
				else:
					pass;
			else:
				if line not in newusrarray:
					newusr=newusr+1;
					newusrarray.append(line); # note new usr
	print('Newusr is '+str(newusr));