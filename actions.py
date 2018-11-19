### Set things up so that log and code target rely on the single unlockCallBack method

import threading, time
from kivy.uix.button import Button
from pseudo import PseudoCode

"""Contains the Prompts and CallableActions objects
which are used to control the function to be frozen"""

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
	return None

class CallableActions:
	"""Stores information relevant to running a particular function
		Controls freezing the function on a seperate thread
		Parameters:
			Name of action; Eg: 'insert',
			Function to be controlled,
			Funciton to which the list containing logs is sent
			Function to run after the functionToExceute finishes running

		Use the addPrompts method to add Prompts objects
		They contain information regarding the values to be fed into the functionToBexEcexuted
	"""
	def __init__(self, name, 
					functionToExecute = Null, 
					lockCallBack = Null,
					endTarget = Null,
					codeObj = PseudoCode()):
		self.prompts = [] #Prompt objects, empty list if no prompts are required
		self.functionToExecute = functionToExecute
		self.name = name.lower() #Eg: 'search'
		# self.adtObj = adtObj #The ADT object the functionToExecute method needs to be able to interact with

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
		self.functionToExecute(**kwargs)

		self.processing = False
		self.endTarget()

	def executeAssociatedFunction(self, promptedValues):
		#any function to be freezed must expect keyword arguments lock and log

		promptedValues["lock"] = self.lock
		promptedValues["log"] = self.log
		promptedValues["light"] = self.light

		# promptedValues["adtObj"] = self.adtObj
		# print(promptedValues)

		self.processing = True

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

		super(Unfreeze_Action_Button, self).__init__(**kwargs)

		self.text = "Next"
		self.bold = True

	def on_press(self, *args):
		self.action.unlock()