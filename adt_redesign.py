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

class Prompts:
	def __init__(self, valueName, promptMsg, validatorFunc):
		self.valueName = valueName
		self.promptMsg = promptMsg
		self.validatorFunc = validatorFunc

class CallableActions:
	def __init__(self, name, functionToExecute):
		self.prompts = [] #Prompt objects
		self.functionToExecute = functionToExecute
		self.name = name #Eg: 'search'

	def addPrompt(self, newPrompt):
		self.prompts.append(newPrompt)

	# Add item to prompted for when action is called
	# valueName is the variable name that the function associated with the action anticipates 
	# the dictionary is ** operated to turn dictionary key into key arguments
	# thus valueName should match variable names anticipated by function to execute 
	
	def executeAssociatedFunction():
		pass

class linkNode:
	def __init__(self):
/		self.item = ""
		self.pointer = -1

class ADT:
	def post(self, content):
		self.log.append(content)

	def __doc__(self, *args):
		"""Takes a list, each entry each a seperate sentence for the ADT's docstring."""

		text = list(args)
		output = ""

		for i in range(len(text)):
			output += text[i] + "\n"

		return output

	def addToDisplayData(self, name, width, retrFunc):
		"""Extends the data the ADT provides for the ADT's representation in the UI
		Parameter: Name of the header, 
			Width to be allocated for the col corresponding to this attribute,
			Function which takes in index as parameter to give the value for each index
		"""

		self.dataItems.append(name)
		self.dataItemsWidth[name] = width
		self.dataItemsRetrievingFunc[name] = retrFunc

	def __init__(self, name, length, utilizesPointers):

		self.name = name
		self.numberOfNodes = int(length)

		self.refresh = (lambda: None)
		
		self.dataItems = []
		self.dataItemsWidth = {}
		self.dataItemsRetrievingFunc = {}

		## You may need to use/modify this in sub-classes
		self.addToDisplayData("Item", 20, self.getItem)

		self.usesPointers = utilizesPointers

		# The binary tree is the only exception
		self.hasTree = False

		if self.usesPointers: # Uses pointers?
			self.pointerNameToMethod = {}

			self.pointers = []

			self.addToDisplayData("Pointer", 10, self.getPointer)

		self.log = []

		Prompts("Enter item to be searched", lambda x: True, "itemToBeSearched")
		Prompts("Enter item to be inserted", self.isItemValid, "itemToBeInserted")

	def resetLog(self):
		self.log = []

	def getLog(self):
		return self.log

	def isItemValid(self, item):

		if len(item) > self.dataItemsWidth["Item"]:
			return "The item must be shorter than " + int(self.dataItemsWidth["item"]) + " letters."

		if not item.replace(" ", "").isalnum():
			return "Aside from spaces, the item must contain only alpha-numeric characters."

		else:
			return True

	def getInputPrompts(self):
		"""Returns data that allows the user interface to send data properly to functions that need arguments"""
		return self.prompts

	def __str__(self):
		return self.name

	def getSpecialPointersName(self):
		return self.pointers

	def getSpecialPointersValue(self, pointerName):
		if pointerName in self.pointers:
			return self.pointerNameToMethod[pointerName]()

	def getMethod(self, callName):
		"""Returns a dictionary with call name for keys, 
		the function associated for values.
		"""

		if callName in self.calls:
			return self.callsToFunc[callName]

	def getItem(self, index):
		return self.nodeArray[index].item

	def getPointer(self, index):
		return self.nodeArray[index].pointer
		
	def initialize(self, obj):
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
		"""Allows for searching the Tree for an item. Retrieves first instance encountered."""

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
