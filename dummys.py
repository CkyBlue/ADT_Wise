#####ADT needs to anticpate a logTarget keyword since the target is set at initialization
##### and overwriting later wont change the logTarget of the CalllableActionsObject

### Fully build the ADT class to have usable actions that interact with the DataStructure
### Controller will need to check if prompts exist before building a promptsbox
### Add a reponse for after the freeze function is completely processed

from data import DataStructure
from actions import Prompts, CallableActions

def dummyValidator(data):
	if data:
		return True
	else:
		return "Error Message"

dummyData = DataStructure("Index", "Value", "Pointer", size = 12, name = "Dummy")

class ADT:
	"""Ensure that the CallableActions objects have unique names
		The functions that go as parameters into CallableActions are preferably methods of this class
		so that the object reference self if passed automatically and the method can interact with
		the ADTs data structure without additional adt parameters
	"""
	def __init__(self, logTarget, endTarget):
		self.data = dummyData
		self.logTarget = logTarget
		self.endTarget = endTarget

		insert = CallableActions('insert', self.dummyInsert, self.logTarget, self.endTarget)
		insert.addPrompt(Prompts("itemToBeInserted", "Item", dummyValidator))

		remove = CallableActions('remove', self.dummyRemove, self.logTarget, self.endTarget)

		self.actions = [insert, remove]

	def dummyInsert(self, itemToBeInserted, log, lock):
		log("Changing Index")
		lock()
		self.data.setValue("Index", 0, "12")

		log("Changing Value")
		lock()
		self.data.setValue("Value", 0, itemToBeInserted)

		log("Changing Pointer")
		lock()
		self.data.setValue("Pointer", 0, "8")

	def dummyRemove(self, log, lock):
		log("Changing Index")
		lock()
		self.data.setValue("Index", 0, "5")

		log("Changing Value")
		lock()
		self.data.setValue("Value", 0, "")

		log("Changing Pointer")
		lock()
		self.data.setValue("Pointer", 0, "-1")

	def initializeDataStructure(self):
		pass

for i in range(12):
	dummyData.setValue("Index", i, str(i))
	dummyData.setValue("Value", i, "Ram" + str(i))
	dummyData.setValue("Pointer", i, str(i + 1))



