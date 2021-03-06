"""
Fetcher: Webpage Retrieval and Caching System
2021 Eiza Stanford ("Bash Sudo" / "Charky Barky")

Main Script
"""

# >>> STANDARD LIBRARY IMPORTS:
# Datetime
import datetime
from datetime import datetime as datetime_object
from datetime import timedelta as timedelta_object

# Other
import os
import random
import string
import time

# >>> THIRD-PARTY IMPORTS:
# Termcolor
from termcolor import colored

# Fake Useragent
from fake_useragent import UserAgent

# Requests
import requests

# ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# ===== ===== ===== ===== ===== ===== ===== ===== ===== =====


# File and folder names for the cache-related data:
cacheDatabaseFileName = 'fetcher_db.txt'
cacheFolderName = 'fetcher_cache'

# Data read from the cache database file (string and list form):
cacheDatabaseRead = None
cacheDatabaseReadLines = None
cacheDatabaseReadLinesUrl = None

# This is the version of "cacheDatabaseReadLines" that will actually be written to the database file:
cacheDatabaseModifiedLines = None

# Default file and folder permissions when creating things:
folderMode = 0o755
fileMode = 0o644

# The length and list of characters to use (by default) when generating file names:
fileNameGenerateChars = string.ascii_letters + string.digits
fileNameGenerateLength = 32

# Other important cache-related variables:
cacheReferenceDict = {}
cacheExpirationIntervalMinDefault = 1

# Randomize the user agent when requesting pages, to avoid 403 Forbidden errors (among other things):
requestUserAgentRandomized = UserAgent().random

# Boolean variable that either enables or disables ALL "DebugPrint..." functions.
verboseOutput = False


# ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# ===== ===== ===== ===== ===== ===== ===== ===== ===== =====


# === === === === === === === === === === === === === === === === === === === === === === === === === ===
# >>> >>> >>> WARNING: THIS CLASS IS NOT DESIGNED TO BE USED TO EASILY AND SEEMLESSLY MAKE CACHE OBJECTS <<< <<< <<<
# COMPLETE "ENOUGH" FOR NOW
class Cache_Item_Object:

	# COMPLETE "ENOUGH" FOR NOW
	def DatabasePrepare(self):
		global cacheDatabaseModifiedLines
		
		# If the URL is in the content of the database file.
		if self.url in cacheDatabaseRead:
			# Find the line number with the URL.
			self.databaseLineNumber = cacheDatabaseReadLinesUrl.index(self.url)
		
		else:
			# If there is no URL, simply append a new line and use that.
			cacheDatabaseModifiedLines.append('')
			self.databaseLineNumber = len(cacheDatabaseReadLines)
		
		DebugPrint('line number (NOT LIST NUMBER) now %d' % (self.databaseLineNumber + 1), preface='(OBJECT) CACHE %s' % self.url)


	# COMPLETE "ENOUGH" FOR NOW
	def DatabaseUpdate(self):
		global cacheDatabaseModifiedLines
		
		# For readability, assign string ISO-formatted timestamps to variables.
		creationDatetimeIso = datetime_object.isoformat(self.creationDatetimeObject)
		expirationDatetimeIso = datetime_object.isoformat(self.expirationDatetimeObject)
		
		# Update the line that this cache object exists on.
		cacheDatabaseModifiedLines[self.databaseLineNumber] = '%s\t%s\t%s\t%s' % (self.url, self.fileName, creationDatetimeIso, expirationDatetimeIso)
		
		# MIGHT BE CHANGED to only write, instead of write AND read (this may be a bad idea!)
		DatabaseFileWriteReadCycle()
		# DatabaseFileWrite()


	# COMPLETE "ENOUGH" FOR NOW
	def FileCreatePlaceholder(self):
		try:
			open(self.fileName, 'x').close()
			os.chmod(self.fileName, fileMode)
		
		except FileExistsError:
			return False
		
		return True


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
		# Actually make the request for the website and update the object's html.
		pageRequest = requests.get(self.url, headers={'User-Agent':requestUserAgentRandomized})
		self.html = pageRequest.text
		
		# Update the creation datetime: take the current date and time (datetime) at this moment.
		self.creationDatetimeObject = datetime_object.now()
		
		# Update the expiration datetime: take the creation datetime and add it with the expiration interval timedelta (i.e. expiration = creation + interval).
		self.expirationDatetimeObject = self.creationDatetimeObject + self.expirationIntervalObject
		
		# Update the file with the new cache content.
		self.FileWrite()
		
		# Update the database with the new creation, expiration times, etc.
		self.DatabaseUpdate()


	# COMPLETE "ENOUGH" FOR NOW
	def ExpirationCheck(self, autoUpdateFile=True, autoUpdateExpirationInterval=None):
		# Create a boolean whether or not the cache object has expired (passed expiration time).
		expired = (datetime_object.now() > self.expirationDatetimeObject)
		
		# NOTE: originally this if-statement was to be executed IF the object expired
		# This was moved OUTSIDE of the expired code block
		# Thus the expiration interval can be changed even if the cache has not expired yet
		if autoUpdateExpirationInterval:
			self.ExpirationIntervalChange(autoUpdateExpirationInterval)
		
		# Update the cache (and file).
		if expired:
			DebugPrint('cache object expired!', important=True, preface='(OBJECT) CACHE %s' % self.url)
			
			if autoUpdateFile:
				self.CacheContentUpdate()
		
		return expired


	# COMPLETE "ENOUGH" FOR NOW
	def ExpirationIntervalChange(self, expirationIntervalMin):
		DebugPrint('changed expiration interval to %s' % str(expirationIntervalMin), preface='(OBJECT) CACHE %s' % self.url)
		self.expirationIntervalObject = timedelta_object(minutes=expirationIntervalMin)


	# COMPLETE "ENOUGH" FOR NOW
	def __init__(self, url, fileName, creationDatetimeObject, expirationDatetimeObject, expirationIntervalMin=None):
		# Update the attributes that can be directly taken from parameters.
		self.url = url
		self.fileName = fileName
		self.creationDatetimeObject = creationDatetimeObject
		self.expirationDatetimeObject = expirationDatetimeObject
		
		self.databaseLineNumber = None
		self.html = None
		
		# >>> EXPIRATION INTERVAL ATTRIBUTE
		if expirationIntervalMin:
			# if given the expiration interval (minute integer), then make a timedelta object out of it.
			self.expirationIntervalObject = timedelta_object(minutes=expirationIntervalMin)
		else:
			# If NOT given any expiration interval (None), then make a timedelta object out of the difference between the creation datetime and expiration datetime.
			self.expirationIntervalObject = self.expirationDatetimeObject - self.creationDatetimeObject
		
		# Immediately create a placeholder file.
		if self.fileName:
			newlyCreated = self.FileCreatePlaceholder()
			
			if not newlyCreated:
				DebugPrint('HTML cache file already exists; updating object HTML content to cache file', preface='(OBJECT) CACHE %s' % self.url)
				
				self.FileRead()
		
		# Prepare this object to modify the database file.
		self.DatabasePrepare()



# ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# ===== ===== ===== ===== ===== ===== ===== ===== ===== =====


# COMPLETE "ENOUGH" FOR NOW
def DebugPrint(string, preface=None, important=False):
	if verboseOutput:
		if important:
			colorString = 'yellow'
			colorPreface = 'red'
		else:
			colorString = 'blue'
			colorPreface = 'cyan'
		
		string = colored(string, colorString)
		
		if preface:
			string = '%s%s' % (colored('%s: ' % preface, colorPreface, attrs=['bold']), string)
		
		print(string, '\n')


# COMPLETE
def GenerateFileName():
	return ''.join(random.SystemRandom().choice(fileNameGenerateChars) for loop in range(fileNameGenerateLength))


# COMPLETED "ENOUGH" FOR NOW
def GenerateCacheObject(url, expirationIntervalMin=None):
	# If the given expiration interval is None, assume the global default.
	if not expirationIntervalMin:	
		expirationIntervalMin = cacheExpirationIntervalMinDefault
	
	# Get the path: the folder with the cache object files + the generated name.
	fileName = '%s/%s.html' % (cacheFolderName, GenerateFileName())
	
	# Get the creation datetime: take the current date and time (datetime) at this moment.
	creationDatetimeObject = datetime_object.now()
	
	# Get the expiration datetime: take the creation datetime and add it with the expiration interval timedelta (i.e. expiration = creation + interval).
	expirationDatetimeObject = creationDatetimeObject + timedelta_object(minutes=expirationIntervalMin)
	
	# Finally create the object.
	cacheObject = Cache_Item_Object(url, fileName, creationDatetimeObject, expirationDatetimeObject, expirationIntervalMin)
	
	return cacheObject


# COMPLETED "ENOUGH" FOR NOW
# === === === === === === === === === === === === === === === === === === === === === === === === === ===
# >>> >>> >>> THIS FUNCTION WILL BE HEAVILY USED BY OTHER SCRIPTS THAT IMPORT THE FETCHER SCRIPT <<< <<< <<<
# >>> >>> >>> IN OTHER WORDS, THIS FUNCTION IS ALMOST THE WHOLE POINT/PURPOSE OF THE FETCHER SCRIPT <<< <<< <<<
def WebpageFetch(url, expirationIntervalMin=None, forceUpdateCache=False):
	global cacheReferenceDict
	
	# VERY IMPORTANT NOTE:
	# When the parameter "expirationIntervalMin" is NOT None, the expiration interval value will be changed to match it in a certain cache object ONLY when it the cahce content is updated (
	
	# If the URL already has a corresponding cache object in the database.
	if url in cacheReferenceDict:
		DebugPrint('url is in the list of cache objects (object already exists)', preface='(WebpageFetch) CACHE %s' % url)
		
		
		# Grab an existing cache object that corresponds with the URL.
		cacheObject = cacheReferenceDict[url]
		
		# If the user wants the latest page request (forceUpdateCache).
		if forceUpdateCache:
			DebugPrint('force update cache requested: returning html from cache object, but with request from website just now', preface='(WebpageFetch) CACHE %s' % url, important=True)
			
			# If "expirationIntervalMin" is not None, forcefully update the expiration interval.
			if expirationIntervalMin:
				cacheObject.ExpirationIntervalChange(expirationIntervalMin)
			
			# Forcefully update the cache content, regardless if it has expired or not.
			cacheObject.CacheContentUpdate()
		
		# If not, then use the current cache data (but update the cache if it is expired).
		else:
			DebugPrint('returning cached html content (returning new html if expired)', preface='(WebpageFetch) CACHE %s' % url)	
			
			# Check to see if it has expired (and tell the function to automatically update and change the expiration interval).
			cacheObject.ExpirationCheck(autoUpdateFile=True, autoUpdateExpirationInterval=expirationIntervalMin)
			
		return cacheObject.html
	
	# If there is no matching cache object with the URL.
	else:
		DebugPrint('url is NOT FOUND in the list of cache objects: creating new cache object', preface='(WebpageFetch) CACHE %s' % url, important=True)
		
		# Create a brand-new cache object.
		cacheObject = GenerateCacheObject(url, expirationIntervalMin=expirationIntervalMin)
		
		# Add it to the reference.
		cacheReferenceDict[url] = cacheObject
		
		# Update the cache content (so that it can be used later).
		cacheObject.CacheContentUpdate()
		
		return cacheObject.html


# THIS FUNCTION SHOULD ONLY BE USED IN THE VERY BEGINNING OF RUNNING THIS SCRIPT, SPECIFICALLY BEFORE DatabaseFileRead(init=False) DUE TO EXISTING CACHE OBJECTS IN THE REFERENCE
def DatabaseCleanup():
	if not cacheDatabaseReadLines:
		DatabaseFileRead()
	
	for line in cacheDatabaseReadLines:
		lineSplit = line.split('\t')
		
		url = lineSplit[0]
		fileName = lineSplit[1]
		expirationDatetimeObject = datetime_object.fromisoformat(lineSplit[3])
		
		# Testing if the cache object expired (current date-time exceeds the expiration date-time of the object)
		if datetime_object.now() > expirationDatetimeObject:
			DebugPrint('removed expired cache file in database (filename="%s")' % fileName, important=True, preface='(DatabaseCleanup) CACHE %s' % url)
			
			# Remove the corresponding HTML file with the cache object.
			os.remove(fileName)
			
			# Removes the line from the modified-lines buffer list.
			# The "modified-lines" is being used now instead of "read-lines" because using "read-lines" for indexes does not accomodate for shifts in lines resulting from deleting lines in "modified-lines."
			# Iterating through a list and removing its content IS RISKY, which is why "read-lines" is used in the for-loop.
			index = cacheDatabaseModifiedLines.index(line)
			
			del cacheDatabaseModifiedLines[index]
	
	# At the very end, write the changes and read from the file.
	DatabaseFileWriteReadCycle()
	
	# Tell the existing cache objects to adjust to the shifted lines in the database file (due to possibly deleted lines).
	for cacheObject in list(cacheReferenceDict.values()):
		cacheObject.DatabasePrepare()


# COMPLETED "ENOUGH" FOR NOW
def DatabaseFileWrite():
	with open(cacheDatabaseFileName, 'w') as fileItself:
		fileItself.write('\n'.join(cacheDatabaseModifiedLines))


# COMPLETED "ENOUGH" FOR NOW
def DatabaseFileRead(init=False):
	global cacheDatabaseRead
	global cacheDatabaseReadLines
	global cacheDatabaseReadLinesUrl
	global cacheDatabaseModifiedLines
	
	global cacheReferenceDict
	
	with open(cacheDatabaseFileName, 'r') as fileItself:
		cacheDatabaseRead = fileItself.read()
		
		# If the data read from the database file is NOT blank.
		if cacheDatabaseRead:
			cacheDatabaseReadLines = cacheDatabaseRead.split('\n')
			cacheDatabaseReadLinesUrl = [line.split('\t')[0] for line in cacheDatabaseReadLines]
			
		# If the data read from the database file IS ACTUALLY blank.
		else:
			# Keep the list variables EMPTY, and not "empty" with [''].
			cacheDatabaseReadLines = []
			cacheDatabaseReadLinesUrl = []
		
		cacheDatabaseModifiedLines = cacheDatabaseReadLines.copy()
		
		# If the function was told to create cache objects from every single line read from the database file (done first-time).
		if init and cacheDatabaseReadLines:
			for line in cacheDatabaseReadLines:
				if '\t' in line:
					lineSplit = line.split('\t')
					
					# Get the data from the tab-separated fields.
					url = lineSplit[0]
					fileName = lineSplit[1]
					creationDatetimeObject = datetime_object.fromisoformat(lineSplit[2])
					expirationDatetimeObject = datetime_object.fromisoformat(lineSplit[3])
					
					DebugPrint('found cache file in database (filename="%s")' % fileName, preface='(DatabaseFileRead) CACHE %s' % url)
					
					# Update the cache reference with brand-new cache objects.
					cacheReferenceDict[url] = Cache_Item_Object(url, fileName, creationDatetimeObject, expirationDatetimeObject)


# COMPLETED "ENOUGH" FOR NOW
def DatabaseFileWriteReadCycle():
	DatabaseFileWrite()
	DatabaseFileRead()


# COMPLETED "ENOUGH" FOR NOW
def InitFilesNeededCreate():
	# Create the cache folder.
	try:
		os.mkdir(cacheFolderName, mode=folderMode)
	
	except FileExistsError:
		DebugPrint('folder "%s" already exists!' % cacheFolderName, important=True)
	
	# Create the database file.
	try:
		open(cacheDatabaseFileName, 'x').close()
		os.chmod(cacheDatabaseFileName, fileMode)
	
	except FileExistsError:
		DebugPrint('file "%s" already exists!' % cacheDatabaseFileName, important=True)


# COMPLETED "ENOUGH" FOR NOW
# === === === === === === === === === === === === === === === === === === === === === === === === === ===
# >>> >>> >>> THIS FUNCTION SHOULD BE CALLED IMMEDIATELY WHEN THIS SCRIPT IS IMPORTED OR RAN! <<< <<< <<<
def InitEverything():
	InitFilesNeededCreate()
	DatabaseCleanup()
	DatabaseFileRead(init=True)


# ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# ===== ===== ===== ===== ===== ===== ===== ===== ===== =====


def TestProgram():
	DebugPrint('===== ===== ===== ===== ===== ===== ===== ===== ===== =====', important=True)
	DebugPrint('THIS TEST FUNCTION WILL DO THE FOLLOWING:', important=True)
	DebugPrint('* USE WebpageFetch TO REQUEST 3 EXAMPLE URLS', important=True)
	DebugPrint('* HAVE EXPIRATION INTERVALS OF 12 SECONDS', important=True)
	DebugPrint('* LOOP EVERY 4 SECONDS TO REPEAT THE PROCESS', important=True)
	DebugPrint('* THE EXPECTATION IS THAT EVERY 3 LOOPS (GIVE OR TAKE), THE CACHE WILL EXPIRE AND UPDATE', important=True)
	DebugPrint('===== ===== ===== ===== ===== ===== ===== ===== ===== =====', important=True)
	expirationInterval = 0.2
	
	time.sleep(6)
	
	while True:
		urlList = [
			'https://www.cnn.com',
			'https://en.wikipedia.org',
			'https://ikea.com/'
		]
		
		for url in urlList:
			WebpageFetch(url, expirationInterval)
		
		DebugPrint('\n\n(END, TIME: %s)\n\n' % datetime_object.isoformat(datetime_object.now()), important=True)
		time.sleep(4)
		DebugPrint('\n\nLOOPED!\n\n', important=True)


if __name__ == '__main__':
	verboseOutput = True

	InitEverything()
	TestProgram()
else:
	InitEverything()
