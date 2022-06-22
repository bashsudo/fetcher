import fetcher, time

fetcher.verboseOutput = True

url = 'https://www.raspberrypi.org/blog/'

fetcherBanner = '= = = = = = fetcher output = = = = = = '

def htmlDifferenceCheck():
	global previousHtml
	
	if previousHtml == html:
		print('DEMO DIFFERENCE CHECKER: the HTML returned by Fetcher is in fact the SAME as the previous HTML (cache unchanged).')
	
	else:
		print('DEMO DIFFERENCE CHECKER: the HTML returned by Fetcher is in fact DIFFERENT than the previous HTML (cache updated with fresh webpage request).')
	
	previousHtml = html


def htmlDifferenceExpectation(shouldBeSame=True):
	if shouldBeSame:
		print('DEMO DIFFERENCE EXPECTATION: the HTML returned by Fetcher should be the SAME as the previously fetched HTML.')
	
	else:
		print('DEMO DIFFERENCE EXPECTATION: the HTML returned by Fetcher should be DIFFERENT than the previously fetched HTML.')



# fetching: first time fetching the URL
# by default, the expiration time is 60 seconds
print('DEMO: now fetching for the first time.')
print('DEMO: by default, the expiration time is 1 minute (60 seconds).')
print(fetcherBanner)

html = fetcher.WebpageFetch(url)
previousHtml = html

print('DEMO: fetched, waiting for 30 seconds (half of the 60 second expiration time).')

time.sleep(30)



# fetching: 30 seconds have passed; the cache has NOT expired yet
# the cache will be used and no page request will be made
print('\n\nDEMO: 30 seconds have passed, now fetching for the second time.')
print(fetcherBanner)

html = fetcher.WebpageFetch(url)
htmlDifferenceExpectation(True)
htmlDifferenceCheck()

print('DEMO: fetched, waiting for 35 seconds.')

time.sleep(35)



# fetching: 35 seconds have passed; the cache has expired
# (waited for an additional 5 seconds to ensure that the cache expired for sake of demo)
# the cache will now be updated with a fresh page request
# the expiration time will now be set to 6 seconds (1/10th of a minute)
print('\n\nDEMO: 10 seconds have passed, now fetching for the third time.')
print('DEMO: the expiration has been set to 6 seconds (originally 60 seconds as per default setting).')
print(fetcherBanner)

html = fetcher.WebpageFetch(url, expirationIntervalMin=0.1)
htmlDifferenceExpectation(False)
htmlDifferenceCheck()

print('DEMO: fetched, waiting for 10 seconds.')

time.sleep(10)



# fetching: 10 seconds have passed; the cache has expired
# (waited for an additional 4 seconds to ensure that the cache expired for sake of demo)
# the cache will now be updated with a fresh page request
# the expiration time will remain at 6 seconds without any arguments
print('\n\nDEMO: 10 seconds have passed, now fetching for the fourth time.')
print('DEMO: this time, no new expiration time will be passed into WebpageFetch.')
print('DEMO: this means that WebpageFetch will use whatever expiration time was previously set (in this case, 6 seconds).')
print(fetcherBanner)

html = fetcher.WebpageFetch(url)
htmlDifferenceExpectation(False)
htmlDifferenceCheck()

print('DEMO: fetched, waiting for 10 seconds.')

time.sleep(10)



# fetching: 10 seconds have passed; the cache has expired
# (waited for an additional 4 seconds to ensure that the cache expired for sake of demo)
# the expiration time will remain at 6 seconds, HOWEVER the script will wait for 4 seconds (before cache expires0
# with this in mind, it will later FORCEFULLY update the cache so it updates despite not being expired
print('\n\nDEMO: 10 seconds have passed, now fetching for the fifth time.')
print(fetcherBanner)

html = fetcher.WebpageFetch(url)
htmlDifferenceExpectation(False)
htmlDifferenceCheck()

print('DEMO: fetched, waiting for 4 seconds.')
print('DEMO: 4 seconds is less than the 6 second expiration time, and say I wanted the cache to be updated before it expires.')
print('DEMO: to do this, we will later forcefully update the cache; this way, the cache is updated regardless of whether or not it has expired.')

time.sleep(4)



# fetching: 4 seconds have passed; the cache has NOT expired yet
# here is where it will now FORCEFULLY update the cache
# WebpageFetch will now be called with parameter "forceUpdateCache" set to True
print('\n\nDEMO: 4 seconds has passed, now fetching for the sixth time.')
print('DEMO: The cache will now be forcefully updated; WebpageFetch will now be called with forceUpdateCache set to True.')
print(fetcherBanner)

html = fetcher.WebpageFetch(url, forceUpdateCache=True)
htmlDifferenceExpectation(False)
htmlDifferenceCheck()

print('DEMO: the demo has finished, thank you for your participation!')
