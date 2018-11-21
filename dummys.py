from data import DataStructure, PointerData
from actions import Prompts, CallableActions, PseudoCode

def dummyValidator(data):
	if data:
		return True
	else:
		return "Error Message"

dummyData = DataStructure(["Index", "Value", "Pointer"], name = "Dummy")

def Null(*args, **kwargs):
	return None

### Later on use a base Operations class instead of ADT class
class dummyADT:
	"""Ensure that the CallableActions objects have unique names
		The functions that go as parameters into CallableActions are preferably methods of this class
		so that the object reference self if passed automatically and the method can interact with
		the ADTs data structure without additional adt parameters
	"""
	def __init__(self, 
				lockCallBack = Null, 
				actionEndTarget = Null):

		self.data = dummyData
		self.pointers = PointerData(["Head", "Tail", "Free"])

		self.lockCallBack = lockCallBack
		self.endTarget = actionEndTarget

		insert = CallableActions(name = 'insert', 
								functionToExecute = self.dummyInsert, 
								lockCallBack = self.lockCallBack,
								endTarget = self.endTarget,
								codeObj = self.pseudoForInsert())

		insert.addPrompt(Prompts("itemToBeInserted", "Item", dummyValidator))

		remove = CallableActions(name = 'remove', 
								functionToExecute = self.dummyRemove,  
								lockCallBack = self.lockCallBack,
								endTarget = self.endTarget,
								codeObj = self.pseudoForInsert())

		self.actions = [insert, remove]

	def pseudoForInsert(self):
		text = "Do A"
		text += "\n" + "Do B"
		text += "\n" + "Do C"
		text += "\n" + "Do D"

		p = PseudoCode()
		p.extract(text)

		return p

	def dummyInsert(self, itemToBeInserted, log, lock, light):
		log("Changing Index and Free Pointer")
		lock()
		light([1, 2])
		self.pointers.setValue("Free", "12")
		self.data.setValue("Index", 0, "12")

		log("Changing Value")
		lock()
		light([3, 4])
		self.data.setValue("Value", 0, itemToBeInserted)

		log("Changing Pointer")
		lock()
		self.data.setValue("Pointer", 0, "8")

	def dummyRemove(self, log, lock, light):
		log("Changing Index")
		light([1, 2])
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



