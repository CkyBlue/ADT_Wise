from adt_queue import Queue
from adt_hash_tables import HashTable

import adt_wise_data as data

# Link call name to ADT class here
ADTS = {"queue": Queue, "hash table": HashTable}

class undoNode:
	def __init__(self):
		self.obj = None
		self.pointer = -1

class undoGroup:
	def __init__(self, length):
		self.numberOfNodes = length
		self.objArray = [undoNode() for i in range(int(self.numberOfNodes))]

		# Setting up the free list
		for i in range(self.numberOfNodes):
			self.objArray[i].pointer = i + 1

		self.objArray[self.numberOfNodes - 1].pointer = -1

		self.freePointer = 0
		self.headPointer = -1
		self.tailPointer = -1

	def addToGroup(self, obj):

		if self.freePointer == -1: # If group is full, use head

			# Move to current head pointer
			currentPointer = self.headPointer

			# Use index pointed to by head as next head
			self.headPointer = self.objArray[currentPointer].pointer

		else: # If group is not full, use a free index

			# Move to free pointer
			currentPointer = self.freePointer

			# Use index pointed to by free pointer as the next free pointer
			self.freePointer = self.objArray[currentPointer].pointer

			# If head pointer not setup,
			if self.headPointer == -1: 

				# Set up current as head
				self.headPointer = currentPointer

		if self.tailPointer != -1: # If previous tail exists
			# Previous tail points to the newest addition
			self.objArray[self.tailPointer].pointer = currentPointer

		# Set addition as the tail
		self.tailPointer = currentPointer

		# Putting argument object at index
		self.objArray[self.tailPointer].obj = obj

		# Tail doesn't point to anything
		self.objArray[self.tailPointer].pointer = -1

	def getMostRecentAddition(self):
		pass

def fetchIndex():
	"""Returns [[<adt-name>, <adt-type>], ]"""
	return data.loadIndex()

def getavailableADTCallNames():
	"""Returns [<adt-call-name>, ]"""
	return list(ADTS.keys())

def getADTFromCallName(adtCallName):
	if adtCallName in getavailableADTs():
		return ADTS[adtCallName]
	else:
		return None


def retrieveAllAvailableObjs():
	"""Returns {<obj_name>: <obj>,} """

	availableObjs = {}

	objList = fetchIndex()
	for objName in objList.keys():
		obj = data.loadObj(objName)
		availableObjs[objName] = obj

	return availableObjs

def retrieveObj(objName):
	return data.loadObj(objName)


def createADT(nameOfADT, typeOfADT, numberOfNodes):
	thisObj = getavailableADTs()[typeOfADT](nameOfADT, numberOfNodes)
		
	data.dumpObject(nameOfADT, thisObj)
	data.updateIndex(nameOfADT, typeOfADT)




 