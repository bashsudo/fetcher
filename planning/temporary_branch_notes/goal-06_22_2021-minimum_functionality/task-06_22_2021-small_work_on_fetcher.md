# SCRIPT: fetcher.py
* PURPOSE: used for making requests for webpages, but will automatically cache pages temporarily
* NOTES:
	* cached pages will expire after a certain amount of time
	* pages will be created based on their URL
		* however, the physical cache files on disk will have randomized names
	* there will be a central database file in plaintext (fetcher_db.txt)
		* has each cached page's URL, file name, date & time, etc.
* FUNCTIONALITY TREE/PSEUDOCODE:
	* when asked to make a request for a webpage:
		* look for existing cache
		* does cache exist?
			* check for expiration date and compare to current time


# fetcher_db.txt format
* every line will look like this:
	* <url> \t <filename> \t <ISO date+time created> \t <ISO date+time expiration>

# datetime - standard module notes
* datetime object: datetime.datetime
* datetime objects can be compared in later vs. earlier time with > & <
	* e.g. object1 > object2
* an existing datetime object can spit out its data as ISO: object.isoformat()
* a datetime object can be created FROM an ISO formatted string with: datetime.fromisoformat(...)

# Cache_Item class
* `__INIT__` PARAMETERS FOR ATTRIBUTES:
	* file name
	* url
	* current/creation time (datetime object)
	* expiration time (datetime object)
	* time interval between creation & expiration time (NOT timedelta, it is integer)