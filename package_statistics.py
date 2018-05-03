#!/bin/env python
""" 
    This script is written to download a Contents file associated with architecture (amd64, arm64, mips etc).
    Note this will also extract and process Contents-udeb-* if the architecture matches. 
"""

# Import python modules
import sys
import re
import gzip
import urllib, urllib2
from BeautifulSoup import BeautifulSoup
from collections import Counter

# Assign arg to a variable
architecture = sys.argv[1].lower()


"""
   Empty list for contents file (We can expect more than one content file based on architecture) and 
   for storing list of packages from each file. 
"""

files = []
packageNames = []
debrepo = "http://ftp.uk.debian.org/debian/dists/stable/main/"

"""
   FilesExtract fuction will parse the url and extracts the file names based on the filters which is 
   a regular expression by having extracted with Contents with lookup ahead with architecture
"""

def FilesExtract():
    html_page = urllib2.urlopen(debrepo)
    soup = BeautifulSoup(html_page)
    filter = 'Contents(?=.*' + str(architecture) + ')'
    for link in soup.findAll('a',  attrs={'href': re.compile(filter)}):
    	files.append(link.get('href'))
    return files

"""
  Create a empty list, this list will store the package names which gets appended when we extract file in Package_statistics fuction
"""
#PackageNames = []

def package_statistics():
	
	ContentFiles = FilesExtract()

	"""
		From line 62 to 70, code extracts the gunzip file with gzip and spliting the lines with regular expression module.
		We could use split fuction but here we are spliting the lines with two delimeters which is better doing with
		regular expressions. After the split we are extracting the PackageName and appending it to PackageNames list.
	"""
	
	""" 
		From line number 71 to 35 we are using Counter method from Collections package which helping the program to convert the list to
		Dict by the having value as number of occurence of the word key. The number of occurence is exactly equal to 
		the number of files associated and we are having print format to output data in tabular form.
	"""

	for file in ContentFiles:
		packageNames = []  # Resetting packageNames list
		url = debrepo + file
		connect = urllib.URLopener()
		connect.retrieve(url, "file.gz")
		with gzip.open('file.gz', 'rb') as f:
			for line in f:
				str = re.split(', |/', line)
				packageNames.append(str[-1])
		PackageDict = Counter(packageNames)
		print "The top 10 packages that have the most files associated for : %s" % (file)
		for PackageName, NumberOfFilesAssociatedToPackage in PackageDict.most_common(10):
			PackageName = PackageName.rstrip('\n')
			print "{:20s} <--- {}".format(PackageName, NumberOfFilesAssociatedToPackage)
    

"""
	We are using variable stats to call function by passing url as parameter. When we print stats we should expect a tabular 
	representation of data of top 10 packages with most number of associated files.
"""
stats = package_statistics()
if stats is not None:
	print stats



  

