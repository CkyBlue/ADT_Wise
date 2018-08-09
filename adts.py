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
are meant to be string."""

## TODO - Get remove through the post treatment
## Add elaboration to __doc___

class node:
	def __init__(self):
		self.item = ""
		self.pointer = -1

class ADT:
	def post(self, content):
		self.log.append(content)

	def __doc__(self, *args):
		"""Takes a list, each entry each a seperate sentence for the ADT's docstring."""

		docArgs = list(args)

		text = docArgs
		output = ""

		for i in text:
			if i != (len(text) - 1) :
				output += i + "\n"
			else:
				output += i

		return output

	def __init__(self, name, length, pointers):

		self.name = name
		self.numberOfNodes = int(length)

		self.refresh = (lambda: None)
		
		self.dataItems = ["Item", "Pointer"]
		self.dataItemsWidth = {"Item": 20, "Pointer": 10}
		self.dataItemsRetrievingFunc = {"Item": self.getItem}

		if pointers: # Uses pointers?

			self.usesPointers = True

			self.pointerNameToProp = {}
			self.pointersName = []

			self.dataItemsRetrievingFunc["Pointer"] = self.getPointer
		

		self.log = []

		# Names used to invoke functions against corresponding methods

		self.calls = {"insert": self.insert, 
		"search": self.search,
		"remove": self.remove}

		# Input prompts for the functions that are associated with commands that can be invoked from the UI

		self.prompts = {}

		# The dictionary is inside an array so that if a single command need multiple values, the existing system permits
		# valueName must match the name of the parameter for the function

		self.prompts["insert"] = [{"promptMsg": "Enter item to be inserted", 
			"validator": self.isItemValid, 
			"valueName": "itemToBeInserted"}
		]

		self.prompts["search"] = [{"promptMsg": "Enter item to be searched", 
			"validator": lambda x: True, # No validation needed
			"valueName": "itemToBeSearched"}
		]

	def resetLog(self):
		self.log = []

	def getLog(self):
		return self.log

	def isItemValid(self, item):

		if len(item) > 20:
			return "The item must be shorter than 20 letters."

		if not item.replace(" ", "").isalnum():
			return "Aside from spaces, the item must contain only alpha-numeric characters."

		else:
			return True

	def getInputPrompts(self):
		"""Returns data that allows the user interface to send data properly to functions that need arguments"""
		-
		return self.prompts

	def __str__(self):
		return self.name

	def getSpecialPointersName(self):
		return self.pointers

	def getPointersValue(self, pointerName):
		return self.pointerNameToProp[pointerName]

	def getMethods(self):
		"""Returns a dictionary with call name for keys, 
		the function associated for values.
		"""
		return self.calls

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
		"""Allows for adding an item to the ADT."""

		# Short-hand
		rfr = self.refresh
		post = self.post

		msg = [] # Holds message that is displayed after the logs

		return msg

	def search(self, itemToBeSearched):
		"""Allows for searching the queue for an item. Retrieves first instance encountered."""

		msg = [] # Holds message that is displayed after the logs

		# Short-hand
		rfr = self.refresh
		post = self.post

		return msg

	def remove(self):
		"""Allows for removing a particular entry from the ADT."""

		msg = [] # Holds message that is displayed after the logs

		# Short-hand
		rfr = self.refresh
		post = self.post

		return msg
