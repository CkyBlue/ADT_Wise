import os, copy
from cmd import Cmd
from colorama import init, Style, Fore, Back

init()

def clear():
	os.system('cls' if os.name == 'nt' else 'clear')

color_mapping = {-1: Back.BLACK,
	0: Back.BLUE + Fore.WHITE,
	1: Back.CYAN + Fore.WHITE,
	2: Back.GREEN + Fore.WHITE,
	3: Back.MAGENTA + Fore.WHITE,	
	4: Back.RED + Fore.WHITE,
	5: Back.WHITE + Fore.BLACK,
	6: Back.YELLOW + Fore.BLACK}

header = "Type 'load' to choose an ADT to interact with, else type 'exit' to quit."  
header += "\n"

adtNames = []
adtType = {}
objectStore = {}

# Turn on for debugging purposes
noPosting = False

### ADTS ###

class linkNode:
	def __init__(self):
		self.item = ""
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

		# Names used to invoke functions against corresponding methods
		## You may need to use/modify this in sub-classes
		self.calls = ["insert", "search", "remove"]

		self.callsToFunc = {"insert": self.insert, 
		"search": self.search,
		"remove": self.remove}

		# Input prompts for the functions that are associated with commands that can be invoked from the UI
		## You may need to use/modify this in sub-classes
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

class Queue(ADT):

	def __doc__(self):
		text = ["A queue is an abstract data type",
		"which works on the principle of Last in, first out.",
		"This particular implementation is of a circular queue",
		"\nThe nodes are initially set up into a free list.",
		"as new items are added, the nodes are made into a data list."
		]

		return super().__doc__(*text)

	def getFreePointer(self):
		return self.freePointer

	def getHeadPointer(self):
		return self.headPointer

	def getTailPointer(self):
		return self.tailPointer

	def __init__(self, name, length):
		super().__init__(name, length, True) # pointer = True

		# Queue's pointers

		self.freePointer = 0
		self.headPointer = -1
		self.tailPointer = -1

		# Queue's node array

		self.nodeArray = [linkNode() for i in range(self.numberOfNodes)]
		self.initialize(self.nodeArray)

		# Overwrite

		self.pointers = ["Free Pointer", "Head Pointer", "Tail Pointer", "Current Pointer"]
		self.pointerNameToMethod = {"Free Pointer": self.getFreePointer, 
			"Head Pointer": self.getHeadPointer, 
			"Tail Pointer": self.getTailPointer,
			"Current Pointer": self.getCurrentPointer
			}

		self.currentPointer = -1

	def getCurrentPointer(self):
		return self.currentPointer

	def insert(self, itemToBeInserted):
		"""Allows for adding an item to the tail of the queue if it is not full."""

		newItem = itemToBeInserted

		msg = []

		# Short-hand
		post = self.post
		rfr = self.refresh

		post("Checking if operation can be performed...")
		post("Operation possible  if free pointer does not point to null.")
		post("Free Pointer: {}".format(self.freePointer))

		rfr()

		# Check eligibility
		if self.freePointer == -1:
			post("Pointer to free node is null.")
			post("Error, there is no empty node.")
			rfr()
			msg.append("Item could not be inserted.")

		else:
		# Handle key operation
			post("We need a free node to work with.")
			post("The head of the free list,")
			post("given by the free pointer will do.")
			rfr()
			post("Moving to free node...")
			post("Current pointer changes to {}.".format(self.freePointer))
			rfr()
			self.currentPointer = self.freePointer
			post("Setting item at free node to {}".format(newItem))
			rfr()		
			self.nodeArray[self.currentPointer].item = newItem 

		# Correct Flow
			post("Correcting links...")
			# Free list
			pointerTo = self.nodeArray[self.currentPointer].pointer
			post("The index value {} that the current node points to will be overwritten,".format(pointerTo))
			post("because it will be used to to incorporate the current node into the data list.")
			post("\nBefore this overwriting occurs, any action that makes use of this pointer needs to be completed.")
			rfr()
			post("With this rationalization,")
			post("correction will use that address first.")
			rfr()
			post("The current node is linked into the free list,")
			post("which is setup such that the free pointer points to")
			post("the head of the free list (which has now used by us to store the new item),")
			post("which points to another free node which points to another free node and so on.")
			rfr()
			post("The index it points to thus can be used as the next free node.")
			post("New free pointer: {}".format(pointerTo))
			rfr()			
			self.freePointer = pointerTo 

			# Data list			
			if self.tailPointer != -1:
				post("As for the data list,")
				post("The previous tail at index {} is set to point to the current tail at {}.".format(self.tailPointer,
					self.currentPointer))
				rfr()
				self.nodeArray[self.tailPointer].pointer = self.currentPointer	
				post("This is done because that information will be needed when popping heads.")
				post("When a head node is popped, a new head node is required.")
				post("By setting up each node to point to the one which came after it,")
				post("we have a means of fetching the next logical head.")
				rfr()
						
			post("Since current node is now the new tail, it does not need to point to anything.")
			post("Thus, the current node should point to: {}".format(-1))		
			rfr()
			self.nodeArray[self.currentPointer].pointer = -1
			post("Setting the tail pointer as: {}".format(self.currentPointer))
			rfr()
			self.tailPointer = self.currentPointer

			if self.headPointer == -1:
				post("Since the current node is the new head, the head pointer is also modified...")
				post("Head pointer is set to: {}".format(self.currentPointer))
				rfr()
				self.headPointer = self.currentPointer

			post("All done.")
			rfr()

			msg.append("Item successfully inserted.")

			return msg

	def search(self, itemToBeSearched):
		"""Allows for searching the queue for an item. Retrieves first instance encountered."""

		msg = [] # Holds message that is displayed after the logs

		# Short-hand
		post = self.post
		rfr = self.refresh

		post("We want to search through the data list.")
		post("We begin from the head pointer.")
		rfr()
		post("Moving to the head-pointer...")
		post("Current Pointer becomes: {}".format(self.headPointer))
		rfr()
		self.currentPointer = self.headPointer
		itemFound = False

		if self.currentPointer == -1: # If list is empty
			post("Since current pointer points to null,")
			post("we know that there was no head node present.")
			post("This indicates that the queue is empty.")
			rfr()
			msg.append("Item could not be located.")
		
		else:
			post("Searching thrrough the items,")
			post("until item is found,")
			post("or the  end is reached.")

			rfr()

			while self.currentPointer != -1 and not itemFound:
				post("Item at current position: {}".format(self.nodeArray[self.currentPointer].item))
				post("Item being searched: {}\n".format(itemToBeSearched))

				if self.nodeArray[self.currentPointer].item == itemToBeSearched:
					post("The two are the same,")
					post("The item at {} matched.".format(self.currentPointer))

					msg.append("The item {} was found at index {}.".format(itemToBeSearched, self.currentPointer))
					itemFound = True

				else:
					post("The two do not match.")
					rfr()
					post("We move to the next node in the data list.")
					post("Current node points to: {}\n".format(self.nodeArray[self.currentPointer].pointer))
					rfr()
					post("Moving to next node,")
					post("Current Pointer becomes: {}".format(self.nodeArray[self.currentPointer].pointer))
					rfr()
					self.currentPointer = self.nodeArray[self.currentPointer].pointer

					if self.currentPointer == -1:

						post("Current Pointer reached: {}".format(-1))
						post("Since no item exists at an index of -1,")
						post("we know we have reached the end of the data list.")
						rfr()
						post("Breaking out of loop...")
						rfr()			

			if not itemFound:
				post("Finished checking all occupied nodes,")
				post("No match was found.")
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
		rfr = self.refresh

		post("Checking if operation can be performed...")
		post("Operation possible if list is not empty,")
		post("i.e, it has a head,")
		rfr()
		post("Head Pointer: {}".format(self.headPointer))
		rfr()
		if self.headPointer == -1:
			post("Since the head pointer points to null,")
			post("we know that the data list is empty.")

			msg.append("No item could be removed.")
		else:
			# Handle key operation

			post("We begin checking for matches from the head node.")
			post("Moving to head pointer...")
			post("Current Pointer becomes: {}".format(self.headPointer))
			rfr()
			self.currentPointer = self.headPointer

			out = self.nodeArray[self.currentPointer].item
			post("Retrieving item from the index pointed to by current pointer...")
			post("Temporarily stored '{}'".format(out))
			rfr()
			msg.append("Item was successfully removed.")
			msg.append("Output is '{}'.".format(out))

			post("Clearing item from the index pointed to by current pointer...")
			rfr()
			self.nodeArray[self.currentPointer].item = ""
			
			# Correct flow
				# Data List
			post("Correcting links...")

			post("The current node is to be linked to the free list,")
			post("However, the pointer stored by the node will be overwritten")
			post("when linked to the free list.\n")
			post("Correction thus makes use of this pointer value first,")
			rfr()
			post("Current node points to {}".format(self.nodeArray[self.currentPointer].pointer))
			post("This value gives the next head pointer,")
			post("Setting head pointer to point to {}.".format(self.nodeArray[self.currentPointer].pointer))
			rfr()
			self.headPointer = self.nodeArray[self.currentPointer].pointer

			post("Now, adding the released node to the end of the free list...")
			post("Current node is made to point to the head of the free node,")
			post("given by the free pointer.")
			post("Free Pointer: {}".format(self.freePointer))
			rfr()
			self.nodeArray[self.currentPointer].pointer = self.freePointer
			post("The released node now becomes the new head of the free list.")
			rfr()
			self.freePointer = self.currentPointer

			post("Checking if tail pointer needs to be modified...")
			post("It needs to be modified if the removed node happened to be the tail,")
			post("Released node: {} and tail node: {}".format(self.currentPointer, self.tailPointer))
			rfr()
			if self.currentPointer == self.tailPointer:
				post("It's a match,")
				post("meaning that the tail node was removed.")
				post("Tail pointer is changed to -1.")
				rfr()
				self.tailPointer = -1
			else:
				post("They do not match,")
				post("No change is made to tail pointer,")

		rfr()
		return msg

class binaryNode:
	def __init__(self):
		self.item = ""
		self.leftPointer = 0
		self.rightPointer = 0

class BinaryTree(ADT):

	def __doc__(self):
		text = ["A binary tree is an abstract data type",
		"where each node can have two children",
		"This particular implementation is ordered",
		"with the smallest entry in the left most node",
		"and the largest in the right most node."
		"",
		"The nodes are linked into a free list through their",
		"left pointers.",
		"Instead of node deletion, this ADT currently only supports",
		"resetting."
		]

		return super().__doc__(*text)

	def getRootPointer(self):
		return self.rootPointer

	def getFreePointer(self):
		return self.freePointer

	def __init__(self, name, length):
		super().__init__(name, length, True) # pointer = True

		# Tree's pointers

		self.freePointer = 0
		self.rootPointer = -1
		self.currentPointer = -1

		# Overwrite
		self.dataItems = []
		self.dataItemsWidth = {}
		self.dataItemsRetrievingFunc = {}
		self.hasTree = True

		self.addToDisplayData("Left Pointer", 15, self.getLeftPointer)
		self.addToDisplayData("Item", 12, self.getItem)
		self.addToDisplayData("Right Pointer", 15, self.getRightPointer)

		# Tree's node array

		self.nodeArray = [binaryNode() for i in range(self.numberOfNodes)]
		self.initialize(self.nodeArray)

		# Overwrite

		self.pointers = ["Free Pointer", "Root Pointer", "Current Pointer"]
		self.pointerNameToMethod = {"Free Pointer": self.getFreePointer, 
			"Root Pointer": self.getRootPointer,
			"Current Pointer": self.getCurrentPointer}

		self.calls = ["insert", "traverse", "reset"]

		self.callsToFunc = {"insert": self.insert, 
		"traverse": self.traverse,
		"reset": self.reset}

		# Transient pointers

		self.prevPointer = -1

	def reset(self):
		"""Clears all of the data."""

		self.post("Resetting the tree...")
		self.refresh()
		self.initialize(self.nodeArray)
		self.post("All done.")
		self.refresh()
		return ["Tree reset."]

	def initialize(self, nodeArray):

		# Setting up free list for a binary tree
		for index in range(self.numberOfNodes):

			nodeArray[index].leftPointer = index + 1
			nodeArray[index].rightPointer = -1
			nodeArray[index].item = ""

		# Tail node doesn't point to anything.
		nodeArray[self.numberOfNodes - 1].leftPointer = -1

	def getPrevPointer(self):
		return self.prevPointer

	def getCurrentPointer(self):
		return self.currentPointer

	def getLeftPointer(self, index):
		return self.nodeArray[index].leftPointer

	def getRightPointer(self, index):
		return self.nodeArray[index].rightPointer

	def insert(self, itemToBeInserted):
		"""Allows for adding an item to the tree if it is not full."""

		msg = []

		# Short-hand
		post = self.post
		rfr = self.refresh

		post("Checking if tree has an empty node,")
		post("Free pointer: {}".format(self.freePointer))
		rfr()

		if self.freePointer == -1: # Checking eligibility
			
			post("Since free pointer points to null,")
			post("We understand that the tree is full.")
			
			post("\n Thus, the operation cannot be performed.")
			msg.append("The item could not be inserted.")

		else:
			post("Since free pointer does not point to null,")
			post("We understand that the tree has an empty node.")
			rfr()

			post("Moving to the first free node in the free list...")
			post("Current pointer is changed to: {}".format(self.freePointer))
			rfr()

			self.currentPointer = self.freePointer
			post("Since this node is no longer going to be free,")
			post("we need a new node to serve as the free node.")
			rfr()

			post("The nodes in the free list are linked,")
			post("so we can fetch the next free node in the list from the current node,")
			post("Note that this implementation links nodes by default into the free list")
			post("using the left pointers.")
			rfr()

			post("Current node's left pointer points to {}".format(self.nodeArray[self.currentPointer].leftPointer))
			rfr()

			if self.nodeArray[self.currentPointer].leftPointer == -1:
				post("Note that this being null is not of consequence,")
				post("It just means that instead of pointing to the next free node,")
				post("The free pointer will be set to point to null.")
				rfr()

			post("Setting the free pointer as this value,")
			rfr()
			self.freePointer = self.nodeArray[self.currentPointer].leftPointer

			post("Now, working with the data list")
			post("Inserting item at current node,")
			rfr()
			self.nodeArray[self.currentPointer].item = itemToBeInserted

			post("Since this new node is a leaf node,")
			post("It does not point to anything.")
			rfr()
			self.nodeArray[self.currentPointer].leftPointer = -1
			self.nodeArray[self.currentPointer].rightPointer = -1

			post("Now, finding node to which we will attach the current node")
			post("This will be done such that if a node has a node to its left")
			post("the content in the node to the left will be alphabetically smaller,")
			post("\nif there is a node to the right,")
			post("the content in the node to the right will be alphabetically larger,")
			rfr()
			post("We start evaluating from the root,")
			post("Root pointer: {}".format(self.rootPointer))
			post("This becomes out current node,")
			post("Current pointer changes to {}.".format(self.rootPointer))
			rfr()
			nodeOfInsertion = self.currentPointer
			self.currentPointer = self.rootPointer

			post("We want to keep traversing down the tree until we hit a node,")
			post("which does not have a leaf node in the drection we need to traverse,")
			post("This means we stop when the next node to go to becomes null or has index -1.")
			rfr()

			if self.currentPointer != -1:
				post("Everytime we fetch a new node index to traverse to,")
				post("We need to remember which node we came from,")
				post("Let's define it as the previous pointer.")
				rfr()

				self.pointers += ["Previous Pointer"]
				self.pointerNameToMethod["Previous Pointer"] = self.getPrevPointer

			while self.currentPointer != -1:
				post("Currently we are looking at node at {}".format(self.currentPointer))
				post("We will be moving from this so,")
				self.prevPointer = self.currentPointer
				post("Previous pointer: {}".format(self.prevPointer))
				rfr()
				post("Now, we need to decide which direction we traverse in,")
				post("Let's check if the item at the current node")
				post("is larger or smaller than the item we are going to insert.")
				post("Is {} > {}?".format(self.nodeArray[self.currentPointer].item, itemToBeInserted))
				rfr()

				if self.nodeArray[self.currentPointer].item > itemToBeInserted:
					post("Yes apparently,")
					post("so we traverse left")
					rfr()
					turnedLeft = True
					self.currentPointer = self.nodeArray[self.currentPointer].leftPointer

				else:
					post("No apparently,")
					post("so we traverse right")
					rfr()
					turnedLeft = False
					self.currentPointer = self.nodeArray[self.currentPointer].rightPointer

				post("Current pointer: {}".format(self.currentPointer))
				rfr()	
				
			if self.currentPointer == self.rootPointer:
				post("Looks like we didn't have a root node yet,")
				post("so no traversing it seems.")
				rfr()
				post("Setting our node, the one we had taken from the free list,")
				post("as the root node.")
				rfr()
				self.rootPointer = nodeOfInsertion
			else:
				post("We've finally hit a end.")
				post("The previous node was {} ".format(self.prevPointer))

				if turnedLeft:
					post("We had turned left from the previous node,")
					post("So we attach the new node to the left of the previous node,\n")
					post("Thus, the left pointer of the node at {} is changed to {}.".format(self.prevPointer, nodeOfInsertion))
					rfr()
					self.nodeArray[self.prevPointer].leftPointer = nodeOfInsertion
				else:
					post("We had turned right from the previous node,")
					post("So we attach the new node to the right of the previous node,\n")
					post("Thus, the right pointer of the node at {} is changed to {}.".format(self.prevPointer, nodeOfInsertion))
					rfr()
					self.nodeArray[self.prevPointer].rightPointer = nodeOfInsertion

				self.pointers.remove("Previous Pointer")
				del self.pointerNameToMethod["Previous Pointer"]

			msg.append("Item added successfully.")

		post("All done.")
		rfr()
		return msg	

	def traverseNode(self, root):
		# Short-hand
		post = self.post
		rfr = self.refresh

		post("Current Pointer becomes: {}".format(root))
		rfr()
		self.currentPointer = root

		post("Lets see if there is a node to the left of this node.")
		post("The left pointer to current node is: {}".format(self.nodeArray[root].leftPointer))
		rfr()

		if self.nodeArray[root].leftPointer != -1:
			post("Since this is not null, we traverse left.")
			self.traverseNode(self.nodeArray[root].leftPointer)
			post("We go back to the parent node of the current node.")
			post("Current Pointer should again become: {}".format(root))
			rfr()
			self.currentPointer = root
			post("All nodes left to this node have been handled,")
			post("so we now deal with the item at the current node.")

		else:
			post("Since this is null, we know that there are no nodes.")
			post("to the left of this node.")
			post("So we now deal with the item at the current node.")

		rfr()
		post("Item at current node is: {}".format(self.nodeArray[root].item))
		post("We append this to the output.")
		rfr()

		self.accumulator.append(self.nodeArray[root].item)

		post("Now lets see if there is a node to the right of this node.")
		post("The right pointer to current node is: {}".format(self.nodeArray[root].rightPointer))
		rfr()

		if self.nodeArray[root].rightPointer != -1:
			post("Since this is not null, we traverse right.")
			rfr()

			self.traverseNode(self.nodeArray[root].rightPointer)
			post("We go back to the parent node of the current node.")
			post("Current Pointer should again become: {}".format(root))
			rfr()
			self.currentPointer = root
		else:
			post("Since this is null, we know that there are no nodes.")
			post("to the right of this node.")
			rfr()

		post("We're all done with the node at {} and its descendants so we leave.".format(root))
		rfr()

	def traverse(self):
		"""Traverses the tree to print items going from the left most node to the right most.."""

		msg = []

		# Short-hand
		post = self.post
		rfr = self.refresh

		self.accumulator = []

		post("We start down the tree from the root node,")
		post("Root node: {}".format(self.rootPointer))

		if self.rootPointer != -1:
			padding = 4

			demarc = padding*" " + (self.dataItemsWidth["Item"] + 2)*"-"
			template = padding*" " + "|{:^" + str(self.dataItemsWidth["Item"]) + "}|"

			self.traverseNode(self.rootPointer) # Start from the node
			
			msg.append("Tree successfully traversed.\n")

			# Format output
			msg.append(demarc + "\n" + template.format("Output") + "\n" + demarc)
			for item in self.accumulator:
				msg.append(template.format(item))
			msg.append(demarc)

		else:
			post("The root pointer pointed to null,")
			post("indicating that the tree is empty.")
			rfr()
			msg.append("The tree was empty. No output.")
		
		return msg

###

# Link call name to ADT class here
ADTS = {"queue": Queue, "binary-tree": BinaryTree}

def getADTClassFromCallName(adtCallName):
	if adtCallName in getAvailableADTCallNames():
		return ADTS[adtCallName]

	else:
		return None

def getAvailableADTCallNames():
	return ADTS.keys()

def parse(log):
	"""Takes a log list and gives a string where the items are indivisual statements,
	
	Consider developing to recognize markup
	"""
	content = ""

	for statement in log:
		content += statement + "\n"

	return content

class ADTObjectHandler:
	def __init__(self, object):
		"""Uses an ADT object which is input as parameter to build an embeded interface."""

		self.skipThroughPostings = noPosting

		# ADT object
		self.object = object

		# Title text for the embedded prompt
		self.title = "\nType in a command, 'help' or 'exit'.\n"

		self.availableMethods = self.object.calls # List

		# Dictionary of prompts for a command {<cmd-name>: []}
		self.promptsInfo = self.object.getInputPrompts()

		# Whether or not pointers need to be parsed
		self.usesPointers = self.object.usesPointers

		self.keyForPrompt = ":>>"

		# Set refresher function
		self.object.refresh = self.refresherPrompt

	def treeGraphic(self, obj, index):
		## To vary padding
		padding = 4

		widthOfItem = obj.dataItemsWidth["Item"]

		nodeFormat = "{index:^2}: |{left:^4}|{item:^" + str(widthOfItem) + "}|{right:^4}|"
		indexIndent = 4

		demarcUnit = "-"

		# Overlining demarcation
		demarcLength = 4 + widthOfItem + 4 + 4

		# and space for index preceder
		blockLength = demarcLength + indexIndent
		overline = " " * indexIndent + demarcUnit * demarcLength

		pad = " " * padding

		blankNode = nodeFormat.format(index = -1, left = "-", right = "-", item = "-")
		##
		currentNode = index

		if currentNode != -1:
			leftNode = obj.nodeArray[index].leftPointer
			rightNode = obj.nodeArray[index].rightPointer	
			root = nodeFormat.format(index = index,
				left = leftNode,
				right = rightNode,
				item = obj.nodeArray[index].item)
		else:
			leftNode = -1
			rightNode = -1		
			root = blankNode		

		if leftNode != -1:
			left = nodeFormat.format(index = leftNode,
				left = obj.nodeArray[leftNode].leftPointer,
				right = obj.nodeArray[leftNode].rightPointer,
				item = obj.nodeArray[leftNode].item)
		else:
			left = blankNode

		if rightNode != -1:
			right = nodeFormat.format(index = rightNode,
				left = obj.nodeArray[rightNode].leftPointer,
				right = obj.nodeArray[rightNode].rightPointer,
				item = obj.nodeArray[rightNode].item)
		else:
			right = blankNode

		output = ""
		output += pad + "{:^70}".format("Current node:") + "\n"
		output += pad + "{:^70}".format(overline + " "*3) + "\n"
		output += pad + "{:^70}".format(root + " "*3) + "\n"
		output += pad + "{:^70}".format(overline + " "*3) + "\n"	
		output += pad + "{:^70}".format("|") + "\n"
		output += pad + "{:^70}".format("-"*34) + "\n"
		output += pad + "{:<35}{:>35}".format(" "*17 + "|", "|" + " "*17) + "\n"
		output += pad + "{:<35}{:>35}".format(overline, overline + " "*3) + "\n"	
		output += pad + "{:<35}{:>35}".format(left, right + " "*3) + "\n"
		output += pad + "{:<35}{:>35}".format(overline, overline + " "*3) + "\n"

		return output

	def internalLoop(self):
		while True:
			self.object.resetLog()

			clear()
			# Embedded prompt is displayed
			print(self.title)
			self.embeddedPrompt()

			userInput = input("{} ".format(self.keyForPrompt))

			# " CMD  now" -> "cmd"
			cmd = userInput.lower().split()
			if len(cmd) > 0:
				cmd = cmd[0] 
			else:
				cmd = ""

			# Evaluate input
			if cmd in self.availableMethods:
				funcToRun = self.object.getMethod(cmd)

				if funcToRun == None:
					print("Call registered without designated function.")
					continue

				# Checks the prompts info dictionary for a key with name matching the cmd.
				prompts = self.promptsInfo.get(cmd, None)

				# If no values need to be prompted for a function
				if prompts == None:

					# GUI needs another thread to run this
					response = funcToRun()
					
					if response:
							clear()
							print(parse(response))

							input("Press enter to continue... ")
							clear()

				else: # If values need to prompted for

					kwargs = {} # Holds parameters that are to be passed into function that is to be fired.
					# kwargs is unpackaged into the function

					limitExceeded = False
					
					for prompt in prompts: # Uses prompt parameters to fetch values
						keyName = prompt["valueName"]

						count = 0

						while True: 
							val = input("{} :> ".format( (prompt["promptMsg"]) ) )

							valid = prompt["validator"](val)

							if valid == True: # If validator return True
								kwargs[keyName] = val
								break

							else: # Validator returns error message

								errorMessage = valid
								print("\n"+errorMessage)
								
								count += 1

								if count >= 3:
									print("You have responded incorrectly 3 times. Exiting prompt...")
									input("\nPress enter to continue... ")
									limitExceeded = True
									break

						if limitExceeded:
							break

					if not limitExceeded: # If evrything is valid
						response = funcToRun(**kwargs)

						clear()

						if response:
							print(parse(response))

						input("\nPress enter to continue... ")
						clear()

			elif cmd == "help":
				clear()
				print("Help:\n")
				print(self.object.__doc__())
				print("For current purposes, the available commands are:\n")

				for callName in self.availableMethods:

					# Casing the print right
					thisCommand = callName.title()
			
					# Reading command info from docstring
					info = self.object.getMethod(callName).__doc__ or '' 

					print(thisCommand + "\n\t" + info)

				toggleInfo = "Allows toggling the logs on or off."  
				print("Toggle" + "\n\t" + toggleInfo)

				input("\nPress enter to continue...")

			elif cmd == "exit":
				print("Exiting ADT interface.")

				input("Press enter to continue...")
				clear()
				break

			elif cmd == "toggle":
				self.skipThroughPostings = not self.skipThroughPostings

				translation = {True: "off", False: "on"} # Maps true->off, false->on
				print("Toggled postings to {}.".format(translation[self.skipThroughPostings])) # on/off

				input("\nPress enter to continue...")

			else:
				print("The command '{}' is not valid.".format(cmd))
				print("Check spelling, type 'help' for instructions.")

				input("\nPress enter to continue...")
	
	def embeddedPrompt(self):
		"""The internal prompt which is used when handling an object which can be invoked from with adt 
		Parameters: Text to be displayed as title, The object to be used for display"""

		self.displayValuesWithinADT()

		if self.usesPointers:
			print()
			self.displayPointersWithinADT()

		print()

	def displayValuesWithinADT(self):
		# Returns a list [ {<heading>: {<attr>: <val>, } }, ]
		obj = self.object

		numberOfHeadings = len(obj.dataItems)

		padding = " "*4
		widthForIndex = 15

		# Initially,
		placeholderTemplate = padding + "|"
		demarcLength = 1
		parametersForHeader = {}

		parametersForHeader = {"Index": "Index of Node"} # Header for index, index is imposed by the function
		placeholderTemplate += "{Index:^" + str(widthForIndex) + "}|"

		demarcLength += (widthForIndex + 1)

		for heading in obj.dataItems: 
			# Accumulates headings into template for placeholder
			# and sets up variables used for controlling output

			keyName = heading
			width = obj.dataItemsWidth[heading]

			placeholderTemplate += "{" + keyName + ":^" + str(width) + "}|"
			demarcLength += (width + 1)

			parametersForHeader[keyName] = keyName.title()

		demarc = padding + "-" * demarcLength

		print(demarc + "\n" + placeholderTemplate.format(**parametersForHeader) + "\n" + demarc)

		for nodeIndex in range(obj.numberOfNodes):	

			parametersForRows = {}

			# Builds a dictionary for formatting
			for heading in obj.dataItems:

				# Returns function which processes value fetching for a certain node index
				retrfunc = obj.dataItemsRetrievingFunc[heading]

				if "pointer" in heading.lower(): # Color Formatting
					n = retrfunc(nodeIndex)
					width = obj.dataItemsWidth[heading]
					parametersForRows[heading] =  color_mapping[n]
					parametersForRows[heading] += ("{:^" + str(width) + "}").format(str(n)) + Style.RESET_ALL

				else:
					parametersForRows[heading] = retrfunc(nodeIndex)

				i = nodeIndex
				parametersForRows["Index"] = color_mapping[i]
				parametersForRows["Index"] += ("{:^" + str(widthForIndex) + "}").format(str(i)) + Style.RESET_ALL

			print(placeholderTemplate.format(**parametersForRows))

		print(demarc)
					
	def displayPointersWithinADT(self):
		pointers = self.object.getSpecialPointersName() # List

		numberOfPointers = len(pointers)

		padding = "    "
		widthForValues = 10

		# Initially,
		placeholderTemplate = padding + "|"
		demarcLength = 1

		extraSpace = 2

		# Makes a list out of length of pointer names and get's longest
		maxLengthOfPointerName = max([len(pointer) for pointer in pointers]) + extraSpace

		# Demarcation length
		demarcLength += (widthForValues + 1)
		demarcLength += (maxLengthOfPointerName + 1)

		placeholderTemplate += "{PointerName:^" + str(maxLengthOfPointerName) + "}|"
		placeholderTemplate += "{Value:^" + str(widthForValues) + "}|"

		demarc = padding + "-" * demarcLength

		# Header
		print(demarc + "\n" + placeholderTemplate.format(PointerName="", Value="Values") + "\n" + demarc)

		# Body
		for pointer in pointers: 
			# Grabs the pointer name for the entry
			pointerName = pointer

			rawVal = self.object.getSpecialPointersValue(pointer)

			r = rawVal
			pointerValue = color_mapping[r]
			pointerValue += ("{:^" + str(widthForValues) + "}").format(str(r)) + Style.RESET_ALL

			parametersForRows = {"PointerName": pointerName, "Value": pointerValue}
			print(placeholderTemplate.format(**parametersForRows))
		
		print(demarc)

	def refresherPrompt(self):
		if self.skipThroughPostings: # If post should be short-circuited
			return None

		clear()

		self.embeddedPrompt()

		if self.object.hasTree: # If a tree graphic is required
			tree = self.treeGraphic(self.object, self.object.currentPointer)
			print(tree)

		logString = parse(self.object.log)
		print(logString)

		self.object.resetLog()
		input("Press enter to continue... ")
		for i in range(100):
			pass

class adt_wise_ui(Cmd):
	# initialization

	maxNumOfPrompts = 3

	availableADTTypes = getAvailableADTCallNames()

	nodeCount = 7

	maxPermissibleLengthOfName = 15
		
	def validTypeOfADT(self, typeOfADT):
		"""If valid returns True, else returns an error message """

		if typeOfADT.lower().strip() in self.availableADTTypes:
			return True
		else:
			return "{} is not a supported type of ADT. Choose one from the available types.".format(typeOfADT)

	def do_help(self, args):
		print("For current purposes, the available commands are:\n")

		availableCommands = ["load", "exit"]
		ascMethods = {"load": self.do_load, "exit": self.do_exit}

		for cmd in availableCommands:
			# Casing the print right
			thisCommand = cmd.title()
	
			# Reading command info from docstring
			info = ascMethods[cmd].__doc__ or ''

			print(thisCommand + "\n\t" + info)
	def validADTName(self, name):
		"""If valid returns True, else returns an error message """
		
		if name in self.existingObjects:
			return("An ADT with ths name already exists. Try another name.")

		elif len(name) > self.maxPermissibleLengthOfName:
			return("The name should be shorter than {} letters.".format(self.maxPermissibleLengthOfName))

		elif not name.isalnum():
			return("The name must only contain alpha-numeric characters. Spaces are not allowed.")

		else:
			return True

	def validNodeCount(self, nodeCount):
		"""If valid returns True, else returns an error message """

		if nodeCount.isdigit():
			nodeCount = int(nodeCount)
			if nodeCount >= self.minNumOfNodes and nodeCount <= self.maxNumOfNodes:
				return True
		return ("Please provide a integer between {min} and {max}.".format(min = self.minNumOfNodes,
			max = self.maxNumOfNodes))

	def do_load(self, args):
		"""Loads a particular type of ADT for interacting with."""

		limitExceeded = False
		invalidEntry = False

		# Process argument to split on ',' and strip elements of trailing/leading spaces

		arguments = args.split(",")
		arguments = list(map(lambda x: x.strip(), arguments))

		if arguments == ['']: # If no arguments received

			# Prompts for ADT Type
			for i in range(self.maxNumOfPrompts):
				print("The following types of ADT are available:\n")

				self.displayAvailableADTs()

				# typeOfADT
				typeOfADT = input("\nWhat type of ADT do you want to load? ")

				# Validation
				valid =  self.validTypeOfADT(typeOfADT)

				if valid == True:
					break
				else:
					errorMsg = valid
					print(errorMsg)
			else:
				limitExceeded = True

			if limitExceeded:
				print("You have responded incorrectly 3 times. Exiting prompt...")
				invalidEntry = True

		elif len(arguments) == 1: # If 1 arguments received

			typeOfADT = arguments[0]

			valid =  self.validTypeOfADT(typeOfADT)

			if valid != True:
				errorMsg = valid
				print(errorMsg)	
				invalidEntry = True

		else:
			invalidEntry = True
	
		# Build ADT or give error message
		if not invalidEntry:
			# ADT Call names are stored in lower-case
			typeOfADT = typeOfADT.lower().strip()

			# Create and Load 
			adtClass = getADTClassFromCallName(typeOfADT)
			objToUse = adtClass("Micro", self.nodeCount)
			ADTObjectHandler(objToUse).internalLoop()

			# Redisplay header after finished working with the object
			print(header)

		elif len(arguments) not in [0, 1]:
			print("Either provide no arguments or 1 valid one. You provided {}.".format(len(arguments)))

	def do_exit(self, args):
		"""Exits the program."""
		print("Exiting.")
		raise SystemExit

	def displayAvailableADTs(self):
		
		numberOfHeadings = 2
		padding = " "*4

		widthForCol = 20
		widthForIndex = 5
		keyName = "ADTs"

		# A template is made

		placeholderTemplate = padding + "|"
		demarcLength = 1

		# Values to be fed for header

		# Index
		parametersForHeader = {}
		parametersForHeader = {"Index": ""} # Header for index

		placeholderTemplate += "{Index:^" + str(widthForIndex) + "}|"

		demarcLength += (widthForIndex + 1)

		# ADTs
		placeholderTemplate += "{" + keyName + ":^" + str(widthForCol) + "}|"

		demarcLength += (widthForCol + 1)

		parametersForHeader[keyName] = keyName

		# Demarcation
		demarc = padding + "-" * demarcLength

		# Print header
		print(demarc + "\n" + placeholderTemplate.format(**parametersForHeader) + "\n" + demarc)

		ADTNames = list(ADTS.keys())

		# Dump ADT names into template and print
		for i in range(len(ADTNames)):

			parametersForRows = {}
			# Builds a dictionary for formatting

			parametersForRows[keyName] = ADTNames[i].title()
			parametersForRows["Index"] = ("{:^" + str(widthForIndex) + "}").format(str(i + 1))

			print(placeholderTemplate.format(**parametersForRows))

		print(demarc)

def start():
	promptLoop = adt_wise_ui()
	promptLoop.prompt = ":>> "

	promptLoop.cmdloop("...Starting\n" + header)

if __name__ == "__main__":
	start()


