### Modify this for a standard base class
### Consider implementing a way to track code within pseudocode

### Use it to create a queue and finish packaging a queue app

from data import DataStructure

def Null(*args, **kwargs):
	return None

class ADT:
	"""Ensure that the CallableActions objects have unique names
		The functions that go as parameters into CallableActions are preferably methods of this class
		so that the object reference self is passed automatically and the method can interact with
		the ADTs data structure without additional adt parameters
	
		Refer to the '##' commented out code in the init to see how polymorphism should be implemented
	"""
	def __init__(self, logTarget = Null, endTarget = Null):
		# '##' precedes examsple code for polymorphism

		# -------------- Definition that can be inherited without problem --------------

		# Remember the targets are available to you when creating CallableActions objects
		# to which they need to be passed

		self.logTarget = logTarget
		self.endTarget = endTarget

		# A list of CallableActions objects that represent all operations that can be called on the ADT.
		self.actions = [] 

		# A method which sets up self.data with the required initial values 
		self.initializeDataStructure()  

		# ------------------------------------------------------------------------------

		# ... in the following ## code means more strings can be passed as arguments, 
		# they each behave as a column header
		# The {}s are places where you would put values as needed, name is not an optional keyword
		#  size is though,

		# Creating CallableActions object, class ensure name becomes lowercase
		
		## insert = CallableActions(name = 'insert', 
		## 						functionToExecute = self.dummyInsert, 
		## 						logTarget = self.logTarget, 
		## 						endTarget = self.endTarget)

		# validatorFunc gives True if data entered is valid for an 'Item'
		# if data is invalid, it should give error text as a single string
		# the first value must match one of the values being expected by 
		# the function that CallableActions is used to freeze
		# the second value gives the text used to prompt for that value

		## insert.addPrompt(Prompts("itemToBeInserted", "Item", validatorFunc))

	# A function that is prepared to be passed into the above insert CallableActions object
	# The null is there just in case the parameter is not passed
	# Intended to integrate an additional a pseudocode log easily if need arises
	# and allow using 
	# log and lock are passed in my the CallableActions object that controls this function

	##  def dummyInsert(self, itemToBeInserted, log = Null, lock = Null):
	## 		log("Explanation text")
	## 		lock() # Freezes the functiton and updates the visuals (data table and log box)
	## 		self.data.setValue("Index", 0, "12") # Code that does stuff

	def initializeDataStructure(self):
		# Should create and initialize values within self.data
		## self.data = DataStructure("Index", "ID", "Value" ... , size = {}, name = {})

		pass

class Queue(ADT):
	def __init__(self, **kwargs):
		super(Queue, self).__init__(**kwargs)
		
		insert = CallableActions(name = 'insert', 
								functionToExecute = self.dummyInsert, 
								logTarget = self.logTarget, 
								endTarget = self.endTarget)

		## insert.addPrompt(Prompts("itemToBeInserted", "Item", validatorFunc))
	
	def insert(self, itemToBeInserted, log = Null, lock = Null):
		"""Adds an item to the tail of the queue if it is not full."""

		newItem = itemToBeInserted

		log("We'll be performing an insertion,")

		lock()

		log("Checking if the operation can be performed...")
		log("Operation possible if free pointer does not point to null.")
		log("Free Pointer: {}".format(self.freePointer))

		lock()

		# Checking eligibility
		if self.freePointer == -1:
			log("Pointer to free node is null.")
			log("This means there is no empty node.")

			lock()

			log("The Item could thus not be inserted.")

		else:

		# Handling key operations

			log("We need a free node to work with.")
			log("The head of the free list,")
			log("given by the free pointer will do.")

			lock()

			log("Moving to free node...")
			log("The current pointer changes to {}.".format(self.freePointer))

			lock()

			self.currentPointer = self.freePointer
			log("Setting item at free node to {}".format(newItem))

			lock()		

			self.nodeArray[self.currentPointer].item = newItem 

		# Correct Flow
			log("We'll be now adjusting the link between nodes")
			log("so that the data retains link information required for")
			log("the data structure to behave as a queue.")

			# Free list

			pointerTo = self.nodeArray[self.currentPointer].pointer

			log("The index value {} that the current node points to will be overwritten,".format(pointerTo))
			log("because it will be used to to incorporate the current node into the data list.")
			log("\nBefore this overwriting occurs, any action that makes use of this pointer needs to be completed.")
			
			lock()

			log("With this rationalization,")
			log("correction will use that address first.")

			lock()

			log("The current node is linked into the free list,")
			log("which is setup such that the free pointer points to")
			log("the head of the free list (which has now used by us to store the new item),")
			log("which points to another free node which points to another free node and so on.")

			lock()

			log("The index it points to thus can be used as the next free node.")
			log("New free pointer: {}".format(pointerTo))

			lock()			

			self.freePointer = pointerTo 

			# Data list			
			if self.tailPointer != -1:

				log("As for the data list,")
				log("The previous tail at index {} is set to point to the current tail at {}.".format(self.tailPointer,
					self.currentPointer))

				lock()

				self.nodeArray[self.tailPointer].pointer = self.currentPointer	

				log("This is done because that information will be needed when popping heads.")
				log("When a head node is popped, a new head node is required.")
				log("By setting up each node to point to the one which came after it,")
				log("we have a means of fetching the next logical head.")

				lock()
						
			log("Since current node is now the new tail, it does not need to point to anything.")
			log("Thus, the current node should point to: {}".format(-1))

			lock()

			self.nodeArray[self.currentPointer].pointer = -1

			log("Setting the tail pointer as: {}".format(self.currentPointer))

			lock()

			self.tailPointer = self.currentPointer

			if self.headPointer == -1:
				log("Since the current node is the new head, the head pointer is also modified...")
				log("Head pointer is set to: {}".format(self.currentPointer))

				lock()

				self.headPointer = self.currentPointer

			log("All done.")
			log("Item successfully inserted.")

			lock()

			
