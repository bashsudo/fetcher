import fetcher
#from bs4 import BeautifulSoup
import pathlib

fetcher.verboseOutput = True

class Tester:
	
	def tell(self, who, message, prefix=''):
		print('>>> TESTER SYSTEM (LINK %s):%s (%s) %s' % (self.linkShort, prefix, who, message))
	
	
	#def sitePiScrape(self):
	#	soup = BeautifulSoup(self.html, 'lxml')
	#	
	#	blogList = soup.find_all('li', class_='c-blog-post-loop__item')
	
	
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
		self.html = fetcher.WebpageFetch(self.link, self.expTime)
		self.tell('fetch', 'finished call WebpageFetch')
		
		if self.html:
			self.tell('fetch', 'SUCCESS: HTML OK')
		else:
			self.tell('fetch', 'FAILURE: NO HTML (None type in html)!')
		
		if differenceCheck:
			self.htmlDumpRead()
			self.tell('fetch', 'DUMP COMPARE BEGIN:')
			
			if self.htmlDump == self.html:
				self.tell('fetch', 'DUMP SAME', '\t')
			else:
				self.tell('fetch', 'DUMP DIFFERENT', '\t')
		
		if dumpUpdate:
			self.htmlDumpWrite()
			self.tell('fetch', 'dump written')
	
	
	def __init__(self, link, expTime):
		self.link = link
		self.linkShort = '-'.join(link.split('//')[1].split('.')).replace('/','X')
		
		self.dumpPath = 'dump_html_%s.html' % self.linkShort
		
		self.expTime = expTime
		
		self.html = None
		self.htmlDump = None
		
		self.fetch()


if __name__ == '__main__':
	t1 = Tester('https://time.is/', 0.1)
	t2 = Tester('https://www.raspberrypi.org/blog/', 0.2)
