from data import DataStructure
from actions import CallableActions, Prompts, Null, PseudoCode

class RepeatedNames(Exception):
	"""Custom exception to throw if CallableActions objects belonging to one Operations based object
		have the same name property. The name needs to be unique as it is used to access the CallableActions
		object"""
	pass

class Operations:
	"""This class is used together with the Controller class to create the GUI
		The class (not its instance) is passed into a controller's init through the source keyword
		It is instantiated such that the callbacks passed by the Controller are sent where
		they are appropriate.

		Certain parts of the controller are dependent on how the source class (the base Operations
		class or an inheriting sub-class) is set up. If Operations uses a VariableBox, for eg,
		the buildInternal method and doUpdates method will need to be set up to interact with it

		Each Class from data such as DataStructure has a corresponding box in boxes (or customized boxes
		in customs)

		Each command that Operations is supposed to accomodate is defined as a CallableActions object
		See actions.CallableActions for more detail

		The method defined here to use for the command is passed into the CallableActions object's init
		and the object is used to run it. The object handles keeping the method on its own thread and
		controlling its freezing

		The method needs to anticipate the lock, log and light functions with respectively named keywords.

		Methods that need input utilize the Prompts class (see action.Prompts and see below to see init how
		it is used)

		After creating a CallableActions object, it needs to be passed into
		the addAction method (as show in init) to ensure that the Controller can access it

		Ensure that the CallableActions objects used in the class have unique names
		The functions that go as parameters into CallableActions are preferably methods of this class
		so that the object reference self if passed automatically and the method can interact with
		the Operations objects data structure without additional adt parameters

		Use getActions to get a list of all actions associated with the class

		Refer to the '##' commented out code in the init to see how polymorphism should be implemented
	
		Overwrite init for your custom Operations classes
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

		# By default, setting them to none so that the Controller can read them without throwing
		# an exception

		self.data = None
		self.pointers = None
		self.variables = None

	# The following is a function that is prepared to be passed into the above insert CallableActions 
	# object, The null is there just in case the keyword parameter is not passed
	# Intended to integrate an additional a pseudocode log easily if need arises
	# and allow using 
	# log and lock are passed in my the CallableActions object that controls this function

	def getActions(self):
		return self.actions

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

