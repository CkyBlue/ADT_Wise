import os

"""	adt_wise_data is the data module for the adt_wise app, 
it handles reading and writing objects and maintaining the index

TODO - Implementing objectStore through SQLite3
Index through json
"""

adtNames = [] # Index File
adtType = {} # Index File
objectStore = {} # Represents database

def loadObj(name):
	# Modify to read form database
	return objectStore[name]

def loadAllADTNames():
	# Modify to read from file
	return adtNames

def loadAllADTTypes():
	# Modify to read from file
	return adtType

def dumpObject(name, obj):
	objectStore[name] = obj

def updateIndex(name, ADTtype):
	adtNames.append(name)
	adtType[name] = ADTtype

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

