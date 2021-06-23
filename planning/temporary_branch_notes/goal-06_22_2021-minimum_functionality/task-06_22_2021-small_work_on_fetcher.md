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
	* <url> \t <filename> \t <date and time created>