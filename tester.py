"""
Fetcher: Webpage Retrieval and Caching System
2021 Eiza Stanford ("Bash Sudo" / "Charky Barky")

Tester Script
"""

# >>> FETCHER IMPORTS:
import fetcher

# >>> STANDARD LIBRARY IMPORTS:
import pathlib

fetcher.verboseOutput = True

fetcher.cacheExpirationIntervalMinDefault = 0.1

urlExampleList = [
	'https://time.is/',
	'https://www.raspberrypi.org/blog/',
	'https://xkcd.com/',
	'https://www.python.org/'
]

# ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# ===== ===== ===== ===== ===== ===== ===== ===== ===== =====

class Test_Container:
	
	def tell(self, who, message, prefix=''):
		print('\tURL %s:%s (%s) %s' % (self.link, prefix, who, message))
	
	
	def htmlDumpWrite(self):
		with open(self.dumpPath, 'w') as fileItself:
			fileItself.write(self.html)
			self.tell('htmlDump', 'success')
			
			return True
		
		return False
	
	
	def htmlDumpRead(self):
		if pathlib.PosixPath(self.dumpPath).exists():
			with open(self.dumpPath, 'r') as fileItself:
				self.htmlDump = fileItself.read()
				self.tell('htmlDumpRead', 'success')
				
				return True
		
		return False
	
	
	def fetch(self, differenceCheck=True, dumpUpdate=True):
		#self.html = fetcher.WebpageFetch(self.link, self.expTime)
		self.html = fetcher.WebpageFetch(self.link)
		self.tell('fetch', 'finished call WebpageFetch')
		
		if self.html:
			self.tell('fetch', 'SUCCESS: HTML OK')
		else:
			self.tell('fetch', 'FAILURE: NO HTML (None type in html)!')
		
		if differenceCheck:
			self.htmlDumpRead()
			
			if self.htmlDump:
				self.tell('fetch', 'DUMP COMPARE BEGIN:')
				
				if self.htmlDump == self.html:
					self.tell('fetch', 'DUMP SAME', '\t')
					
				else:
					self.tell('fetch', 'DUMP DIFFERENT', '\t')
		
		if dumpUpdate:
			self.htmlDumpWrite()
			self.tell('fetch', 'dump written')
	
	
	def __init__(self, link, expTime=None):
		self.link = link
		self.linkShort = '-'.join(link.split('//')[1].split('.')).replace('/','X')
		
		self.dumpPath = 'dump_html_%s.html' % self.linkShort
		
		self.expTime = expTime
		
		self.html = None
		self.htmlDump = None
		
		self.fetch()

def testInterface():
	active = True
	
	urlUsedList = {}
	
	while active:
		print('INTERFACE: choose an action, use an (e)xample URL, (m)anually enter a URL, or (l)ist currently used URLs.')
		inputAction = None
		
		while not inputAction in ('e', 'm', 'l'):
			inputAction = input('e/m/l> ')
		
		URL = None
		
		if inputAction in ('e', 'm'):
			if inputAction == 'e':
				for index in range(len(urlExampleList)):
					item = urlExampleList[index]
					print('%d: %s' % (index, item))
				
				print('\tINTERFACE: choose an example URL.')
				inputIndex = None
				indexAvailable = range(len(urlExampleList))
				
				while not (inputIndex and int(inputIndex) in indexAvailable):
					inputIndex = input('\t0-%d> ' % (len(urlExampleList) - 1))
					
				inputIndex = int(inputIndex)
					
				URL = urlExampleList[inputIndex]
			
			elif inputAction == 'm':
				print('\tINTERFACE: input a URL.')
				URL = input('\turl> ')
				print('\tINTERFACE: added URL %s to list of example URLs for use later.' % URL)
				urlExampleList.append(URL)
			
			else:
				print('\tINTERFACE: something went wrong with the input, defaulting to first URL example.')
				URL = urlExampleList[0]
			
			print('INTERFACE: selected URL %s' % URL)
			print('INTERFACE: enter an expiration duration (enter nothing to leave it unchanged)')
			inputExpiration = input('min> ')
			expDurationMin = None
			
			if inputExpiration:
				expDurationMin = float(inputExpiration)
			
			print('INTERFACE: preparing to fetch...')
			
			if URL in urlUsedList:
				print('\tFETCH: a cache object for this URL already exists!')
				
				obj = urlUsedList[URL]
				
				if expDurationMin:
					print('\tFETCH: an expiration duration was given (now %s)' % str(inputExpiration))
					obj.expTime = expDurationMin
				
				print('\tFETCH: fetching...')
				obj.fetch()
				
			else:
				print('\tFETCH: this URL does NOT already have a corresponding cache object, creating...')
				print('\tFETCH: fetching...')
				obj = Test_Container(URL, expDurationMin)
				urlUsedList[URL] = obj
				
		elif inputAction == 'l':
			if urlUsedList:
				print('INTERFACE: listing currently used URLs...')
				
				for item in urlUsedList:
					print('\tURL %s' % item)
			else:
				print('INTERFACE: nothing to list; no URLs have been used yet.')
			
		else:
			pass


# ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# ===== ===== ===== ===== ===== ===== ===== ===== ===== =====


if __name__ == '__main__':
	testInterface()
