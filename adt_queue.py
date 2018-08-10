import adt

class Queue(adt.ADT):

	def __doc__(self):
		text = ["A queue is an abstract data type",
		"which works on the principle of Last in, first out.",
		"",
		"Add more elaboration later..."
		]

		return super().__doc__(text)

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
					currentPointer))
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

		## Add postings

		# Short-hand
		post = self.post
		rfr = self.refresh

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
