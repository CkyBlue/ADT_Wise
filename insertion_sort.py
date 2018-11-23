"""See controller.Controller and operations.Operations for info on how to use them"""

### Create a 'Click and drag to scroll...' msg

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from operations import Operations
from labels import ScrollableLabel, HeaderLabel
from data import DataStructure, VariableData, PointerData
from actions import Null, CallableActions, Prompts, PseudoCode, Unfreeze_Action_Button
from controller import CustomController
from customs import DataBoxColor, PointerBox, VariableBox, CustomCmdBox, PseudoBoxWithCount
from boxes import PromptBox, CommandsBox, ScrollBox

from kivy.lang import Builder

# Where the commands like 'Insertion Sort' and necessary properties are defined
# if no need change anything about the GUI this is all you need to customize
class SortOp(Operations):
	def __init__(self, **kwargs):
		super(SortOp, self).__init__(**kwargs)
		
		self.pointers = PointerData(["Current Item"])
		self.variables = VariableData(["Index", "Number of items", "Item to be inserted"])
		self.data = DataStructure(["List Index", "List Item"], name = "List", size = 5)

		sort = CallableActions(name = 'insertion sort', 
			functionToExecute = self.insertionSort, 
			lockCallBack = self.lockCallBack,
			endTarget = self.endTarget,
			codeObj = self.insertion_Sort_PseudoCode())

		self.addAction(sort)
		self.initializeData()

	def insertionSort(self, log = Null, lock = Null, light = Null):

		light([0])

		log("Here we will be exploring how the")
		log("insertion sort algorithm works")
		log("using the data, variables and pointers indicated.")

		lock()

		log("In this algorithm,")
		log("For each item in the list,")
		log("we momentarily focus on ordering")
		log("with respect to it only,")

		lock()

		log("We keep moving it towards the front of the list as long as")
		log("it makes sense to do so.")

		lock()

		log("Note that the list being sorted has index")
		log("starting from 0")

		lock()

		light([1])

		log("Since the item at index 0 cannot be moved any more to the front")
		log("we start by considering index 1 in an iteration")
		self.variables.setValue("Number of items", self.data.size)

		lock()

		log("'Number of items' is the length of the list being sorted")
		log("at {}".format(self.data.size))

		lock()

		for index in range(1, self.data.size):
	
			light([1])	
			log("Currently the index we are considering is {}".format(index))

			self.variables.setValue("Index", index)
			lock()

			itemToBeInserted = self.data.getValue("List Item", index)

			light([2])
			log("The item at this index is {}".format(itemToBeInserted))
			log("")
			log("in this algorithm, the items before the one being considered")
			log("are gradually shifted a step back each as appropriate.")

			lock()

			log("Since the item at the current index will get overwritten,")
			log("it is temporarily stored elsewhere,")
			log("'Item to be inserted' will be set as {}".format(itemToBeInserted))
			log("for this purpose.")

			lock()

			self.variables.setValue("Item to be inserted", itemToBeInserted)

			light([3])

			log("We now need to consider each item before the one at the current index,")
			log("i.e, the'Current Item Pointer' is going to be set as the index just one step before")
			log("{} - 1 gives {} which will be set as the Current Item Pointer.".format(index, index - 1))

			lock()

			currentItemPointer = index - 1
			self.pointers.setValue("Current Item", currentItemPointer)

			log("We now iterate until it is appropriate to stop,")
			log("We know to stop if the item at the 'Current Item Pointer' is no longer")
			log("suitable to be shifted backward.")

			lock()

			log("We will keep shifting items back whilst the items are larger than")
			log("the item which is being temporarily stored elsewhere.")

			lock()

			log("If the item reached is no longer larger than the stored item 'Item to be inserted'")
			log("the place from which the last item was shited is the perfect spot for inserting")
			log("this item as the item before it is smaller than it and the one after is larger than it")

			lock()

			log("the item at a particular index in a list is accessed")
			log("for read and write by the 'List[Index]' notation")

			lock()

			while (self.data.getValue("List Item", currentItemPointer) > itemToBeInserted) and currentItemPointer >= 0:

				light([4])

				log("It is true that the item pointed to by the 'Current Item Pointer' is")
				log("larger than our 'Item to be inserted'.")
				log("")
				log("{} > {}".format(self.data.getValue("List Item", currentItemPointer), itemToBeInserted))

				lock()	

				log("It is also true that the value of 'Current Item Pointer', {}".format(currentItemPointer))
				log("is greater than or equal to 0.")

				lock()

				light([5])			

				log("We will now shift the item at the 'Current Item Pointer' a step backward")
				log("we will do this by dumping the value at the 'Current Item Pointer' index,")

				listValue = self.data.getValue("List Item", currentItemPointer)

				log("which is {} at index {}".format(listValue, currentItemPointer))
				log("into the index position one greater than 'Current Item Pointer'")
				log("which is {} + 1, or  {}".format(currentItemPointer, currentItemPointer + 1))

				lock()
				
				self.data.setValue("List Item", currentItemPointer + 1, listValue)

				light([6])

				log("With this done, we will now decrease 'Current Item Pointer'")
				log("by 1 so that the item before it is considered")

				lock()

				currentItemPointer -= 1
				self.pointers.setValue("Current Item", currentItemPointer)

				log("Notice that the item at the previous 'Current Item Pointer'")
				log("{} is itself untouched for now,".format(listValue))

				lock()

				log("depending on the item before it, it will be overwritten")
				log("by 'Item to be inserted' or the item at the index of {}".format(currentItemPointer))
				log("the index given by the 'Current Item Pointer'")	

			light([7])

			if currentItemPointer < 0:
				log("The item pointed to by the 'Current Item Pointer' is")
				log("no longer larger than our 'Item to be inserted'.")
				log("")
				log("{} < {}".format(self.data.getValue("List Item", currentItemPointer), itemToBeInserted))

			else:
				log("The value of 'Current Item Pointer', {} is no longer".format(currentItemPointer))
				log("greater than or equal to 0.")

			lock()

			light([8])

			log("The index right behind 'Current Item Pointer', {}'".format(currentItemPointer + 1))
			log("is where 'Item to be inserted', {}".format(itemToBeInserted))
			log("should be dumped as the item at behind that, at {}".format(currentItemPointer + 2))
			log("is larger than 'Item to be inserted")

			lock()

			self.data.setValue("List Item", currentItemPointer + 1, itemToBeInserted)

			log("If applicable,")
			log("we will now consider the next index behind the one from which we")
			log("took 'Item to be inserted', i.e index {}".format(index + 1))

			lock()

		light([9])

		log("The index {} does not exist".format(index + 1))
		log("and we have finished going through the entire list.")
		log("The list is sorted now.")

		lock()

	def initializeData(self):
		for i in range(5):
			self.data.setValue("List Index", i, str(i))
			self.data.setValue("List Item", i, chr(ord('z') - i * 2))

	def insertion_Sort_PseudoCode(self):
		f = open("insertionSort_pseudo.txt", "r")
		# print(f.read().split("\n"))
		p = PseudoCode()
		p.extract(f.read())
		return p

# The GUI Controller which uses the SortOp class as source
c = CustomController(source = SortOp)

class anApp(App):
	def build(self):
		return c #Returning instance of controller object c

anApp().run()