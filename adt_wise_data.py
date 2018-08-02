import os

"""	adt_wise_data is the data module for the adt_wise app, 
it handles reading and writing objects and maintaining the index

TODO - Implementing objectStore through SQLite3
Index through json
"""

index = [] # Represents index File
objectStore = {} # Represents database

def loadObj(name):
	# Modify to read form database
	return objectStore[name]

def loadIndex():
	# Modify to read from file
	return index

def dumpObject(name, obj):
	objectStore[name] = obj

def updateIndex(name, ADTtype):
	index.append([name, ADTtype])

def _fetchBaseAddress():
	try:
		appPath = os.environ["HOME"] or os.environ["HOMEPATH"]
		if not os.path.exists(appPath):
			appPath = os.getcwd()
	except (TypeError, KeyError):
		appPath = os.getcwd()
	return appPath
	
def readObjFromFile():
	pass

