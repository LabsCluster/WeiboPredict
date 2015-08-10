#!/usr/bin/env python3
__author__='DGideas';
#Release:Dorado

try:
	os.chdir(os.path.dirname(sys.argv[0]));
except FileNotFoundError:
	pass;
except OSError:
	pass;

class DGStorage:
	def __init__(self):
		import os;
		import sys;
		import codecs;
		import uuid;
		import urllib.parse;
		
		self.query=[];
		self.database='';
		self.conf={};
		self.coll=[];
		self.optcache={};
		self.keycache=[];
		self.LTkeycache=[]; #键值长期缓存
		self.uidcache=[];
		
	def selectdb(self,database):
		import os;
		import sys;
		import codecs;
		import uuid;
		import urllib.parse;
		
		try:
			open(database+'/conf.dgb','r');
		except FileNotFoundError:
			return False;
		else:
			with codecs.open(database+'/conf.dgb','r','utf8') as conf:
				for line in conf.readlines():
					config=line.split(':');
					self.conf[config[0]]=config[1];
				self.database=database;
		return True;

	def createdb(self,database):
		import os;
		import sys;
		import codecs;
		import uuid;
		import urllib.parse;
		
		try:
			open(database+'/conf.dgb','r');
		except FileNotFoundError:
			with codecs.open(database+'/conf.dgb','a','utf8') as conf:
				os.chdir(database);
				self.database=database
				os.mkdir('index');
				self.createcoll(0);
				conf.write('databaseid:'+str(uuid.uuid1()));
				conf.write('\ndatabaseversion:1.0');
			return True;
		else:
			return False;

	def add(self,key,content):
		import os;
		import sys;
		import codecs;
		import uuid;
		import urllib.parse;
		
		self.clche();
		key=urllib.parse.quote_plus(key);
		try:
			codecs.open(self.database+'/index/index.dgi','r','utf8');
		except FileNotFoundError:
			return False;
		else:
			with codecs.open(self.database+'/index/index.dgi','r','utf8') as index:
				for line in index.readlines():
					line=line.replace('\n',''); #去除换行符
					self.coll.append(str(line));
				for collection in self.coll:
					try:
						self.optcache['coll'];
					except KeyError:
						try:
							codecs.open(self.database+'/'+collection+'/index/index.dgc','r','utf8');
						except FileNotFoundError:
							return False;
						else:
							with codecs.open(self.database+'/'+collection+'/index/index.dgc','r','utf8') as docindex:
								if len(docindex.readlines())<1024:
									self.optcache['coll']=collection; #目的集合选择器
					else:
						pass;
					with codecs.open(self.database+'/'+collection+'/index/index.dgc','r','utf8') as docindex:
						r=docindex.readlines();
						if len(r)==0:
							continue;
						else:
							if r[0].split(',')[1] not in self.LTkeycache: #长期缓存机制
								for line in docindex.readlines():
									self.keycache.append(line.split(',')[1]);
									self.LTkeycache.append(line.split(',')[1]);
				if key not in self.LTkeycache:
					try:
						self.optcache['coll'];
					except KeyError:
						self.LTkeycache.append(key);
						addcollid=int(self.coll[-1])+1;
						self.createcoll(addcollid);
						self.optcache['coll']=str(addcollid);
						uid=uuid.uuid1();
						with codecs.open(self.database+'/'+self.optcache['coll']+'/index/index.dgc','a','utf8') as docindex:
							with codecs.open(self.database+'/'+self.optcache['coll']+'/index/index.dgc','r','utf8') as docindexr:
								data=codecs.open(self.database+'/'+self.optcache['coll']+'/'+str(uid)+'.dgs','w','utf8');
								if len(docindexr.readlines())==0:
									docindex.write(str(uid)+','+key);
								else:
									docindex.write('\n'+str(uid)+','+key);
								data.write(content);
								return True;
					else:
						self.LTkeycache.append(key);
						uid=uuid.uuid1();
						with codecs.open(self.database+'/'+self.optcache['coll']+'/index/index.dgc','a','utf8') as docindex:
							with codecs.open(self.database+'/'+self.optcache['coll']+'/index/index.dgc','r','utf8') as docindexr:
								data=codecs.open(self.database+'/'+self.optcache['coll']+'/'+str(uid)+'.dgs','w','utf8');
								if len(docindexr.readlines())==0:
									docindex.write(str(uid)+','+key);
								else:
									docindex.write('\n'+str(uid)+','+key);
								data.write(content);
								#垃圾回收
								index.close();
								docindex.close();
								docindexr.close();
								data.close();
								return True;
				else:
					return False;

	def get(self,key):
		import os;
		import sys;
		import codecs;
		import uuid;
		import urllib.parse;
		
		self.clche();
		key=urllib.parse.quote_plus(key);
		with codecs.open(self.database+'/index/index.dgi','r','utf8') as index:
			for line in index.readlines():
				line=line.replace('\n',''); #去除换行符
				self.coll.append(str(line));
			for collection in self.coll:
				with codecs.open(self.database+'/'+collection+'/index/index.dgc','r','utf8') as docindex:
					for line in docindex.readlines():
						line=line.replace('\n','');
						linesplit=line.split(',');
						if key==linesplit[1]:
							with codecs.open(self.database+'/'+collection+'/'+str(linesplit[0])+'.dgs','r','utf8') as cont:
								return cont.read();
		return False;
				
	def put(self,key,content):
		import os;
		import sys;
		import codecs;
		import uuid;
		import urllib.parse;
		
		self.clche();
		key=urllib.parse.quote_plus(key);
		with codecs.open(self.database+'/index/index.dgi','r','utf8') as index:
			for line in index.readlines():
				line=line.replace('\n',''); #去除换行符
				self.coll.append(str(line));
			for collection in self.coll:
				with codecs.open(self.database+'/'+collection+'/index/index.dgc','r','utf8') as docindex:
					for line in docindex.readlines():
						line=line.replace('\n','');
						linesplit=line.split(',');
						if key==linesplit[1]:
							with codecs.open(self.database+'/'+collection+'/'+str(linesplit[0])+'.dgs','w','utf8') as cont:
								cont.write(content);
								return True;
		return False;
		
	def remove(self,key):
		import os;
		import sys;
		import codecs;
		import uuid;
		import urllib.parse;
		
		self.clche();
		key=urllib.parse.quote_plus(key);
		with codecs.open(self.database+'/index/index.dgi','r','utf8') as index:
			for line in index.readlines():
				line=line.replace('\n',''); #去除换行符
				self.coll.append(str(line));
			for collection in self.coll:
				with codecs.open(self.database+'/'+collection+'/index/index.dgc','r','utf8') as docindex:
					for line in docindex.readlines():
						line=line.replace('\n','');
						linesplit=line.split(',');
						if key==linesplit[1]:
							os.remove(self.database+'/'+collection+'/'+str(linesplit[0])+'.dgs');
							with codecs.open(self.database+'/'+collection+'/index/index.dgc','r','utf8') as docindexr:
								for record in docindexr.readlines():
									record=record.replace('\n','');
									record=record.split(',');
									if record[1]==key:
										pass;
									else:
										self.keycache.append(record[1]);
										self.uidcache.append(record[0]);
								i=1;
								with codecs.open(self.database+'/'+collection+'/index/index.dgc','w','utf8') as indexb:
									indexb.write('');
									while i<=len(self.uidcache):
										with codecs.open(self.database+'/'+collection+'/index/index.dgc','a','utf8') as indexc:
											with codecs.open(self.database+'/'+collection+'/index/index.dgc','r','utf8') as indexr:
												if len(indexr.readlines())==0:
													indexc.write(str(self.uidcache[i-1])+','+str(self.keycache[i-1]));
												else:
													indexc.write('\n'+str(self.uidcache[i-1])+','+str(self.keycache[i-1]));
												i=i+1;
									with codecs.open(self.database+'/'+collection+'/index/index.dgc','r','utf8') as dgcfile:
										if (dgcfile.readlines())==[]:
											self.removecoll(collection);
									return True;
		return False;

	##################################################
	#以下方法无需在外部调用
	def clche(self):
		import os;
		import sys;
		import codecs;
		import uuid;
		import urllib.parse;
		
		self.optcache={};
		self.keycache=[];
		self.uidcache=[];
		self.coll=[];

	def createcoll(self,coll):
		import os;
		import sys;
		import codecs;
		import uuid;
		import urllib.parse;
		
		os.chdir(self.database);
		os.mkdir(str(coll));
		os.mkdir(str(coll)+'/index');
		collindex=codecs.open(self.database+'/'+str(coll)+'/index/index.dgc','a','utf8');
		index=codecs.open(self.database+'/index/index.dgi','a','utf8');
		indexr=codecs.open(self.database+'/index/index.dgi','r','utf8');
		if len(indexr.readlines())==0:
			index.write(str(coll));
		else:
			index.write('\n'+str(coll));
		#垃圾回收
		index.close();
		indexr.close();
		
	def removecoll(self,coll):
		import os;
		import sys;
		import codecs;
		import uuid;
		import urllib.parse;
		
		os.chdir(self.database);
		os.remove(self.database+'/'+str(coll)+'/index/index.dgc');
		os.rmdir(self.database+'/'+str(coll)+'/index');
		os.rmdir(self.database+'/'+str(coll));
		return True;
