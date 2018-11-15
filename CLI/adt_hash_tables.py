import adt

class hashTableNode:
	def __init__(self):
		self.idCol = ""
		self.item = ""

class HashTable(adt.ADT):
	def __init__(self, name, length):
		super().__init__(name, length, False) # pointer = False

		# Hash-Table's
		self.nodeArray = [hashTableNode() for i in range(self.numberOfNodes)]
		
		# Set all IDs initially to -1
		for index in range(self.numberOfNodes):
			self.nodeArray[index].idCol = "-1"		

		# Prompts
		# ID Prompt comes before item prompt so append was not used
		self.prompts["insert"].insert(0, 
			{"promptMsg": "Enter item ID <0 to 9999>", 
			"validator": self.isNewIdValid, 
			"valueName": "idForNewEntry"},
		)

		# Prompt for search by ID
		self.prompts["search"] = [
			{"promptMsg": "Enter ID to be searched for", 
			"validator": self.isSearchIdValid,
			"valueName": "idToBeSearchedFor"}
		]


		# Prompt for remove by ID
		self.prompts["remove"] = [
			{"promptMsg": "Enter the ID of the entry you wish to remove", 
			"validator": self.isSearchIdValid,
			"valueName": "idOfItemToBeRemoved"
		}
		]

		# Display Items
		self.addToDisplayData("ID", 10, self.getID)

		# Re-order so ID appears before Item
		self.dataItems = ["ID", "Item"]

	def getID(self, index):
		return self.nodeArray[index].idCol

	def __doc__(self):

		text = ["A hash table is an abstract data type",
		"Add more elaboration later..."
		]

		return super().__doc__(text)

	def isSearchIdValid(self, id):
		if not id.isdigit():
			return "The ID must be a number."

		elif not self.idWithinRange(id):
			return "The ID must be between 0 to 9999."

		else:
			return True

	def idAlreadyTaken(self, id):
		for node in self.nodeArray:
			if str(node.idCol) == str(id):
				return True

		return False 

	def idWithinRange(self, id):
		try:
			id = int(id)
		except:
			id = -1
		finally:
			isValid = ((id <= 9999) and (id >= 0))
			return isValid

	def isNewIdValid(self, id):
		if not id.isdigit():
			return "The ID must be a number."

		elif not self.idWithinRange(id):
			return "The ID must be between 0 to 9999."

		elif self.idAlreadyTaken(id):
			return "The ID has already been taken."

		else:
			return True

	def insert(self, idForNewEntry, itemToBeInserted):

		msg = [] # End message

		# Short-hand
		post = self.post
		rfr = self.refresh

		index = self.hash(int(idForNewEntry))
		
		currentPointer = index
		tableFull = False

		while not tableFull and self.nodeArray[currentPointer].idCol != "-1": # Exhaust table

			# Move to next position
			currentPointer += 1

			# If wrapping around needed
			if currentPointer >= len(self.nodeArray):
				currentPointer = 0

			# If the current pointer wraps back to initial position
			if currentPointer == index:
				tableFull = True

		if tableFull:
			msg.append("The item could not be added as the table is full.")

		else:

			self.nodeArray[currentPointer].idCol = str(int(idForNewEntry))
			self.nodeArray[currentPointer].item = itemToBeInserted

			msg.append("The item was added successfully at index {}.".format(currentPointer))

		return msg

	def remove(self, idOfItemToBeRemoved):

		msg = [] # End message

		# Short-hand
		post = self.post
		rfr = self.refresh

		index = self.hash(idOfItemToBeRemoved)

		pointer = index

		itemNotFound = False

		while not itemNotFound and idOfItemToBeRemoved != self.nodeArray[pointer].idCol:

			pointer += 1 # Traverse

			if pointer >= len(self.nodeArray): # Wrap if necessary
				pointer = 0

			if pointer == index: # Back to the start?
				itemNotFound = True

		if itemNotFound:
			msg.append("No entry with that ID was found.")

		else:
			# Empty the node
			self.nodeArray[pointer].item = ""
			self.nodeArray[pointer].idCol = "-1"

			msg.append("Entry was found at index {} and removed.".format(pointer))

		return msg

	def search(self, idToBeSearchedFor):
		"""Allows for searching the hash table for an item through its ID. Retrieves first instance."""
		msg = [] # End message

		# Short-hand
		post = self.post
		rfr = self.refresh

		idToBeSearchedFor = int(idToBeSearchedFor)

		index = self.hash(idToBeSearchedFor)
		pointer = index

		tableExausted = False

		while not tableExausted and idToBeSearchedFor != self.nodeArray[pointer].idCol:

			pointer += 1 # Traverse

			if pointer >= len(self.nodeArray): # Wrap if necessary
				pointer = 0

			if pointer == index: # If back to start
				tableExausted = True

		if not tableExausted:
			msg.append("Entry found at index {},".format(pointer))
			msg.append("Item: {}".format(self.nodeArray[pointer].item))

		else:
			msg.append("No entry with that ID was found.")

		return msg

	def hash(self, key):
		key = int(key)
		return key % self.numberOfNodes # Gives modulus appropriate to number of nodes
