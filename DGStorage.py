#!/usr/bin/env python3
__author__='DGideas';
#Document:https://github.com/DGideas/DGStorage/wiki

class DGStorage:
	def __init__(self,conf={}):
		import os;
		import sys;
		
		self.DGSTORAGE_VERSION='2.2';
		self.DGSTORAGE_CHARSET='utf8';
		self.DGSTORAGE_SINGLECOLLECTIONLIMIT=1024;
		self.DGSTORAGE_SEARCHRANGE=3;
		self.DGSTORAGE_SEARCHINDEXLIMIT=32;
		self.DGSTORAGE_SEARCHCACHELIMIT=32;
		self.DGSTORAGE_PROPCACHELIMIT=32;
		self.DGSTORAGE_SAFETY=True;
		
		self.DGSTORAGE_Name=None;
		self.DGSTORAGE_TimeStamp='';
		
		self.CollectionCache=[];
		self.LastCollection='';
		self.SearchCache=[];
		
		try:
			os.chdir(os.path.dirname(sys.argv[0]));
		except FileNotFoundError:
			pass;
		except OSError:
			pass;

	def create(self,name):
		import codecs;
		import uuid;
		import urllib.parse;
		import os;
		self.DGSTORAGE_Name=str(name);
		if self.DGSTORAGE_SAFETY==True:
			self.DGSTORAGE_Name=urllib.parse.quote_plus(self.DGSTORAGE_Name);
		try:
			os.mkdir(self.DGSTORAGE_Name);
		except FileExistsError:
			return False;
		else:
			self.DGSTORAGE_Name=self.DGSTORAGE_Name;
			self.DGSTORAGE_Name=name;
			with codecs.open(self.DGSTORAGE_Name+'/conf.dgb','a',self.DGSTORAGE_CHARSET) as conf:
				conf.write(str(uuid.uuid1())+'\n');
				conf.write('Version:'+self.DGSTORAGE_VERSION);
			os.mkdir(self.DGSTORAGE_Name+'/index');
			with codecs.open(self.DGSTORAGE_Name+'/index/index.dgi','a',self.DGSTORAGE_CHARSET) as index:
				pass;
			os.mkdir(self.DGSTORAGE_Name+'/cache');
			os.mkdir(self.DGSTORAGE_Name+'/cache/search');
			os.mkdir(self.DGSTORAGE_Name+'/cache/prop');
			self.uptmp();
			return True;
	
	def select(self,name):
		import urllib.parse;
		import os;
		self.DGSTORAGE_Name=str(name);
		if self.DGSTORAGE_SAFETY==True:
			self.DGSTORAGE_Name=urllib.parse.quote_plus(self.DGSTORAGE_Name);
		try:
			os.mkdir(self.DGSTORAGE_Name);
		except FileExistsError:
			self.DGSTORAGE_Name=name;
			with open(self.DGSTORAGE_Name+'/conf.dgb') as conf:
				correctVersion=False;
				for line in conf:
					if line.find('Version:2')!=-1:
						correctVersion=True;
				if correctVersion==False:
					return False;
			with open(self.DGSTORAGE_Name+'/index/index.dgi') as index:
				for line in index:
					line=line.replace('\n','');
					if line!='':
						self.CollectionCache.append(str(line));
			with open(self.DGSTORAGE_Name+'/cache/time.dgb') as cacheTimeStamp:
				self.DGSTORAGE_TimeStamp=cacheTimeStamp.read();
			return len(self.CollectionCache);
		else:
			os.rmdir(self.DGSTORAGE_Name);
			return False;
	
	def append(self,content):
		import uuid;
		return self.add(str(uuid.uuid1()),content,{"method":"append"});
	
	def add(self,key,content,prop={},insertuid=None,rawProp=None):
		import codecs;
		import uuid;
		import urllib.parse;
		key=str(key).replace('\n','');
		key=urllib.parse.quote_plus(str(key));
		operationCollection='';
		if key=='':
			return False;
		if len(self.CollectionCache)==0:
			if (self.createcoll(0)):
				operationCollection=0;
			else:
				return False;
		else:
			if self.LastCollection!='':
				with open(self.DGSTORAGE_Name+'/'+str(self.LastCollection)+'/index/index.dgi') as collIndex:
					i=0;
					for line in collIndex:
						if line!='':
							i+=1;
					if i<self.DGSTORAGE_SINGLECOLLECTIONLIMIT:
						operationCollection=self.LastCollection;
					else:
						operationCollection=self.findavailablecoll(True);
			else:
				operationCollection=self.findavailablecoll(True);
		self.LastCollection=operationCollection;
		uid='';
		with codecs.open(self.DGSTORAGE_Name+'/'+str(operationCollection)+'/index/index.dgi','a',self.DGSTORAGE_CHARSET) as collIndex:
			collIndexR=open(self.DGSTORAGE_Name+'/'+str(operationCollection)+'/index/index.dgi');
			i=0;
			for line in collIndexR:
				if line!='' and line!='\n':
					i+=1;
			collIndexR.close();
			if insertuid==None:
				uid=uuid.uuid1();
			else:
				uid=insertuid;
			if i==0:
				collIndex.write(str(uid)+','+str(key));
			else:
				collIndex.write('\n'+str(uid)+','+str(key));
		with codecs.open(self.DGSTORAGE_Name+'/'+str(operationCollection)+'/'+str(uid)+'.dgs','a',self.DGSTORAGE_CHARSET) as storage:
			storage.write(str(content));
		if len(prop)!=0:
			with codecs.open(self.DGSTORAGE_Name+'/'+str(operationCollection)+'/'+str(uid)+'.dgp','a',self.DGSTORAGE_CHARSET) as storageProp:
				for propItem in prop:
					propItem=urllib.parse.quote_plus(str(propItem));
					prop[propItem]=urllib.parse.quote_plus(str(prop[propItem]));
					storageProp.write(str(propItem)+':'+str(prop[propItem])+'\n');
		if insertuid!=None and rawProp!=None:
			with codecs.open(self.DGSTORAGE_Name+'/'+str(operationCollection)+'/'+str(uid)+'.dgp','a',self.DGSTORAGE_CHARSET) as storageProp:
				storageProp.write(rawProp);
		self.uptmp();
		return uid;
	
	def index(self,key):
		return self.get(key);
	
	def count(self,key):
		return len(self.get(key));
	
	def get(self,key,limit=-1,skip=0):
		return self.finditemviakey(key,limit,skip);
	
	def fetch(self,limit=5,skip=0):
		return self.finditemviakey('$all',limit,skip);
		
	def uid(self,uid):
		return self.finditemviauid(uid);
	
	def search(self,keyword,cache=False):
		import codecs;
		res=[];
		for collection in self.CollectionCache:
			with open(self.DGSTORAGE_Name+'/'+str(collection)+'/index/index.dgi') as collIndex:
				for line in collIndex:
					line=line.replace('\n','');
					if line!='':
						split=line.split(',');
						with codecs.open(self.DGSTORAGE_Name+'/'+str(collection)+'/'+str(split[0])+'.dgs','r','utf8') as storage:
							if storage.read().find(str(keyword))!=-1:
								res.append(self.finditemviauid(split[0],str(collection)));
		return res;
	
	def pervious(self,uid):
		pervious='';
		for collection in self.CollectionCache:
			with open(self.DGSTORAGE_Name+'/'+str(collection)+'/index/index.dgi') as collIndex:
				for line in collIndex:
					line=line.replace('\n','');
					if line!='':
						split=line.split(',');
						if split[0]==uid:
							if pervious!='':
								return pervious;
							else:
								with open(self.DGSTORAGE_Name+'/'+str(self.CollectionCache[-1])+'/index/index.dgi') as lastColl:
									lastUid='';
									for line in lastColl:
										line=line.replace("\n","");
										if line!='':
											lastUid=line;
									return line.split(",")[0];
						else:
							pervious=split[0];
		return False;
	
	def following(self,uid):
		follow='';
		find=False;
		for collection in self.CollectionCache:
			with open(self.DGSTORAGE_Name+'/'+str(collection)+'/index/index.dgi') as collIndex:
				for line in collIndex:
					line=line.replace('\n','');
					if line!='':
						split=line.split(',');
						if split[0]==uid:
							find=True;
						else:
							if find==True:
								return split[0];
		with open(self.DGSTORAGE_Name+'/'+str(self.CollectionCache[0])+'/index/index.dgi') as firstColl:
			for line in firstColl:
				if line!='':
					return line.split(",")[0];
	
	def sort(self,propItem,order="ASC",limit=5,skip=0):
		import urllib.parse;
		import os;
		propItem=str(propItem);
		propItem=urllib.parse.quote_plus(propItem);
		sortArray=[];
		res=[];
		if skip<0:
			skip=0;
		if limit==0:
			return res;
		elif limit<0 or limit==None:
			limit=-1;
		try:
			open(self.DGSTORAGE_Name+'/cache/prop/'+propItem+'_'+order+'.dgb');
		except:
			for collection in self.CollectionCache:
				with open(self.DGSTORAGE_Name+'/'+str(collection)+'/index/index.dgi') as collIndex:
					for line in collIndex:
						line=line.replace('\n','');
						if line!='':
							split=line.split(",");
							prop=self.getprop(split[0],collection);
							try:
								prop[propItem];
							except:
								pass;
							else:
								sortArray.append({"uid":split[0],"propValue":(prop[propItem])});
			if order=="WORD":
				srt=sorted(sortArray,key=lambda x:str(x["propValue"]));
			elif order=="ASC":
				srt=sorted(sortArray,key=lambda x:float(x["propValue"]));
			elif order=="DESC":
				srt=sorted(sortArray,key=lambda x:float(x["propValue"]),reverse=True);
			else:
				return False;
			for element in srt:
				res.append(element);
			try:
				open(self.DGSTORAGE_Name+'/cache/prop/index.dgi');
			except:
				pass;
			else:
				with open(self.DGSTORAGE_Name+'/cache/prop/index.dgi') as cacheIndex:
					count=0;
					for line in cacheIndex:
						line=line.replace('\n','');
						if line!='':
							count+=1;
					if count>=self.DGSTORAGE_PROPCACHELIMIT:
						if limit==-1:
							return res[skip:];
						else:
							return res[skip:skip+limit];
			with open(self.DGSTORAGE_Name+'/cache/prop/'+propItem+'_'+order+'.dgb','a') as cacheTimeStamp:
				cacheTimeStamp.write(self.DGSTORAGE_TimeStamp);
			with open(self.DGSTORAGE_Name+'/cache/prop/'+propItem+'_'+order+'.dgc','a') as cacheObject:
				for element in res:
					cacheObject.write(element["uid"]+','+element["propValue"]+'\n');
			with open(self.DGSTORAGE_Name+'/cache/prop/index.dgi','a') as cacheIndex:
				cacheIndex.write(propItem+'_'+order);
			if limit==-1:
				return res[skip:];
			else:
				return res[skip:skip+limit];
		else:
			with open(self.DGSTORAGE_Name+'/cache/prop/'+propItem+'_'+order+'.dgb') as cacheTimeStamp:
				if cacheTimeStamp.read()!=self.DGSTORAGE_TimeStamp:
					os.remove(self.DGSTORAGE_Name+'/cache/prop/'+propItem+'_'+order+'.dgb');
					os.remove(self.DGSTORAGE_Name+'/cache/prop/'+propItem+'_'+order+'.dgc');
					return self.sort(propItem,order,limit,skip);
			with open(self.DGSTORAGE_Name+'/cache/prop/'+propItem+'_'+order+'.dgc') as cacheObject:
				for line in cacheObject:
					line=line.replace("\n","");
					if line!='':
						split=line.split(",");
						res.append({"uid":split[0],"propValue":split[1]});
				if limit==-1:
					return res[skip:];
				else:
					return res[skip:skip+limit];
	
	def put(self,uid,content):
		import codecs;
		for collection in self.CollectionCache:
			with open(self.DGSTORAGE_Name+'/'+str(collection)+'/index/index.dgi') as collIndex:
				findStatus=False;
				for line in collIndex:
					line=line.replace('\n','');
					if line!='':
						split=line.split(',');
						if split[0]==uid:
							with codecs.open(self.DGSTORAGE_Name+'/'+str(collection)+'/'+str(uid)+'.dgs','w',self.DGSTORAGE_CHARSET) as storage:
								storage.write(content);
							findStatus=True;
					if findStatus==True:
						break;
			if findStatus==True:
				break;
			else:
				continue;
		if findStatus==True:
			self.uptmp();
			return True;
		else:
			return False;
	
	def setprop(self,uid,propItem,propValue):
		import codecs;
		import urllib.parse;
		propItem=urllib.parse.quote_plus(str(propItem));
		propValue=urllib.parse.quote_plus(str(propValue));
		for collection in self.CollectionCache:
			with open(self.DGSTORAGE_Name+'/'+str(collection)+'/index/index.dgi') as collIndex:
				for line in collIndex:
					line=line.replace('\n','');
					if line!='':
						split=line.split(',');
						if split[0]==uid:
							try:
								open(self.DGSTORAGE_Name+'/'+str(collection)+'/'+str(uid)+'.dgp');
							except:
								with codecs.open(self.DGSTORAGE_Name+'/'+str(collection)+'/'+str(uid)+'.dgp','a',self.DGSTORAGE_CHARSET) as storageProp:
									storageProp.write(propItem+':'+propValue);
								return True;
							else:
								propList={};
								with codecs.open(self.DGSTORAGE_Name+'/'+str(collection)+'/'+str(uid)+'.dgp','r',self.DGSTORAGE_CHARSET) as storageProp:
									for line in storageProp:
										line=line.replace('\n','');
										if line!='':
											split=line.split(':');
											if split[0]!=propItem:
												propList[split[0]]=split[1];
									propList[propItem]=propValue;
								with codecs.open(self.DGSTORAGE_Name+'/'+str(collection)+'/'+str(uid)+'.dgp','w',self.DGSTORAGE_CHARSET) as storageProp:
									for propElement in propList:
										storageProp.write(propElement+':'+propList[propElement]+'\n');
								return True;
		return False;
	
	def removeprop(self,uid,propItem):
		import codecs;
		import urllib.parse;
		import os;
		propItem=urllib.parse.quote_plus(str(propItem));
		for collection in self.CollectionCache:
			with open(self.DGSTORAGE_Name+'/'+str(collection)+'/index/index.dgi') as collIndex:
				for line in collIndex:
					line=line.replace('\n','');
					if line!='':
						split=line.split(',');
						if split[0]==uid:
							try:
								open(self.DGSTORAGE_Name+'/'+str(collection)+'/'+str(uid)+'.dgp');
							except:
								return False;
							else:
								propList={};
								with codecs.open(self.DGSTORAGE_Name+'/'+str(collection)+'/'+str(uid)+'.dgp','r',self.DGSTORAGE_CHARSET) as storageProp:
									for line in storageProp:
										line=line.replace('\n','');
										if line!='':
											split=line.split(':');
											if split[0]!=propItem:
												propList[split[0]]=split[1];
								if(len(propList)>0):
									with codecs.open(self.DGSTORAGE_Name+'/'+str(collection)+'/'+str(uid)+'.dgp','w',self.DGSTORAGE_CHARSET) as storageProp:
										for propElement in propList:
											storageProp.write(propElement+':'+propList[propElement]+'\n');
									return True;
								else:
									os.remove(self.DGSTORAGE_Name+'/'+str(collection)+'/'+str(uid)+'.dgp');
									return True;
		return False;
	
	def remove(self,uid):
		import os;
		import codecs;
		findStatus=False;
		for line in self.CollectionCache:
			line=line.replace('\n','');
			itemList=[];
			with open(self.DGSTORAGE_Name+'/'+str(line)+'/index/index.dgi') as collIndex:
				for row in collIndex:
					row=row.replace('\n','');
					split=row.split(',');
					if split[0]==uid:
						os.remove(self.DGSTORAGE_Name+'/'+str(line)+'/'+str(uid)+'.dgs');
						try:
							os.remove(self.DGSTORAGE_Name+'/'+str(line)+'/'+str(uid)+'.dgp');
						except FileNotFoundError:
							pass;
						findStatus=True;
					else:
						itemList.append(row);
			if findStatus==True:
				with codecs.open(self.DGSTORAGE_Name+'/'+str(line)+'/index/index.dgi','w',self.DGSTORAGE_CHARSET) as collIndex:
					string='';
					for item in itemList:
						string=str(string)+str(item)+'\n';
					collIndex.write(string);
				i=0;
				with open(self.DGSTORAGE_Name+'/'+str(line)+'/index/index.dgi') as collIndex:
					for line in collIndex:
						line=line.replace('\n','');
						if line!='':
							i+=1;
				if i==0:
					self.removecoll(str(line));
				break;
		if findStatus==False:
			return False;
		self.uptmp();
		return True;
	
	def zip(self,zipName="DGStorage"):
		import codecs;
		import urllib.parse;
		if zipName=='' or zipName==None:
			return False;
		zipName=str(zipName).replace('.dgz','');
		zipName=urllib.parse.quote_plus(str(zipName));
		zip=codecs.open(zipName+'.dgz','a',self.DGSTORAGE_CHARSET);
		zip.write(self.DGSTORAGE_Name+'\n');
		with codecs.open(self.DGSTORAGE_Name+'/conf.dgb','r',self.DGSTORAGE_CHARSET) as conf:
			zip.write(urllib.parse.quote_plus(conf.read())+'\n');
		for collection in self.CollectionCache:
			with open(self.DGSTORAGE_Name+'/'+str(collection)+'/index/index.dgi') as collIndex:
				for line in collIndex:
					line=line.replace('\n','');
					if line!='':
						split=line.split(',');
						zip.write(split[0]+','+split[1]+',');
						with codecs.open(self.DGSTORAGE_Name+'/'+str(collection)+'/'+str(split[0])+'.dgs','r','utf8') as storage:
							zip.write(urllib.parse.quote_plus(storage.read())+',');
						try:
							open(self.DGSTORAGE_Name+'/'+str(collection)+'/'+str(split[0])+'.dgp');
						except:
							zip.write('\n');
						else:
							with codecs.open(self.DGSTORAGE_Name+'/'+str(collection)+'/'+str(split[0])+'.dgp','r','utf8') as storageProp:
								zip.write(urllib.parse.quote_plus(storageProp.read())+'\n');
		zip.close();
		return True;
	
	def unzip(self,zipName="DGStorage"):
		import codecs;
		import urllib.parse;
		import os;
		import uuid;
		if zipName=='' or zipName==None:
			return False;
		zipName=str(zipName).replace('.dgz','');
		zipName=urllib.parse.quote_plus(zipName);
		try:
			open(zipName+'.dgz');
		except:
			return False;
		else:
			zip=codecs.open(zipName+'.dgz','r',self.DGSTORAGE_CHARSET);
			i=0;
			for line in zip:
				line=line.replace('\n','');
				if i==0:
					self.create(line);
					self.select(line);
					i+=1;
				elif i==1:
					os.remove(self.DGSTORAGE_Name+'/conf.dgb');
					with codecs.open(self.DGSTORAGE_Name+'/conf.dgb','a',self.DGSTORAGE_CHARSET) as conf:
						conf.write(urllib.parse.unquote_plus(line));
					i+=1;
				else:
					split=line.split(',');
					split[1]=urllib.parse.unquote_plus(split[1]);
					split[2]=urllib.parse.unquote_plus(split[2]);
					split[3]=urllib.parse.unquote_plus(split[3]);
					if split[3]!='' and split[3]!='\n':
						self.add(split[1],split[2],{},split[0],split[3]);
					else:
						self.add(split[1],split[2],{},split[0]);
		return True;
	
	#Private
	def clche(self,where=''):
		if where=='':
			self.CollectionCache=[];
	
	def createcoll(self,coll):
		import codecs;
		import os;
		try:
			os.mkdir(self.DGSTORAGE_Name+'/'+str(coll));
		except FileExistsError:
			return False;
		else:
			os.mkdir(self.DGSTORAGE_Name+'/'+str(coll)+'/index');
			with codecs.open(self.DGSTORAGE_Name+'/'+str(coll)+'/index/index.dgi','a',self.DGSTORAGE_CHARSET) as dgc:
				pass;
			self.CollectionCache.append(str(coll));
			with open(self.DGSTORAGE_Name+'/index/index.dgi','a') as index:
				index.write(str(coll)+'\n');
			return True;
	
	def removecoll(self,coll):
		import codecs;
		import os;
		os.remove(self.DGSTORAGE_Name+'/'+str(coll)+'/index/index.dgi');
		os.rmdir(self.DGSTORAGE_Name+'/'+str(coll)+'/index');
		os.rmdir(self.DGSTORAGE_Name+'/'+str(coll));
		self.CollectionCache.remove(str(coll));
		collCache=[];
		with open(self.DGSTORAGE_Name+'/index/index.dgi') as index:
			for line in index:
				line=str(line.replace('\n',''));
				if line!=str(coll):
					collCache.append(line);
		with codecs.open(self.DGSTORAGE_Name+'/index/index.dgi','w',self.DGSTORAGE_CHARSET) as index:
			if len(collCache)!=0:
				for collection in collCache:
					index.write(str(collection)+'\n');
		return True;
	
	def findavailablecoll(self,createNewColl=False):
		searchRange=self.DGSTORAGE_SEARCHRANGE;
		if searchRange!='' or searchRange!=None:
			searchRange=-1-int(searchRange);
		for collection in self.CollectionCache[:searchRange:-1]:
			with open(self.DGSTORAGE_Name+'/'+str(collection)+'/index/index.dgi') as collIndex:
				i=0;
				for line in collIndex:
					if line!='':
						i+=1;
				if i<self.DGSTORAGE_SINGLECOLLECTIONLIMIT:
					return collection;
					break;
				else:
					continue;
		if createNewColl==True:
			self.createcoll(int(self.LastCollection)+1);
			return int(self.LastCollection)+1;
		else:
			return False;
	
	def finditemviakey(self,key,limit,skip):
		limit=int(limit);
		skip=int(skip);
		if skip<0:
			skip=0;
		res=[];
		if limit==0:
			return res;
		elif limit<0 or limit==None:
			limit=-1;
		if key!='$all':
			import urllib.parse;
			key=str(urllib.parse.quote_plus(str(key)));
		s=0;
		i=1;
		res=[];
		if key=='$all':
			for collection in self.CollectionCache:
				with open(self.DGSTORAGE_Name+'/'+str(collection)+'/index/index.dgi') as collIndex:
					for line in collIndex:
						if s>=skip:
							if i<=limit and limit!=-1:
								line=line.replace('\n','');
								if line!='':
									split=line.split(',');
									with open(self.DGSTORAGE_Name+'/'+str(collection)+'/'+str(split[0])+'.dgs') as storage:
										prop=self.getprop(split[0],collection);
										res.append({"uid":str(split[0]),"key":str(split[1]),"content":str(storage.read()),"prop":prop});
								i+=1;
							elif limit==-1:
								line=line.replace('\n','');
								if line!='':
									split=line.split(',');
									with open(self.DGSTORAGE_Name+'/'+str(collection)+'/'+str(split[0])+'.dgs') as storage:
										prop=self.getprop(split[0],collection);
										res.append({"uid":str(split[0]),"key":str(split[1]),"content":str(storage.read()),"prop":prop});
								i+=1;
							else:
								break;
						else:
							s+=1;
		else:
			for collection in self.CollectionCache:
				with open(self.DGSTORAGE_Name+'/'+str(collection)+'/index/index.dgi') as collIndex:
					for line in collIndex:
						if s>=skip:
							if i<=limit and limit!=-1:
								line=line.replace('\n','');
								if line!='':
									split=line.split(',');
									if split[1]==key:
										with open(self.DGSTORAGE_Name+'/'+str(collection)+'/'+str(split[0])+'.dgs') as storage:
											prop=self.getprop(split[0],collection);
											res.append({"uid":str(split[0]),"key":str(split[1]),"content":str(storage.read()),"prop":prop});
								i+=1;
							elif limit==-1:
								line=line.replace('\n','');
								if line!='':
									split=line.split(',');
									if split[1]==key:
										with open(self.DGSTORAGE_Name+'/'+str(collection)+'/'+str(split[0])+'.dgs') as storage:
											prop=self.getprop(split[0],collection);
											res.append({"uid":str(split[0]),"key":str(split[1]),"content":str(storage.read()),"prop":prop});
								i+=1;
							else:
								break;
						else:
							s+=1;
		return res;
	
	def finditemviauid(self,uid,coll=None):
		res={};
		if coll==None:
			for collection in self.CollectionCache:
				with open(self.DGSTORAGE_Name+'/'+str(collection)+'/index/index.dgi') as collIndex:
					for line in collIndex:
						line=line.replace('\n','');
						if line!='':
							split=line.split(',');
							if split[0]==str(uid):
								with open(self.DGSTORAGE_Name+'/'+str(collection)+'/'+str(split[0])+'.dgs') as storage:
									res["uid"]=str(split[0]);
									res["key"]=str(split[1]);
									res["content"]=str(storage.read())
									res["prop"]=self.getprop(split[0],collection);
									return res;
			return res;
		else:
			with open(self.DGSTORAGE_Name+'/'+str(coll)+'/index/index.dgi') as collIndex:
				for line in collIndex:
					line=line.replace('\n','');
					if line!='':
						split=line.split(',');
						if split[0]==str(uid):
							with open(self.DGSTORAGE_Name+'/'+str(coll)+'/'+str(split[0])+'.dgs') as storage:
								res["uid"]=str(split[0]);
								res["key"]=str(split[1]);
								res["content"]=str(storage.read())
								res["prop"]=self.getprop(split[0],coll);
								return res;
				return res;
	
	def getprop(self,uid,coll=None):
		import codecs;
		import urllib.parse;
		res={};
		if coll==None:
			for collection in CollectionCache:
				try:
					open(self.DGSTORAGE_Name+'/'+str(collection)+'/'+str(uid)+'.dgp');
				except FileNotFoundError:
					return res;
				else:
					with codecs.open(self.DGSTORAGE_Name+'/'+str(collection)+'/'+str(uid)+'.dgp') as f:
						for line in f:
							line=line.replace('\n','');
							if line!='':
								split=line.split(':');
								if len(split)>=2:
									split[0]=urllib.parse.unquote_plus(str(split[0]));
									split[1]=urllib.parse.unquote_plus(str(split[1]));
									res[split[0]]=split[1];
						return res;
		else:
			try:
				open(self.DGSTORAGE_Name+'/'+str(coll)+'/'+str(uid)+'.dgp');
			except FileNotFoundError:
				return res;
			else:
				with codecs.open(self.DGSTORAGE_Name+'/'+str(coll)+'/'+str(uid)+'.dgp','r',self.DGSTORAGE_CHARSET) as f:
					for line in f:
						line=line.replace('\n','');
						if line!='':
							split=line.split(':');
							if len(split)>=2:
								split[0]=urllib.parse.unquote_plus(str(split[0]));
								split[1]=urllib.parse.unquote_plus(str(split[1]));
								res[split[0]]=split[1];
					return res;
	
	def uptmp(self):
		import uuid;
		with open(self.DGSTORAGE_Name+'/cache/time.dgb','w') as timeStamp:
			sts=str(uuid.uuid1());
			timeStamp.write(sts);
			self.DGSTORAGE_TimeStamp=sts;
		return True;

class DGStorageShell(DGStorage):
	def shellAdd(self,key,inFileLocation):
		import codecs;
		with codecs.open(inFileLocation,'r',self.DGSTORAGE_CHARSET) as f:
			string='';
			for line in f:
				line=line.replace('\n','');
				string=str(string)+str(line);
				self.add(key,string);
	
	def shellGet(self,key,outFileLocation):
		import codecs;
		import urllib.parse;
		res=self.get(key);
		f=codecs.open(outFileLocation,'w',self.DGSTORAGE_CHARSET);
		string='';
		for item in res:
			item['content']=urllib.parse.quote_plus(item['content']);
			string=str(string)+str(item['uid'])+','+str(item['content'])+','+str(item['prop'])+'\n';
		f.write(string);
		f.close();
	
	def shellFetch(self,limit,skip,outFileLocation):
		import codecs;
		import urllib.parse;
		res=self.fetch(limit,skip);
		f=codecs.open(outFileLocation,'w',self.DGSTORAGE_CHARSET);
		string='';
		for item in res:
			item['content']=urllib.parse.quote_plus(item['content']);
			string=str(string)+str(item['uid'])+','+str(item['content'])+','+str(item['prop'])+'\n';
		f.write(string);
		f.close();

if __name__ == '__main__':
	try:
		sys.argv[1];
	except IndexError:
		pass;
	else:
		import sys;
		if sys.argv[1]=='add':
			try:
				sys.argv[4];
			except IndexError:
				pass;
			else:
				shellHandle=DGStorageShell();
				shellHandle.select(str(sys.argv[2]));
				if sys.argv[4].find('/')==-1:
					shellHandle.shellAdd(str(sys.argv[3]),'../'+str(sys.argv[4]));
		if sys.argv[1]=='get':
			try:
				sys.argv[4];
			except IndexError:
				pass;
			else:
				shellHandle=DGStorageShell();
				shellHandle.select(str(sys.argv[2]));
				if sys.argv[4].find('/')==-1:
					shellHandle.shellGet(str(sys.argv[3]),'../'+str(sys.argv[4]));
		if sys.argv[1]=='fetch':
			try:
				sys.argv[5];
			except IndexError:
				pass;
			else:
				shellHandle=DGStorageShell();
				shellHandle.select(str(sys.argv[2]));
				if sys.argv[5].find('/')==-1:
					shellHandle.shellFetch(str(sys.argv[3]),str(sys.argv[4]),'../'+str(sys.argv[5]));
		if sys.argv[1]=='unzip':
			try:
				sys.argv[2];
			except IndexError:
				pass;
			else:
				shell=DGStorage();
				shell.unzip(str(sys.argv[2]));
