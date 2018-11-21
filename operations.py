from data import DataStructure
from actions import CallableActions, Prompts, Null, PseudoCode

class RepeatedNames(Exception):
	pass

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

		## self.data = DataStructure([...])
		## self.pointers = PointerData([...])

	# The following is a function that is prepared to be passed into the above insert CallableActions 
	# object, The null is there just in case the keyword parameter is not passed
	# Intended to integrate an additional a pseudocode log easily if need arises
	# and allow using 
	# log and lock are passed in my the CallableActions object that controls this function

	##  def dummyInsert(self, itemToBeInserted, log = Null, lock = Nul, light = Null):
		##  log("Explanation text")
		##  light([1, 2]) # Light up statement 1 and 2 in the pseudocode (starts from 1) 
		##  lock() # Freezes the functiton and updates the visuals (data table and log box)
		##  self.data.setValue("Index", 0, "12") # Code that does stuff

	def addAction(self, newAction):
		# Ensures action names are unique and adds CallableActions objects properly to the class

		for action in self.actions:
			if action.name == newAction.name:
				error = "The name '{}' is being used for multiple CallableActions objects".format(action.name)
				raise RepeatedNames(error)

		self.actions.append(newAction)

