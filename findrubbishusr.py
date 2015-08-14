import codecs;
usrt={};
usrc={};
usrl={};
usraptme={};
usr=[];
go=[];
with open('fork.txt') as f:
	for line in f:
		line=line.replace('\n',''); # VERY IMPORTANT !!!
		if line != '': #avoid empty l n e
			usraptme[line]=0;
			usr.append(line);
			usrt[line]=0;
			usrc[line]=0;
			usrl[line]=0;
#bld fork usr lst
print('finish loading');
#print(usr);
i=1;
with open('train.txt') as f:
	for line in f:
		if line != '':
			name= line.split('\t')[0];
			if name in usr:
				print('find '+str(i));
				i=i+1;
				usraptme[name]=usraptme[name]+1; #add
				split=line.split('\t');
				usrt[name]=int(usrt[name])+int(split[3]);
				usrc[name]=int(usrc[name])+int(split[4]);
				usrl[name]=int(usrl[name])+int(split[5]);
count=1;
for user in usr:
	if (int(usrt[user])/int(usraptme[user])) < 2:
		if (int(usrc[user])/int(usraptme[user])) < 2:
			if (int(usrl[user])/int(usraptme[user])) < 2:
				print(count);
				count=count+1;
				go.append(user);
with codecs.open('rubbishuser.txt','a','utf8') as c:
	for goal in go:
		c.write(goal+'\n');
#by DGideas
