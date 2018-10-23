from adt_queue import Queue
from adt_hash_tables import HashTable
from adt_stack import Stack
from adt_linked_list import LinkedList
from adt_binary_tree import BinaryTree

# Call names would be names used to refer to an ADT, for eg: queue
# Obj names would be names assigned to objects made from ADT classes

# Link call name to ADT class here
ADTS = {"queue": Queue, "binary-tree": BinaryTree, "stack": Stack,
	"hash-table": HashTable, "linked-list": LinkedList}

adtNames = []
adtType = {}
objectStore = {}

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

def fetchAllADTObjNames():
	"""Returns [<user-designated-adt-name>, ]"""
	return adtNames

def deleteADTObj(ADTname):
	if ADTname in fetchAllADTObjNames():

		adtNames.remove(ADTname)
		adtType.pop(ADTname)
		objectStore.pop(ADTname)

		return True
	else:
		return False

def getAvailableADTCallNames():
	return ADTS.keys()

def getADTTypeFromName(adtName):
	if adtName in fetchAllADTObjNames():
		return adtType[adtName]
	else:
		return None

def getADTClassFromCallName(adtCallName):
	if adtCallName in getAvailableADTCallNames():
		return ADTS[adtCallName]

	else:
		return None

def retrieveADTObjectByName(adtName):
	if adtName in fetchAllADTObjNames():
		return objectStore[adtName]
	else:
		return None

def createADT(nameOfADT, typeOfADT, numberOfNodes):
	thisObj = getADTClassFromCallName(typeOfADT)(nameOfADT, numberOfNodes)
		
	objectStore[nameOfADT] = thisObj

	adtNames.append(nameOfADT)
	adtType[nameOfADT] = typeOfADT