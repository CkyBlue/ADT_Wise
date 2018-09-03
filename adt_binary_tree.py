import adt

class binaryNode:
	def __init__(self):
		self.item = ""
		self.leftPointer = 0
		self.rightPointer = 0

class BinaryTree(adt.ADT):

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
