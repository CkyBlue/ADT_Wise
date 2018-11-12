import threading, time

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

def parse(log):
	"""Takes a list and gives a string where the items are indivisual statements"""

	content = ""

	for statement in log:
		content += statement + "\n"

	return content

class CallableActions:
	"""Stores information relevant to running a particular function
		Controls freezing the function on a seperate thread
		Parameters:
			Name of action; Eg: 'insert',
			Function to be controlled,
			Funciton to which the list containing logs is sent

		Use the addPrompts method to add Prompts objects
		They contain information regarding the values to be fed into the functionToBexEcexuted
	"""
	def __init__(self, name, functionToExecute, logTarget, adtObj):
		self.prompts = [] #Prompt objects
		self.functionToExecute = functionToExecute
		self.name = name #Eg: 'search'
		self.adtObj = adtObj #The ADT object the functionToExecute method needs to be able to interact with

		self.locked = False
		self.processing = False

		self.logTarget = logTarget
		self.logTexts = []

	def addPrompt(self, newPrompt):
		self.prompts.append(newPrompt)

	def lock(self):
		"""Freezes the calling function by using a slowly looping infinite loop
		which continuously checks if the lock has been removed by a user action
		signalling that the function should unfreeze"""
		self.logTarget(self.logTexts)
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

	def executeAssociatedFunction(self, promptedValues):
		#any function to be freezed must expect keyword arguments lock and log

		promptedValues["lock"] = self.lock
		promptedValues["log"] = self.log
		promptedValues["adtObj"] = self.adtObj

		self.processing = True

		#the dictionary is ** operated to turn dictionary key into key arguments
		#thus valueName in the Prompts object should match variable names anticipated by function to execute
		
		#a seperate thread is used to keep the rest of the program from freezing with the function
		t = threading.Thread(target = self.functionToExecute, kwargs = promptedValues) 
		t.daemon = True

		t.start()

		self.processing = False

if __name__ == "__main__":
	from dummys import dummyInsert, dummyValidator

	insertAction = CallableActions("insert", dummyInsert, lambda x: print(parse(x)))
	insertAction.addPrompt(Prompts("itemToBeInserted", "Enter item to be inserted", dummyValidator))
	insertAction.addPrompt(Prompts("idToBeInserted", "Enter id to be inserted", dummyValidator))

	insertAction.executeAssociatedFunction({"obj": "String", "itemToBeInserted": "Ram", "idToBeInserted": "12"})

	for i in range(4):
		x = input()
		insertAction.unlock()