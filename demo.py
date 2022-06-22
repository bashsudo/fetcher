import fetcher, time

fetcher.verboseOutput = True

url = 'https://www.raspberrypi.org/blog/'

previousHtml = None

fetcherBanner = '= = = = = = fetcher output = = = = = = '

def htmlDifferenceCheck():
	global previousHtml
	
	if previousHtml == html:
		print('DEMO DIFFERENCE CHECKER: the HTML returned by Fetcher is the SAME as the previous HTML (cache unchanged).')
	
	else:
		print('DEMO DIFFERENCE CHECKER: the HTML returned by Fetcher is DIFFERENT than the previous HTML (cache updated with fresh webpage request).')
	
	previousHtml = html


def htmlDifferenceExpectation(shouldBeSame=True):
	if shouldBeSame:
		print('DEMO : the HTML returned by Fetcher should be the SAME as the previously fetched HTML.')
	
	else:
		print('DEMO : the HTML returned by Fetcher should be DIFFERENT than the previously fetched HTML.')


# fetching: first time fetching the URL
# by default, the expiration time is 60 seconds
print('DEMO: now fetching for the first time.')
print('DEMO: by default, the expiration time is 1 minute (60 seconds).')
print(fetcherBanner)
html = fetcher.WebpageFetch(url)
htmlDifferenceCheck()
print('DEMO: fetched, waiting for 30 seconds.')

time.sleep(30)

# fetching: 30 seconds have passed; the cache has NOT expired yet
# the cache will be used and no page request will be made
print('\nDEMO: 30 seconds has passed, now fetching for the second time.')
htmlDifferenceExpectation(True)
print(fetcherBanner)
html = fetcher.WebpageFetch(url)
htmlDifferenceCheck()
print('DEMO: fetched, waiting for 35 seconds.')

time.sleep(35)

# fetching: 35 seconds have passed; the cache has expired
# (waited for an additional 5 seconds to ensure that the cache expired for sake of demo)
# the cache will now be updated with a fresh page request
# the expiration time will now be set to 6 seconds (1/10th of a minute)
print('\nDEMO: 10 seconds has passed, now fetching for the third time.')
htmlDifferenceExpectation(False)
print('DEMO: the expiration is now 6 seconds.')
print(fetcherBanner)
html = fetcher.WebpageFetch(url, expirationIntervalMin=0.1)
htmlDifferenceCheck()
print('DEMO: fetched, waiting for 10 seconds.')

time.sleep(10)

# fetching: 10 seconds have passed; the cache has expired
# (waited for an additional 4 seconds to ensure that the cache expired for sake of demo)
# the cache will now be updated with a fresh page request
# the expiration time will remain at 6 seconds without any arguments
html = fetcher.WebpageFetch(url)
htmlDifferenceCheck()

time.sleep(10)
