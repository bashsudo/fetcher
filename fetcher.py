"""
ebay scraper 2021 - webpage retrieval and caching system
"""

import requests
import os


fileNameList = [
	'fetcher_db.txt'
]

folderNameList = [
	'fetcher_cache'
]

folderMode = 0o755
fileMode = 0o644

def CachePageExpirationCheck(pageUrl):
	pass


def WebpageFetch(pageUrl):
	pass


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
