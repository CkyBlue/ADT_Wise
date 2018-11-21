### Document COntroller to give info about how the over-writing should be done
### Try to see if a presentation implementation through kv can work properly

### Create a 'Click and drag ...' msg
### Create a w/ msg ScrollBox generating method

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from operations import Operations
from labels import ScrollableLabel, HeaderLabel
from data import DataStructure, VariableData, PointerData
from actions import Null, CallableActions, Prompts, PseudoCode
from controller import Controller
from customs import DataBoxColor, PointerBox, VariableBox
from boxes import PromptBox, CommandsBox, PseudoCodeBox, ScrollBox

from kivy.lang import Builder

class SortOp(Operations):
	def __init__(self, **kwargs):
		super(SortOp, self).__init__(**kwargs)
		
		self.pointers = PointerData(["Current Item"])
		self.variables = VariableData(["Index", "Number of items", "Item to be inserted"])
		self.data = DataStructure(["List Index", "List Item"], name = "List", size = 10)

		sort = CallableActions(name = 'insertion sort', 
			functionToExecute = self.insertionSort, 
			lockCallBack = self.lockCallBack,
			endTarget = self.endTarget,
			codeObj = PseudoCode())

		self.addAction(sort)
		self.initializeData()

	def insertionSort(self, log = Null, lock = Null, light = Null):

		for index in range(2, self.data.size):
			self.variables.setValue("Index", index)

			itemToBeInserted = self.data.getValue("List Item", index)
			self.variables.setValue("Item to be inserted", itemToBeInserted)

			currentItemPointer = index - 1
			self.pointers.setValue("Current Item", currentItemPointer)

			while (self.data.getValue("List Item", currentItemPointer) > itemToBeInserted) and currentItemPointer > 0:
				listValue = self.data.getValue("List Item", currentItemPointer)
				self.data.setValue("List Item", currentItemPointer + 1, listValue)

				currentItemPointer -= 1

			self.data.setValue("List Item", currentItemPointer + 1, itemToBeInserted)

	def initializeData(self):
		for i in range(10):
			self.data.setValue("List Index", i, str(i))
			self.data.setValue("List Item", i, chr(ord('z') - i * 2))

class SortCt(Controller):

	def buildInternal(self):
		self.orientation = 'vertical'

		self.commandsBox = CommandsBox(actions = self.source.actions,
			target = self.cmdTarget)
		self.add_widget(self.commandsBox)

		explanations = BoxLayout()

		self.logBox = ScrollableLabel()
		explanations.add_widget(self.logBox)

		self.pseudoCodeBox = PseudoCodeBox(source = self.pseudoCode)
		explanations.add_widget(self.makeScroll(self.pseudoCodeBox))

		self.add_widget(explanations)

		data = BoxLayout()

		self.dataTable = DataBoxColor(source = self.source.data)
		data.add_widget(self.makeScroll(self.dataTable))

		variables = BoxLayout()

		self.variableBox = VariableBox(source = self.source.variables)
		variables.add_widget(self.makeScroll(self.variableBox))

		self.pointerBox = PointerBox(source = self.source.pointers)
		variables.add_widget(self.makeScroll(self.pointerBox))

		data.add_widget(variables)

		self.add_widget(data)

	def makeScroll(self, box):
		s = ScrollBox()
		s.add_widget(box)
		return s

	def lockCallBack(self, logTexts):
		self.variableBox.updateContent()
		self.pointerBox.updateContent()
		self.pseudoCodeBox.updateContent()

		text = self.parse(logTexts)
		self.logBox.setText(text)

c = SortCt(source = SortOp)

class anApp(App):
	def build(self):
		return c

anApp().run()
