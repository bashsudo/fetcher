"""
ebay scraper 2021 - webpage retrieval and caching system
"""

import requests
import os
import random
import string


fileNameList = [
	'fetcher_db.txt'
]

folderNameList = [
	'fetcher_cache'
]

folderMode = 0o755
fileMode = 0o644

fileNameGenerateChars = string.ascii_letters + string.digits
fileNameGenerateLength = 32

# COMPLETE
def GenerateFileName():
	return ''.join(random.SystemRandom().choice(fileNameGenerateChars) for loop in range(fileNameGenerateLength))


# INCOMPLETE
class Cache_Item:
	
	def __init__(self, url, fileName=None, creationDatetimeObject=None):
		# If "fileName" is None, automatically generate random filename
		# If "creationTimestamp" is None, automatically get latest time
		
		if not fileName:
			fileName = GenerateFileName()
		
		if not creationDatetimeObject:
			creationDatetimeObject = datetime.datetime.now()
		
		self.fileName = fileName
		self.creationDatetimeObject = creationDatetimeObject


# INCOMPLETE
def CachePageExpirationCheck(pageUrl):
	pass


# INCOMPLETE
def WebpageFetch(pageUrl):
	pass


# INCOMPLETE
def InitCacheScan():
	# INCOMPLETE
	with open('fetcher_db.txt', 'r') as fileItself:
		fileReadLines = fileItself.readlines()
		
		for line in fileReadLines:
			lineSplit = line.split('\t')


# COMPLETED "ENOUGH" FOR NOW
def InitFilesystem():
	
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
	InitFilesystem()


main()
