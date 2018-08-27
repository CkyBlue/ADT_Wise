import adt

class Queue(adt.ADT):

	def __doc__(self):
		text = ["A queue is an abstract data type",
		"which works on the principle of Last in, first out.",
		"",
		"Add more elaboration later..."
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

		self.nodeArray = [adt.linkNode() for i in range(self.numberOfNodes)]
		self.initialize(self.nodeArray)

		# Overwrite

		self.pointers = ["Free Pointer", "Head Pointer", "Tail Pointer"]
		self.pointerNameToMethod = {"Free Pointer": self.getFreePointer, 
			"Head Pointer": self.getHeadPointer, 
			"Tail Pointer": self.getTailPointer}

	def insert(self, itemToBeInserted):
		"""Allows for adding an item to the tail of the queue if it is not full."""

		newItem = itemToBeInserted

		msg = []

		# Short-hand
		post = self.post
		rfr = self.refresh

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

			# Free list

			pointerTo = self.nodeArray[currentPointer].pointer
			post("Since the index value {} that the current node points to is to be overwritten,".format(pointerTo))
			post("Correction uses that address first.\n")
			post("Since current node is linked into the free list,")
			post("the index it points to can be used as the next free pointer.")
			post("New free pointer: {}".format(pointerTo))
			rfr()			
			self.freePointer = pointerTo 

			# Data list			
			if self.tailPointer != -1:
				post("As for the data list,")
				post("The previous tail at index {} is set to point to the current tail at {},".format(self.tailPointer,
					currentPointer))
				post("so that the new tail can be fetched for the head pointer,")
				post("when the old tail is popped out.")
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
		"""Allows for searching the queue for an item. Retrieves first instance encountered."""

		msg = [] # Holds message that is displayed after the logs

		# Short-hand
		post = self.post
		rfr = self.refresh

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
			post("Searching thrrough the items,")
			post("until item is found,")
			post("or the  end is reached.")

			rfr()

			while currentPointer != -1 and not itemFound:
				post("Item at current position: {}".format(self.nodeArray[currentPointer].item))
				post("Item being searched: {}\n".format(itemToBeSearched))

				if self.nodeArray[currentPointer].item == itemToBeSearched:
					post("The two are the same,")
					post("The item at {} matched.".format(currentPointer))

					msg.append("The item {} was found at index {}.".format(itemToBeSearched, currentPointer))
					itemFound = True

				else:
					post("The two do not match,")
					post("Current node points to: {}\n".format(self.nodeArray[currentPointer].pointer))

					post("Moving to next node,")
					post("Current Pointer: {}".format(self.nodeArray[currentPointer].pointer))
					
					currentPointer = self.nodeArray[currentPointer].pointer

					if currentPointer == -1:
						rfr()

						post("Current Pointer reached: {}".format(currentPointer))
						post("Since no item exists at a index of -1,")
						post("Breaking out of loop...")
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
		rfr = self.refresh

		post("Checking eligibility...")
		post("Head Pointer: {}".format(self.headPointer))

		rfr()

		if self.headPointer == -1:
			post("The queue is empty.")
			msg.append("No item could be removed.")
		else:
			# Handle key operation

			post("Moving to head pointer...")
			post("Current Pointer: {}".format(self.headPointer))
			rfr()
			currentPointer = self.headPointer

			out = self.nodeArray[currentPointer].item
			post("Retrieving item from the index pointed to by current pointer...")
			post("Temporarily stored '{}'".format(out))
			rfr()
			msg.append("Item was successfully removed.")
			msg.append("Output is '{}'.".format(out))

			post("Clearing item from the index pointed to by current pointer...")
			rfr()
			self.nodeArray[currentPointer].item = ""
			
			# Correct flow
				# Data List
			post("Correcting links...")

			post("The current node is to be linked to the free list,")
			post("However, the pointer stored by the node will be overwritten")
			post("when linked to the free list.\n")
			post("Correction thus tends to the use of this pointer value first,")
			rfr()
			post("Current Pointer points to {}".format(self.nodeArray[currentPointer].pointer))
			post("This value gives the next head pointer,")
			post("Setting head pointer to point to {}...".format(self.nodeArray[currentPointer].pointer))
			rfr()
			self.headPointer = self.nodeArray[currentPointer].pointer

			post("Now, adding node to the end of the free list...")
			post("Current node is made to point to the node pointed to by the present free pointer,")
			post("Free Pointer: {}".format(self.freePointer))
			rfr()
			self.nodeArray[currentPointer].pointer = self.freePointer
			post("Free pointer is then made to point to the current node...")
			rfr()
			self.freePointer = currentPointer

			post("Checking if tail pointer needs to be modified...")
			post("It needs to be modified if removed node was the tail,")
			post("Freed node: {} and tail node: {}".format(currentPointer, self.tailPointer))
			rfr()
			if currentPointer == self.tailPointer:
				post("It's a match,")
				post("meaning the tail node was removed,")
				post("meaning the list is empty,")
				post("Tail pointer is changed to point to -1.")
				rfr()
				self.tailPointer = -1
			else:
				post("They do not match,")
				post("No change made to tail pointer,")

		rfr()
		return msg
