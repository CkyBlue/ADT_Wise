### Modify this for a standard base class
### Consider implementing a way to track code within pseudocode

### Use it to create a queue and finish packaging a queue app

from data import DataStructure
from pseudo import PseudoCode
from actions import CallableActions, Prompts

class RepeatedNames(Exception):
	pass

def Null(*args, **kwargs):
	return None

class Operations:
	"""Ensure that the CallableActions objects have unique names
		The functions that go as parameters into CallableActions are preferably methods of this class
		so that the object reference self if passed automatically and the method can interact with
		the Operations objects data structure without additional adt parameters

		Refer to the '##' commented out code in the init to see how polymorphism should be implemented
	
		Overwrite init to read a source
	"""
		
	def __init__(self, 
		lockCallBack = Null, 
		actionEndTarget = Null):
		
		# '##' precedes example code for polymorphism

		# -------------- Definition that can be inherited without problem --------------

		#Call back functions to be used by CallableActions objects

		self.lockCallBack = lockCallBack
		self.endTarget = actionEndTarget

		# A list of CallableActions objects that represent all operations that can be called on the ADT.
		self.actions = [] 

		# A method which sets up self.data with the required initial values 
		self.initializeDataStructure()  

		# ------------------------------------------------------------------------------

		# Creating CallableActions object, class ensures name becomes lowercase
		# If the names are not 
		
		## insert = CallableActions(name = 'insert', 
		## 				functionToExecute = self.dummyInsert, 
		## 				lockCallBack = self.lockCallBack,
		## 				endTarget = self.endTarget,
		## 				codeObj = self.pseudoForInsert())

		## insert.addPrompt(Prompts("itemToBeInserted", "Item", validatorFunc))

		# validatorFunc gives True if data entered is valid for an 'Item'
		# if data is invalid, it should give error text as a single string
		# the first value must match one of the values being expected by 
		# the function that CallableActions is used to freeze
		# the second value gives the text used to prompt for that value

		## self.addAction(insert) # Store the created action as an action associated with the class

		# Adding object instantiated from classes in data

		## self.data = dummyData
		## self.pointers = PointerData(["Head", "Tail", "Free"])

	# The following is a function that is prepared to be passed into the above insert CallableActions 
	# object, The null is there just in case the parameter is not passed
	# Intended to integrate an additional a pseudocode log easily if need arises
	# and allow using 
	# log and lock are passed in my the CallableActions object that controls this function

	##  def dummyInsert(self, itemToBeInserted, log = Null, lock = Null):
		##  log("Explanation text")
		##  lock() # Freezes the functiton and updates the visuals (data table and log box)
		##  self.data.setValue("Index", 0, "12") # Code that does stuff

	def addAction(self, newAction):
		# Ensures action names are unique and adds CallableActions objects properly to the class

		for action in self.actions:
			if action.name == newAction.name:
				error = "The name '{}' is being used for multiple CallableActions objects".format(action.name)
				raise RepeatedNames(error)

		self.actions.append(newAction)

	def initializeDataStructure(self):
		# Should create and initialize values within self.data
		## self.data = DataStructure("Index", "ID", "Value" ... , size = {}, name = {})

		pass

class Queue(Operations):
	def __init__(self, **kwargs):
		super(Queue, self).__init__(**kwargs)
		
		insert = CallableActions(name = 'insert', 
						functionToExecute = self.insert, 
						lockCallBack = self.lockCallBack,
						endTarget = self.endTarget,
						codeObj = PseudoCode())

		insert.addPrompt(Prompts("itemToBeInserted", "Item", self.insertValidator))

		self.addAction(insert)

	def insertValidator(self, value):
		# Shouldn't be longer than 20 letters
		if len(value) > 20: 
			return "Too long, make it the item shorter than 20 letters."
		else:
			return True

	def insert(self, itemToBeInserted, log = Null, lock = Null, light = Null):
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

q = Queue()
			
