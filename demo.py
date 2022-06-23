"""
Fetcher: Webpage Retrieval and Caching System
2021 Eiza Stanford ("Bash Sudo" / "Charky Barky")

Demo Script
"""

# >>> FETCHER IMPORTS:
import fetcher

# >>> STANDARD LIBRARY IMPORTS:
import time

# ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# ===== ===== ===== ===== ===== ===== ===== ===== ===== =====

# enable verbose output in Fetcher
fetcher.verboseOutput = True

# the example URL used for the demo (anything can be used really)
url = 'https://www.raspberrypi.org/blog/'

# the banner separating the Fetcher output from the demo output
fetcherBanner = '= = = = = = fetcher output = = = = = = '

# corresponding words to phase numbers
namedNumberDict = {
	1:'first',
	2:'second',
	3:'third',
	4:'fourth',
	5:'fifth',
	6:'sixth'
}

# html-related vars
html = None
previousHtml = None

# ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# ===== ===== ===== ===== ===== ===== ===== ===== ===== =====

def demoStep(phaseNumber, summary, message, timePassed, timeWait, cacheShouldBeSame, expirationIntervalMin=None, forceUpdateCache=False):
	global html
	global previousHtml
	
	print('\n\nPHASE #%d: %s' % (phaseNumber, summary.upper()))
	
	namedNumber = namedNumberDict[phaseNumber]
	
	if phaseNumber == 1:
		print('\tDEMO (PHASE):\t\t\tThis is now phase #%d; fetching for the %s time.' % (phaseNumber, namedNumber))
	
	else:
		print('\tDEMO (PHASE):\t\t\t%d seconds have passed; this is now phase #%d; fetching for the %s time.'  % (timePassed, phaseNumber, namedNumber))
		
	
	print('\n\tDEMO (DEVELOPER COMMENTARY):\t%s\n' % '\n\t\t\t\t\t'.join(message))
	
	print(fetcherBanner)
	
	html = fetcher.WebpageFetch(url, expirationIntervalMin, forceUpdateCache)
	
	if phaseNumber > 1:
		
		if cacheShouldBeSame: 
			print('\tDEMO (DIFFERENCE EXPECTATION):\tThe HTML returned by Fetcher SHOULD be the SAME as the previously fetched HTML.')
		
		else:
			print('\tDEMO (DIFFERENCE EXPECTATION):\tThe HTML returned by Fetcher SHOULD be DIFFERENT than the previously fetched HTML.')
		
		
		if previousHtml == html:
			print('\tDEMO (HTML DIFFERENCE):\t\tThe HTML returned by Fetcher is IN FACT the SAME as the previous HTML (cache unchanged).')
		
		else:
			print('\tDEMO (HTML DIFFERENCE):\t\tThe HTML returned by Fetcher is IN FACT DIFFERENT than the previous HTML (cache updated with fresh webpage request).')
	
	previousHtml = html
	
	print('\tDEMO (NOW WAITING):\t\tFetching finished, now wating for another %d seconds...' % timeWait)
	
	time.sleep(timeWait)


# ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
# ===== ===== ===== ===== ===== ===== ===== ===== ===== =====


demoStep(phaseNumber =			1,
		summary =				'fetching for first time',
		message =				('Since we are fetching for the first time, the cache should be new and fresh.',
								'Also note that the default expiration time is 1 minute (60 seconds).',
								'With this in mind, the next phase and fetching will start in another 30 seconds.',
								'This is to demonstrate how the cached HTML for a URL will remain UNCHANGED if WebpageFetch is called before expiration.'),
		timePassed =			0,
		timeWait =				30,
		cacheShouldBeSame =		False)

		
demoStep(phaseNumber =			2,
		summary =				'unchanged HTML before expiration',
		message =				('The cached HTML should remain UNCHANGED at this point.',
								'However, the next phase will occur in another 30 seconds.',
								'At that point, the cached HTML would have expired and thus be updated.'),
		timePassed =			30,
		timeWait = 				35,
		cacheShouldBeSame =		True)


demoStep(phaseNumber =			3,
		summary = 				'HTML expired; setting new expiration time',
		message =				('The cached HTML has now expired: it will now be updated with the latest HTML retrieved from the webpage.',
								'Also, in this phase, the expiration time for that HTML/URL will be changed from the default 60 seconds to 6 seconds (1/10th of a minute).',
								'This is done by setting expirationIntervalMin=0.1 in WebpageFetch.'),
		timePassed =			35,
		timeWait =				10,
		cacheShouldBeSame =		False,
		expirationIntervalMin =	0.1)


demoStep(phaseNumber =			4,
		summary =				'HTML expired; expiration time persistence',
		message =				('Note that when no value is passed into expirationIntervalMin in calls to WebpageFetch, the expiration time that was last set for the particular HTML/URL is used.',
								'Normally, the last-set time is 60 seconds (the default), but in this case it is 6 seconds for that HTML/URL.',
								'Therefore, in this phase, no arguments will be passed in expirationIntervalMin to show that Fetcher remembers the now 6 second expiration.'),
		timePassed =			10,
		timeWait =				10,
		cacheShouldBeSame =		False)


demoStep(phaseNumber =			5,
		summary =				'HTML expired; going to wait before expiration',
		message =				('This phase will wait for 4 seconds, which is less than the expiration time of 6 seconds for our particular HTML/URL.',
								'Say that, instead of simply using the unchanged HTML like in phase #2, I wanted to FORCE the cache to update.',
								'This is can be done by setting the parameter "forceUpdateCache" to True in the call to WebpageFetch.',
								'The next phase will forcefully update the cache.'),
		timePassed =			10,
		timeWait =				4,
		cacheShouldBeSame =		False)


demoStep(phaseNumber =			6,
		summary =				'HTML has NOT expired; now forcing cache update',
		message =				('This phase will now forcefully update the cache by setting forceUpdateCache to True.',
								'This is also the last phase. Thank you for watching the demo!'),
		timePassed =			4,
		timeWait =				0,
		cacheShouldBeSame =		False,
		forceUpdateCache =		True)


print('THE DEMO HAS FINISHED; THANK YOU FOR YOUR PARTICIPATION!')
