"""
ebay scraper 2021 - webpage retrieval and caching system
"""

import datetime
import requests
import os
import random
import string


# file and folder names for the cache-related data
cacheDatabaseFileName = 'fetcher_db.txt'
cacheFolderName = 'fetcher_cache'

# data read from the cache database file (string and list form)
cacheDatabaseRead = None
cacheDatabaseReadLines = None

# list of file and folder names to be created and checked for immediately
fileNameList = [
	'fetcher_db.txt'
]

folderNameList = [
	'fetcher_cache'
]

# default file and folder permissions when creating things
folderMode = 0o755
fileMode = 0o644

# the length and list of characters to use (by default) when generating file names
fileNameGenerateChars = string.ascii_letters + string.digits
fileNameGenerateLength = 32

# other important cache-related variables
cacheReferenceDict = {}
cacheExpirationIntervalMinDefault = 10


# COMPLETE
def GenerateFileName():
	return ''.join(random.SystemRandom().choice(fileNameGenerateChars) for loop in range(fileNameGenerateLength))


# INCOMPLETE
class Cache_Item_Object:

	# INCOMPLETE
	def DatabasePrepare(self):
		global cacheDatabaseRead
		global cacheDatabaseReadLines
		
		if self.url in cacheDatabaseRead:
			pass
			
		else:
			cacheDatabaseReadLines.append('')
			self.databaseLineNumber = len(cacheDatabaseReadLines)


	# INCOMPLETE
	def DatabaseUpdate(self):
		global cacheDatabaseRead
		global cacheDatabaseReadLines

		# there is no existing line in the database text file for the object (brand new object)
		pass


	# COMPLETE "ENOUGH" FOR NOW
	def FileCreatePlaceholder(self):
		try:
			open(self.fileName, 'x').close()
			os.chmod(self.fileName, fileMode)
		
		except FileExistsError:
			pass


	# COMPLETE "ENOUGH" FOR NOW
	def FileRead(self):
		with open(self.fileName, 'r') as fileItself:
			self.html = fileItself.read()


	# COMPLETE "ENOUGH" FOR NOW
	def FileWrite(self):
		with open(self.fileName, 'w') as fileItself:
			fileItself.write(self.html)


	# COMPLETE "ENOUGH" FOR NOW
	def CacheContentUpdate(self):
		# actually make the request for the website and update the object's html
		pageRequest = requests.get(self.url)
		self.html = pageRequest.text
		
		# update the creation datetime: take the datetime at this moment
		self.creationDatetimeObject = datetime.datetime.now()
		
		# update the expiration datetime: take the creation datetime and add it with the expiration interval timedelta (i.e. expiration = creation + interval)
		self.expirationDatetimeObject = self.creationDatetimeObject + self.expirationIntervalObject
		
		# update the file with the new cache content
		self.FileWrite()


	# COMPLETE "ENOUGH" FOR NOW
	def ExpirationCheck(self, autoUpdateFile=True):
		# create a boolean whether or not the cache object has expired (passed expiration time)
		expired = (datetime.datetime.now() > self.expirationDatetimeObject)
		
		# update the cache (and file)
		if autoUpdateFile and expired:
			self.CacheContentUpdate()
		
		return expired


	# COMPLETE "ENOUGH" FOR NOW
	def __init__(self, url, fileName, creationDatetimeObject, expirationDatetimeObject, expirationIntervalMin=None):
		# update the attributes that can be directly taken from parameters
		self.url = url
		self.fileName = fileName
		self.creationDatetimeObject = creationDatetimeObject
		self.expirationDatetimeObject = expirationDatetimeObject
		
		self.databaseLineNumber = None
		self.html = None
		
		# >>> expiration interval attribute
		if expirationIntervalMin:
			# if given the expiration interval (minute integer), then make a timedelta object out of it
			self.expirationIntervalObject = datetime.timedelta(minutes=expirationIntervalMin)
		else:
			# if NOT given any expiration interval (None), then make a timedelta object out of the difference between the creation datetime and expiration datetime
			self.expirationIntervalObject = self.expirationDatetimeObject - self.creationDatetimeObject
		
		# immediately create a placeholder file
		if self.fileName:
			self.FileCreatePlaceholder()


# COMPLETED "ENOUGH" FOR NOW
def GenerateCacheObject(url, expirationIntervalMin=None):
	# if the given expiration interval is None, assume the global default
	if not expirationIntervalMin:	
		expirationIntervalMin = cacheExpirationIntervalMinDefault
	
	# get the path: the folder with the cache object files + the generated name
	fileName = '%s/%s.html' % (cacheFolderName, GenerateFileName())
	
	# get the creation datetime: the datetime at this moment
	creationDatetimeObject = datetime.datetime.now()
	
	# get the expiration datetime: take the creation datetime and add it with the expiration interval timedelta (i.e. expiration = creation + interval)
	expirationDatetimeObject = creationDatetimeObject + datetime.timedelta(minutes=expirationIntervalMin)
	
	# finally create the object
	cacheObject = Cache_Item_Object(url, fileName, creationDatetimeObject, expirationDatetimeObject, expirationIntervalMin)
	
	return cacheObject


# INCOMPLETE
def WebpageFetch(url, forceUpdateCache=False):
	global cacheReferenceDict
	
	# if the URL already has a corresponding cache object in the database
	if url in cacheReferenceDict:
		
		# if the user wants the latest page request (forceUpdateCache)
		if forceUpdateCache:
			cacheObject.CacheContentUpdate()
			return cacheObject.html
		
		# if not, then use the current cache data (but update the cache if it is expired)
		else:
			cacheObject = cacheReferenceDict[url]
			cacheObject.ExpirationCheck(autoUpdateFile=True)
			return cacheObject.html
	
	# if there is no matching cache object with the URL
	else:
		cacheObject = GenerateCacheObject(url)
		cacheReferenceDict[url] = cacheObject
		cacheObject.CacheContentUpdate()
		return cacheObject.html


def DatabaseFileRead():
	global cacheDatabaseRead
	global cacheDatabaseReadLines
	
	with open(cacheDatabaseFileName, 'r') as fileItself:
		cacheDatabaseRead = fileItself.read()
		cacheDatabaseReadLines = fileItself.readlines()


# INCOMPLETE
def InitCacheScan():
	global cacheReferenceDict
	
	# INCOMPLETE
	with open(cacheDatabaseFileName, 'r') as fileItself:
		DatabaseFileRead()
		
		for line in cacheDatabaseReadLines:
			lineSplit = line.split('\t')
			
			url = lineSplit[0]
			fileName = lineSplit[1]
			creationDatetimeObject = datetime.datetime.fromisoformat(lineSplit[2])
			expirationDatetimeObject = datetime.datetime.fromisoformat(lineSplit[3])
			
			cacheReferenceDict[url] = Cache_Item_Object(url, fileName, creationDatetimeObject, expirationDatetimeObject)


# COMPLETED "ENOUGH" FOR NOW
def InitFilesNeededCreate():
	
	# Create the necessary folders in the folder list.
	for folderName in folderNameList:
		try:
			os.mkdir(folderName, mode=folderMode)
		
		except FileExistsError:
			print('InitFilesystem: folder %s already exists!' % folderName)
	
	# Create the necessary files in the file list.
	for fileName in fileNameList:
		try:
			open(fileName, 'x').close()
			os.chmod(fileName, fileMode)
		
		except FileExistsError:
			print('InitFilesystem: file %s already exists!' % fileName)


def main():
	InitFilesNeededCreate()
	
	url = 'https://docs.python.org/3/library/datetime.html'
	WebpageFetch(url)


main()
