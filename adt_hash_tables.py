"""Methods that need to avilable for access through call names
need to be appended appropriately to the getMethods function.

If the function needs arguments, the prompt, validator and the argument name need
to be served through the getInputPrompts function.

The validator returns True if valid, else the error message

Each function shows its working through a real-time log
Information is added to the log through the function self.post(<Info-String>)
Each time self.__refresh is fired the info in the log is displayed

The return of each function, conventionally msg, is a list of strings
it serves as the response message
It is handled differently from logs

If action is detailed in the log, it should fire after the refresh so that 
actions mentioned in the log are only observed when pressing enter brings the
next refresh and user can follow the change more easily by 
knowing where to look 

The info that shows up through 'help <command-name>'
is the doc-string

The arguments that the methods with call names receive 
are meant to be string. idCol is implemented as integer so
care should be taken when dealing with it."""

## TODO - Add log postings
## Add elaboration to __doc___

class node:
	def __init__(self):
		self.idCol = 0
		self.data = ""

class HashTable:
	def __init__(self, name, length):
		self.__name = name
		self.numberOfNodes = int(length)

		self.nodeArray = [node() for i in range(self.numberOfNodes)]
		self.initializeId(self.nodeArray)

		self.__refresh = (lambda: None)
		self.usesPointers = False
		self.__log = []

	def initializeId(self, obj): # Set all IDs initially to -1
		for index in range(len(obj)):
			obj[index].idCol = -1
###
	def __doc__(self):
		# Return the text with each element on its own separate line

		text = ["A hash table is an abstract data type",
		"Add more elaboration later..."
		]

		output = ""

		for i in text:
			if i != (len(text) - 1) :
				output += i + "\n"
			else:
				output += i

		return output
###
	def setLog(self, newLog):
		self.__log = newLog
###
	def getLog(self):
		return self.__log
###
	def setRefresher(self, func):
		self.__refresh = func
###
	def setName(self, name):
		self.__name = name
###
	def getName(self):
		return self.__name
###
	def getAllIds(self):
		return [self.nodeArray[i].idCol for i in range(self.numberOfNodes)]
###
	def isIdValid(self, id):
		if not id.isdigit():
			return "The ID must be a number."

		elif id <= "9999" and id >= "0":
			return "The ID must be between 0 to 9999."

		elif id in self.getAllIds():
			return "An entry with this ID already exists."

		else:
			return True
####
	def isSearchIdValid(self, id):
		if not id.isdigit():
			return "The ID must be a number."

		elif id <= "9999" and id >= "0":
			return "The ID must be between 0 to 9999."

		else:
			return True

###
	def getInputPrompts(self):
		"""Returns data that allows the user interface to send data properly to functions that need arguments"""

		prompts = {}

		# Each dictionary is the data pertaining to one input
		# valueName must match the name of the parameter for the function,
		# eg, "valueName": "idVal" for <call-name-func>(idVal)

		prompts["insert"] = [
		# Prompt for ID
			{"promptMsg": "Enter item ID <0 to 9999>", 
			"validator": self.idIsValid, 
			"valueName": "idForNewEntry"},
		
		# Prompt for value
			{"promptMsg": "Enter item to be inserted", 
			"validator": lambda x: None,
			"valueName": "dataForNewEntry"}
		]

		prompts["search"] = [
		# Prompt for ID
			{"promptMsg": "Enter ID to be searched for", 
			"validator": lambda x: None,
			"valueName": "itemToBeSearched"}
		]


		########
		prompts["remove"] = [
		{"promptMsg": "Enter the ID of the entry you wish to remove", 
		
		"validator":lambda x: x.isdigit() and x <= "9999" and x >= "0", # Anonymous func for validation
		"errorMsg": "The ID can be numbers only \nand between 0 to 9999.",
		
		"valueName": "idOfItemToBeRemoved"
		}
		]

		return prompts

	def __str__(self):
		return self.__name

	def insert(self, idForNewEntry, dataForNewEntry):

		msg = [] # End message

		# Short-hand
		post = self.post
		rfr = self.__refresh

		index = self.hash(idForNewEntry)

		currentPointer = index
		tableFull = False

		while not tableFull and self.nodeArray[currentPointer].idCol != 0: # Exhaust table

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

			self.nodeArray[currentPointer].idCol = int(idForNewEntry)
			self.nodeArray[currentPointer].data = dataForNewEntry

			msg.append("The item was added successfully at index {}".format(currentPointer))

		return msg

	def remove(self, idOfItemToBeRemoved):

		msg = [] # End message

		# Short-hand
		post = self.post
		rfr = self.__refresh

		idOfItemToBeRemoved = int(idOfItemToBeRemoved)

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
			self.nodeArray[pointer].data = ""
			self.nodeArray[pointer].idCol = 0

			msg.append("Entry was found at index {} and removed.".format(pointer))

		return msg

	def search(self, idToBeSearchedFor):
		"""Allows for searching the hash table for an item through its ID. Retrieves first instance."""
		msg = [] # End message

		# Short-hand
		post = self.post
		rfr = self.__refresh

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
			msg.append("Data: {}".format(self.nodeArray[pointer].data))

		else:
			msg.append("No entry with that ID was found.")


	def hash(self, key):
		""""""

		key = int(key)
		return key % self.numberOfNodes # Gives modulus appropriate to number of nodes
