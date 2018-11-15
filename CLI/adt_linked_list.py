import adt

class LinkedList(adt.ADT):

	def __doc__(self):
		text = ["A linked list is an abstract data type",
		"",
		"Add more elaboration later..."
		]

		return super().__doc__(text)

	def getFreePointer(self):
		return self.freePointer

	def getHeadPointer(self):
		return self.headPointer

	def __init__(self, name, length):
		super().__init__(name, length, True) # pointer = True

		# Linked-List's pointers

		self.freePointer = 0
		self.headPointer = -1

		# Linked-List's node array

		self.nodeArray = [adt.linkNode() for i in range(self.numberOfNodes)]
		self.initialize(self.nodeArray)

		# Overwrite

		self.pointers = ["Free Pointer", "Head Pointer"]
		self.pointerNameToMethod = {"Free Pointer": self.getFreePointer, 
			"Head Pointer": self.getHeadPointer}

		# Prompt for remove by ID
		self.prompts["remove"] = [
			{"promptMsg": "Enter the value of the item (case-sensitive) you wish to remove", 
			"validator": lambda x: True,
			"valueName": "itemToBeRemoved"
		}
		]

	def insert(self, itemToBeInserted):

		if self.freePointer == -1:	# Eligibility Check
			
			self.post("Error - list is full.")

		else:
			
			newNodePointer = self.freePointer 
			self.nodeArray[newNodePointer].item = itemToBeInserted # Operation Of Interest
			self.freePointer = self.nodeArray[newNodePointer].pointer # Free List

			nextNodePointer = self.headPointer
			while nextNodePointer != -1 and self.nodeArray[nextNodePointer].item < itemToBeInserted: # Traversal

				previousNodePointer = nextNodePointer
				nextNodePointer = self.nodeArray[previousNodePointer].pointer

			if nextNodePointer == self.headPointer: # Flow Correction
				
				self.headPointer = newNodePointer # Special Pointers
			else:

				self.nodeArray[previousNodePointer].SetPointer(newNodePointer) # Data List

			self.nodeArray[newNodePointer].pointer = nextNodePointer

	def search(self, itemToBeSearched):

		thisNode = self.headPointer

		while thisNode != -1 and self.nodeArray[thisNode].item < itemToBeSearched:

			thisNode = self.nodeArray[thisNode].pointer

		if thisNode != -1 and self.nodeArray[thisNode].item == itemToBeSearched:
			return thisNode
		else:
			return -1

	def remove(self, itemToBeRemoved):
		
		currentPointer = self.headPointer

		while currentPointer != -1 and self.nodeArray[currentPointer].item < item: # Traverse

			previousNodePointer = currentPointer
			currentPointer = self.nodeArray[currentPointer].pointer


		if self.nodeArray[currentPointer].item != item: # Eligibility check
			if self.headPointer == -1:
				self.post("List is empty.")
			else:
				self.post("Entry not found")
		else:
	
			nextPointer = self.nodeArray[currentPointer].pointer
			if self.headPointer == currentPointer:
				self.headPointer =  nextPointer # Special Pointers

			else:
				self.nodeArray[previousNodePointer].pointer = nextPointer # Data list ->.

			self.nodeArray[currentPointer].item = ""

			self.nodeArray[currentPointer].pointer = self.freePointer # Free list .->
			self.freePointer = currentPointer 
