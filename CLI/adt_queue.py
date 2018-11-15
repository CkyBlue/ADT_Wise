import adt

linkNode = adt.linkNode

class Queue(adt.ADT):

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