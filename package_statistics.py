#!/bin/env python
""" This script is written to download a Contents file associated with architecture (amd64, arm64, mips etc).
    Note you need to pass the udeb along with the archiecture when you want to see  
    the statistics of udeb packages example like udeb-amd64 instead of just amd64. 
"""

# Import python modules
import sys
import re
import gzip
import urllib
from collections import Counter

# Assign arg to a variable
architecture = sys.argv[1].lower()

"""
  Construct a url based on user input which is straight forward
  our goal is defined to extract content files so we don't need to parse all the html href tags
  with below url definition we can directly extract url we wanted for the architecture 
"""
url = 'http://ftp.uk.debian.org/debian/dists/stable/main/Contents' + '-' + architecture + '.gz'
print url

"""
  Create a empty list, this list will store the package names which gets appended when we extract file in Package_statistics fuction
"""
PackageNames = []

def package_statistics(url):
	"""
		We have existing module in python for parsing url's, here we are using ulllib which connects to url and downloads the package
	"""
	connect = urllib.URLopener()
	connect.retrieve(url, "file.gz")
	"""
		Below code extracts the gunzip file with gzip and spliting the lines with regular expression module.
		We could use split fuction but here we are spliting the lines with two delimeters which is better doing with
		regular expressions. After the split we are extracting the PackageName and appending it to PackageNames list.
	"""
	with gzip.open('file.gz', 'rb') as f:
		for line in f:
			str = re.split(', |/', line)
			PackageNames.append(str[-1])

	"""
		Counter function from Collections python package used for counting the occurence of the package names and converting the 
		list to dictionary, this code is meant to find the number of files associated with the package so each occurence represents
		its associated file, here number of associated files of a package exactly equal to package name occurence in the list.

	"""
	PackageDict = Counter(PackageNames)
	for PackageName, NumberOfFilesAssociatedToPackage in PackageDict.most_common(10):
		PackageName = PackageName.rstrip('\n')
		print "{:20s} <--- {}".format(PackageName, NumberOfFilesAssociatedToPackage)
	


"""
	We are using variable stats to call function by passing url as parameter. When we print stats we should expect a tabular 
	representation of data of top 10 packages with most number of associated files.
"""
stats = package_statistics(url)
if stats is not None:
	print stats



  

