import threading, time
from kivy.uix.button import Button

"""The Prompts, CallableActions and Unfreeze_Action_Button objects
are used to control the function to be frozen.

Freezing is achieved through multi-threading."""

class Prompts:
	"""An object to store information relevant to an input for the CallableActions object
		Parameters: 
			Keyword name for value expected by the action function run in CallableActions; Eg: 'valueToBeInserted',
			Message to use to prompt for that information,
			Function to validate input which returns True if valid, else error message
	"""
	def __init__(self, valueName, promptMsg, validatorFunc):

		self.valueName = valueName
		self.promptMsg = promptMsg
		self.validatorFunc = validatorFunc

def Null(*args, **kwargs):
	"""Placeholder function which accepts keywords and arguments but does not
		do anything"""
	return None

class PseudoCode:
	"""Contains the pseudocode statements that are associated with each action handled by a Operations class
		Since it was felt necessary to be able to highlight certain portion of the pseudocode text to
		improve the use of the program for teaching algorithms, a solution has been implemented as follows.

		Each statement is a dictionary entry for the 'statement' key, the dictionary contains a Boolean 
		entry for the 'activity' key as flag for whether the statement should be highlighted.

		The method extract uses a string to produce the pseudocode dictionary
		It splits the string through the new-line character

		The method highlight takes a list of index values (with 1 corresponding to the first line in
		the read string) and highlights those statements after deactivating all

		If an invalid index is passed, the 0th index statement (which is blank) lights up

		Is initialized with a single blank statement (index 0)
		"""
	def __init__(self):
		""""A list of strings, each string is a seperate line,	the list is prepared by the extract method
			One additional 0 index entry is added in the beginning of the statements fetched by extract.
			This is to indicate invalid attempts to change statement activity
			For eg, if indices go upto 15 statements and someone attempts to change activity
			for index 17, the change shows for index 0
			Activity means on or off, active statements are those that
			are highlighted, each entry in the statements has an on or off propertry associated with it

			The additional 0 index entry also ensures that the line-numbers that show up in text-editors
			for the pseudocode text which start from 1 match the statement's index here

			Index 0 cannot be made active like the other indices can be since it is an error flag

			Activate means set activity to True for corresponding entry
			"""

		# Each entry is going to be a dictionary with the keys 'statement' and 'activity'
		self.statements = [{"statement": "", "activity": False}] # Index 0 that is automatically added
		self.length = 1

	def extract(self, text):
		statements = text.split("\n")

		# Overwrite
		self.statements = [{"statement": "", "activity": False}] # Index 0 that is automatically added
		self.length = 1

		for statement in statements:
			self.length += 1
			self.statements.append({"statement": statement, "activity": False})

	def highlight(self, indices):
		# Parameter indices is a list of index values for which statements need to be highlighted

		self.deactivateAll()

		for index in indices: # For each index
			if str(index).isdigit(): # If it is a number value
				self.activate(int(index)) # Try to activate it

	def deactivateAll(self):
		for statement in self.statements:
			statement["activity"] = False

	def activate(self, index):
		# Activate the entry at a particular index
		if index > self.length - 1: # If index invalid
			self.statements[0]["activity"] = True

		else:
			if index != 0: # If index is not 0, only then set is as active
				self.statements[index]["activity"] = True

class CallableActions:
	"""Stores information relevant to running a particular function
		Controls freezing the function on a seperate thread
		Parameters:
			name = Name of action; Eg: 'insert', needs to be unique for a single Operations object
			functionToExecute = Function to be controlled,
			lockCallBack = Funciton  which is run everytime a lock is set, the list 
				containing logs is sent to it before being cleared
			endTarget = Function to run after the functionToExceute finishes running
			codeObj = PseudoCode object which is associated with the functionToExecute function

		Use the addPrompts method to add Prompts objects
		They contain information regarding the values to be fed into the functionToBexEcexuted

		This class is responsible for providing functionToExecute functions with the log, lock and light
		functions that add text to log, freeze the function and highlight certain statements in the PseudoCode
		object respectively
	"""
	def __init__(self, name, endTarget,
		functionToExecute = Null, 
		lockCallBack = Null,
		codeObj = PseudoCode()):

		self.prompts = [] #Prompt objects, empty list if no prompts are required

		self.functionToExecute = [functionToExecute]
		self.name = name.lower() #Eg: 'search'

		self.locked = False
		self.processing = False

		self.lockCallBack = lockCallBack
		self.logTexts = []

		self.endTarget = endTarget
		self.codeObj = codeObj

	def addPrompt(self, newPrompt):
		self.prompts.append(newPrompt)

	def lock(self):
		"""Freezes the calling function by using a slowly looping infinite loop
		which continuously checks if the lock has been removed by a user action
		signalling that the function should unfreeze"""
		self.lockCallBack(self.logTexts)
		self.logTexts = []

		self.locked = True

		while self.locked:
			time.sleep(0.15)
			for i in range(20):
				pass

	def log(self, logText):
		"""Adds a string to the log text list"""
		self.logTexts.append(logText)

	def unlock(self):
		self.locked = False

	def light(self, indices):
		self.codeObj.highlight(indices)

	def functionWrapper(self, **kwargs):

		self.functionToExecute[0](**kwargs)

		self.processing = False

		for i in range(40):
			pass

		self.endTarget()

	def executeAssociatedFunction(self, promptedValues):
		#any function to be freezed must expect keyword arguments lock and log

		promptedValues["lock"] = self.lock
		promptedValues["log"] = self.log
		promptedValues["light"] = self.light

		# promptedValues["adtObj"] = self.adtObj
		# print(promptedValues)

		self.processing = True
		self.lock = True

		#the dictionary is ** operated to turn dictionary key into key arguments
		#thus valueName in the Prompts object should match variable names anticipated by function to execute
		
		#a seperate thread is used to keep the rest of the program from freezing with the function
		t = threading.Thread(target = self.functionWrapper, kwargs = promptedValues) 
		t.daemon = True

		t.start()

class Unfreeze_Action_Button(Button):
	"""Used with a CallableActions object,
		The function frozen using CallableActions periodically checks a lock Boolean
		CallableActions class's unlock method sets the Boolean 
		such that the frozen function can continue executing
		Initializes with a CallableActions object reference passed through the action keyword
	"""
	def __init__(self, **kwargs):
		self.action = kwargs["action"]
		del kwargs["action"]

		self.endTarget = [kwargs["endTarget"]]
		del kwargs["endTarget"]

		super(Unfreeze_Action_Button, self).__init__(**kwargs)

		self.text = "Next"
		self.bold = True

		self.finished = False

	def on_press(self, *args):
		if self.action.processing == True and not self.finished:
			self.action.unlock()
		else:
			self.parent.remove_widget(self)
			self.endTarget[0]()

	def finish(self):
		self.action.unlock()
		self.finished = True

		self.text = "Finish"