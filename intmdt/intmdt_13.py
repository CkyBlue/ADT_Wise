from kivy.app import App

from controller import Controller
from dummys import dummyADT

class dummyController(Controller):
	def buildInternal(self):
		self.orientation = 'vertical'

		self.commandsBox = CommandsBox(actions = self.source.actions,
			target = self.cmdTarget)
		self.add_widget(self.commandsBox)

		self.logBox = ScrollableLabel()
		self.add_widget(self.logBox)

		print(self.pseudoCode.statements)

		self.pesudoCodeBox = PseudoCodeBox(source = self.pseudoCode)
		self.pseudoCodeScrollBox = ScrollBox()
		self.pseudoCodeScrollBox.add_widget(self.pesudoCodeBox)
		self.add_widget(self.pseudoCodeScrollBox)

		self.dataTable = DataBoxColor(source = self.source.data)
		self.dataTableScrollBox = ScrollBox()
		self.dataTableScrollBox.add_widget(self.dataTable)
		self.add_widget(self.dataTableScrollBox)

		self.pointerTable = PointerBox(source = self.source.pointers)
		self.pointerTableScrollBox = ScrollBox()
		self.pointerTableScrollBox.add_widget(self.pointerTable)
		self.add_widget(self.pointerTableScrollBox)

	def lockCallBack(self, logTexts):
		self.dataTable.updateContent()
		self.pointerTable.updateContent()
		self.pesudoCodeBox.updateContent()

		text = self.parse(logTexts)
		self.logBox.setText(text)

	def actionEndTarget(self):
		self.actionIsRunning = False

		self.dataTable.dataBox.updateContent()
		self.pointerTable.pointerBox.updateContent()
		
		self.destroyNav()
		# self.logBox.setText("")

newDummy = dummyController(source = dummyADT)

class guiApp(App):
	def build(self):
		return newDummy

guiApp().run()