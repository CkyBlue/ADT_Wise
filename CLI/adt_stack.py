import adt

class Stack(adt.ADT):
	def __doc__(self):
		text = ["A stack is an abstract data type",
		"which works on the principle of First in, first out.",
		"",
		"Add more elaboration later..."
		]

		return super().__doc__(*text)

	def getFreePointer(self):
		return self.freePointer

	def getBaseOfStackPointer(self):
		return self.baseOfStackPointer

	def getTopOfStackPointer(self):
		return self.topOfStackPointer

	def __init__(self, name, length):
		super().__init__(name, length, True) # pointer = True

		# Stack's pointers

		self.baseOfStackPointer = -1
		self.topOfStackPointer = -1
		self.freePointer = 0

		# Stack's node array

		self.nodeArray = [adt.linkNode() for i in range(self.numberOfNodes)]
		self.initialize(self.nodeArray)

		# Overwrite

		self.pointers = ["Free Pointer", "Base Of Stack Pointer", "Top Of Stack Pointer"]
		self.pointerNameToMethod = {"Free Pointer": self.getFreePointer, 
			"Base Of Stack Pointer": self.getBaseOfStackPointer, 
			"Top Of Stack Pointer": self.getTopOfStackPointer}

	def insert(self, itemToBeInserted):
		msg = [] # End message

		# Short-hand
		post = self.post
		rfr = self.refresh

		if self.freePointer == -1:
			msg.sppend("No free node.")
		else:
			currentPointer = self.freePointer
			self.nodeArray[currentPointer].item = itemToBeInserted
			self.freePointer = self.nodeArray[currentPointer].pointer

			self.nodeArray[currentPointer].pointer = self.topOfStackPointer
			self.topOfStackPointer = currentPointer

			if currentPointer == 0:
				self.baseOfStackPointer = currentPointer

		return msg

	def remove(self):
		msg = [] # End message

		# Short-hand
		post = self.post
		rfr = self.refresh

		if self.topOfStackPointer == -1:
			msg.sppend("Empty Stack.")
		else:
			currentPointer = self.topOfStackPointer
			popVal = self.nodeArray[currentPointer].item
			self.nodeArray[currentPointer].item = ""

			self.topOfStackPointer = self.nodeArray[currentPointer].pointer

			self.nodeArray[currentPointer].pointer = self.freePointer
			self.freePointer = currentPointer

			if self.topOfStackPointer == -1:
				self.baseOfStackPointer = -1

			msg.append(popVal)

		return msg

	def search(self, itemToBeSearched):
		msg = [] # End message

		# Short-hand
		post = self.post
		rfr = self.refresh

		if self.topOfStackPointer == -1:
			msg.sppend("Stack is empty.")
		else:
			currentPointer = self.topOfStackPointer
			while currentPointer != -1 and itemToBeSearched != self.nodeArray[currentPointer].item:
				currentPointer = self.nodeArray[currentPointer].pointer
			if currentPointer == -1:
				msg.sppend("Item not found.")
			else:
				msg.sppend("Item found at index: {}".format(currentPointer))

		return msg
