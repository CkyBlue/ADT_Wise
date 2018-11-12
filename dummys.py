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
	"""Ensure that the CallableActions objects have unique names"""
	def __init__(self):
		self.data = dummyData
		self.logTarget = lambda x: print(parse(x))

		insert = CallableActions('insert', self.dummyInsert, self.logTarget, self)
		insert.addPrompt(Prompts("itemToBeInserted", "Item", dummyValidator))

		remove = CallableActions('remove', self.dummyRemove, self.logTarget, self)

		self.actions = [insert, remove]

	def dummyInsert(adtObj, itemToBeInserted, log, lock):
		log("Changing Index")
		lock()
		adtObj.data.setValue("Index", 0, 0)

		log("Changing Value")
		lock()
		adtObj.data.setValue("Value", 0, itemToBeInserted)

		log("Changing Pointer")
		lock()
		adtObj.data.setValue("Pointer", 0, 1)

	def dummyRemove(adtObj, log, lock):
		log("Changing Index")
		lock()
		adtObj.data.setValue("Index", 0, 0)

		log("Changing Value")
		lock()
		adtObj.data.setValue("Value", 0, "")

		log("Changing Pointer")
		lock()
		adtObj.data.setValue("Pointer", 0, -1)

	def initializeDataStructure(self):
		pass

for i in range(12):
	dummyData.setValue("Index", i, str(i))
	dummyData.setValue("Value", i, "Ram" + str(i))
	dummyData.setValue("Pointer", i, str(i + 1))

dummyADT = ADT()

