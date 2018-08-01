"""Methods that need to avilable for access through call names
need to be appended appropriately to the getMethods function.

If the function needs arguments, the prompt, validator and error-message need
to be served through the getInputPrompts function.

Each function shows its working through a log
Information is added to the log through the function self.post(<Info-String>)
Each time self.__refresh, or rfr in the short-hand form, is fired the info in the log is displayed

The return is a list of strings
it serves as the response message
It is handled somewhat differently from logs

The action detailed in the log should fire after the refresh so that 
changes mentioned are only observed when pressing enter brings the
next refresh and user can follow the change more easily by 
knowing where to look 

The info that shows up through 'help <command-name>'
is the doc-string, the text in the triple quotation mark comments  
"""

class node:
	def __init__(self):
		self.item = ""
		self.pointer = -1

class queue:
	def post(self, content):
		self.__log.append(content)

	def __doc__(self):
		text = ["A queue is an abstract data type",
		"which works on the principle of Last in, first out.",
		"",
		"Add more elaboration later..."
		]

		output = ""

		for i in text:
			if i != (len(text) - 1) :
				output += i + "\n"
			else:
				output += i

		return output

	def __init__(self, name, length):

		self.__name = name
		self.numberOfNodes = int(length)

		self.__refresh = (lambda: None)

		self.usesPointers = True

		self.nodeArray = [node() for i in range(int(self.numberOfNodes))]
		self.__initialize(self.nodeArray)

		self.freePointer = 0
		self.headPointer = -1
		self.tailPointer = -1

		self.dataItems = ["Item", "Pointer"]
		self.dataItemsWidth = {"Item": 20, "Pointer": 10}
		self.dataItemsRetrievingFunc = {"Item": self.getItem, "Pointer": self.getPointer}

		self.__log = []

	def setLog(self, newLog):
		self.__log = newLog

	def getLog(self):
		return self.__log

	def setRefresher(self, func):
		self.__refresh = func

	def setName(self, name):
		self.__name = name

	def getName(self):
		return self.__name

	def getInputPrompts(self):
		"""Returns data that allows the user interface to send data properly to functions that need arguments"""

		prompts = {}

		# The dictionary is inside an array so that if a single command need multiple values, the existing system permits
		# valueName must match the name of the parameter for the function

		prompts["insert"] = [

		{"promptMsg": "Enter item to be inserted", 
		"validator": lambda x: len(x) <= 20 and x.replace(" ", "").isalnum(), # Anonymous func for validation
		"errorMsg": "The item must be shorter than 20 letters, \nand aside from spaces must contain only alpha-numeric characters.",
		"valueName": "itemToBeInserted"

		}
		]

		prompts["search"] = [

		{"promptMsg": "Enter item to be inserted", 
		"validator": lambda x: True, # No validation needed
		"errorMsg": "The item must be shorter than 20 letters, \nand aside from spaces must contain only alpha-numeric characters.",
		"valueName": "itemToBeSearched"

		}
		]

		return prompts

	def __str__(self):
		return self.__name

	def getSpecialPointers(self):
		pointers = ["Free Pointer", "Head Pointer", "Tail Pointer"]
		return pointers

	def getPointersValue(self, pointer):
		valuesDict = {"Free Pointer": self.freePointer,
		"Head Pointer": self.headPointer, 
		"Tail Pointer": self.tailPointer}
		return valuesDict[pointer]

	def getMethods(self):
		"""Returns a dictionary with call name for keys, 
		the function associated for values.
		"""

		return {"insert": self.insert, 
		"search": self.search,
		"remove": self.remove}

	def getItem(self, index):
		return self.nodeArray[index].item

	def getPointer(self, index):
		return self.nodeArray[index].pointer

			
	def __initialize(self, obj):
		lenght = len(obj)
		for index in range(lenght):
			obj[index].pointer = index + 1
		obj[lenght - 1].pointer = -1

	def insert(self, itemToBeInserted):
		"""Allows for adding an item to the tail of the queue if it is not full."""

		newItem = itemToBeInserted

		msg = []

		# Short-hand
		post = self.post
		rfr = self.__refresh

		post("Checking eligibility...")
		post("Free Pointer: {}".format(self.freePointer))

		rfr()

		# Check eligibility
		if self.freePointer == -1:
			post("Pointer to free node is null.")
			post("Error, there is no empty node.")

			rfr()

			msg.append("Item could not be inserted.")
			return {"Status": 0, "Message": msg}


		else:
		# Handle key operation
			post("Moving to free node...")
			post("Setting item at free node to {}".format(newItem))
			

			rfr()
			currentPointer = self.freePointer
			self.nodeArray[currentPointer].item = newItem 

		# Correct Flow
			post("Correcting links...")

			pointerTo = self.nodeArray[currentPointer].pointer
			post("Since the index value {} that the current node points to is to be overwritten,".format(pointerTo))
			post("Correction uses that address first.\n")

			post("Since current node is linked into the free list,")
			post("the index it points to can be used as the next free pointer.")
			post("New free pointer: {}".format(pointerTo))

			rfr()

			# Free list
			self.freePointer = pointerTo 

			# Data list			
			if self.tailPointer != -1:
				post("As for the data list,")
				post("Since the pointer to the tail is to be modified, the process involving it is then handled.\n")

				post("The previous tail at index {} is set to point to the current tail at {},".format(self.tailPointer,
					currentPointer),
					logger)
				post("so that when the previous tail is popped on reaching the head of the queue,")
				post("the program will be able to read the next head from it,")

				rfr()
				self.nodeArray[self.tailPointer].pointer = currentPointer			
			
			post("Since current node is now the new tail, it does not need to point to anything.")
			post("Thus, the current node should point to: {}".format(-1))
		
			rfr()
			
			self.nodeArray[currentPointer].pointer = -1

			post("Modifying special pointers...")
			post("New tail pointer: {}".format(currentPointer))

			rfr()

			self.tailPointer = currentPointer

			post("We have,")
			post("Head pointer: {}".format(self.headPointer))

			if self.headPointer == -1:
				post("Since the current node is the new head, the head pointer is modified...")
				post("New head pointer: {}".format(currentPointer))

				rfr()

				self.headPointer = currentPointer

			post("All done.")
			rfr()

			msg.append("Item successfully inserted.")

			return msg

	def search(self, itemToBeSearched):
		"""Allows for searching the queue for an item. Retrieves first instance."""

		msg = [] # Holds message that is displayed after the logs

		# Short-hand
		post = self.post
		rfr = self.__refresh()

		post("Moving to the head-pointer...")
		post("Current Pointer: {}".format(self.headPointer))

		rfr()

		currentPointer = self.headPointer
		itemFound = False

		if currentPointer == -1: # If list is empty

			post("List is empty.")
			msg.append("Item could not be located.")
			rfr()
		
		else:
			while currentPointer != -1 and not itemFound:
				post("Item at current position: {}".format(self.nodeArray[currentPointer].item))
				post("Item being searched: {}\n".format(itemToBeSearched))

				if self.nodeArray[currentPointer].item == itemToBeSearched:
					post("The two are the same,")
					post("The item at {} matched.".format(currentPointer))

					msg.append("The item {} was found at index {}".format(itemToBeSearched, currentPointer))
					itemFound = True

				else:
					post("The two do not match,")
					post("Current node points: {}\n".format(self.nodeArray[currentPointer].pointer))

					post("Moving to next node,")
					post("Current Pointer: {}".format(self.nodeArray[currentPointer].pointer))
					
					currentPointer = self.nodeArray[currentPointer].pointer

				rfr()

			if not itemFound:

				post("Finished checking all occupied nodes,")
				post("No match found.")

				rfr()

				msg.append("Item could not be located.")
			else:
				post("All done.")
				rfr()

		return msg

	def remove(self):
		"""Allows for removing a particular entry from the ADT."""

		msg = [] # Holds message that is displayed after the logs

		# Short-hand
		post = self.post
		rfr = self.__refresh()

		post("Checking eligibility...")
		post("Head Pointer: {}".format(self.headPointer))

		rfr()

		if self.headPointer == -1:
			post("The queue is empty.")
			msg.append("No item could be removed")
			rfr()

		else:
			# Handle key operation
			currentPointer = self.headPointer
			out = self.nodeArray[currentPointer].item
			self.nodeArray[currentPointer].item = ""
			post(out)

			# Correct flow
			# Data List
			self.headPointer = self.nodeArray[currentPointer].pointer

			# Free List
			if self.freePointer == -1:
				self.freePointer = currentPointer

			else:
				newPointer = self.freePointer
				endPointer = self.nodeArray[newPointer].pointer

				while endPointer != -1:
					newPointer = self.nodeArray[endPointer].pointer
					endPointer = self.nodeArray[newPointer].pointer
				self.nodeArray[newPointer].pointer = currentPointer

			self.nodeArray[currentPointer].pointer = -1

			if currentPointer == self.tailPointer:
				self.tailPointer = -1

			return msg
