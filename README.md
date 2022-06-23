# fetcher
A system for creating and managing cache for website HTML files on local storage, complete with expiration times and garbage collection.

(include image here)

## Rationale and Motivation for the Project

## Installation and Basic Use

### Installing and Importing Fetcher
As of now, Fetcher can only be used by cloning the repository to your disk and importing Fetcher from your local clone. In the future, more elegant means of packaging such as PyPi will be utilized.

In terms of importing Fetcher, Fetcher itself is entirely self-contained in the **fetcher.py** file: other files such as **demo.py** and **tester.py** are NOT required for Fetcher to work. Therefore, you may cut/copy and paste **fetcher.py** into the same directory as another project, or vice versa, and use this import statement:

```
import fetcher
```

However, if you prefer importing Fetcher from its repository while your project is located elsewhere, you may need to follow an online tutorial for how to import Fetcher as a module in a different directory.

### Using Fetcher
Fetcher was designed to be a flexible, modular system that could be easily altered and built on with many functions; however, it is intended for developers to only use one single function in Fetcher: **WebpageFetch()**.

This is literally the one and only function you will likely ever use in Fetcher by design: this is a function that "automagically" retrieves, caches, and updates HTML documents. The developer wanting to use Fetcher does NOT need to know or study the inner-workings of Fetcher.

Therefore, this section and **demo.py** will cover the parameters and behavior of **WebpageFetch()**.

### WebpageFetch in General
Here is the pseudocode describing the overall behavior of WebpageFetch when it is called for a particular URL:

* **if**: URL/HTML in database (already cached)
	* **if**: the forced-update parameter is set to True
		* **action**: retrieve webpage and update cached HTML
	* **else, if**: the parameter is False (default)
		* **if**: the cache has expired
			* **action**: retrieve webpage and update cached HTML
		* **else**:
			* **action**: return the current cache without modifying it
* **else, if**: URL/HTML not in database (not already cached)
	* **action**: retrieve webpage and create a new cached HTML

### Situation #1: WebpageFetch Without Parameters
Without specifying the optional parameters...

* If given URL is already in the database (has already been cached):
	* The**WebpageFetch** will use the expiration duration that was last set (either the default 60 seconds or whatever **expirationIntervalMin** was last set to)
	* It will only make an official request to the website at the URL to update the cached HTML if it has expired.
* If the URL is NOT in the database (has not already been cached)...
	* It will make a request to the website and create a new cached HTML.

### Situation #2: Parameter - Forced Cache Update
* If the optional forced-update parameter **forceUpdateCache** is set to True, then the cache object will be updated with the latest copy of the webpage regardless of whether or not it has expired already.
* If there is no pre-existing cache for the given URL, then this has no effect: the latest copy of the webpage will be used either way for a new cached HTML.

### Situation #3: Parameter - Changing Expiration Duration
* If the optional expiration duration parameter **expirationIntervalMin** is set, then the expiration duration for the cached HTML of that particular URL is set to **expirationIntervalMin**.
* This will only have an effect on future calls to **WebpageFetch**, as the new expiration duration is not considered in the same call that set it.

## Fetcher in Action

### Demo Script

### Tester Script