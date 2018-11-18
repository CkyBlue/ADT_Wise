### Kivy, break long sentences

### A pesudocode object hasn't been sent into dummy's actionss yet
### The logTarget here should update the source pseudocode
### PesudoCodeBox should be capable of handling reconstruction


### Thoroughly Document this
### Consider adding a pseduocodeLogger
### Create a class for my PopUps
### Should output an error message saying that an action is already running if it is

"""Note: The reference to an object is preserved unless the object referred to 
is entirely overwritten. Passing in a source object to a box and modifying source's properties will
allow the reference to source in the box to keep up. If the source object is assigned to a new object, 
however, the reference in the box becomes disconnected. At least that's what it looked like was happening."""

from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from kivy.lang import Builder

from dummys import dummyData, dummyADT
from boxes import PromptBox, CommandsBox, PseudoCodeBox
from labels import ScrollableLabel
from actions import Unfreeze_Action_Button
from pseudo import PseudoCode
from customs import Scroll_Box_For_DataBoxColor, Scroll_Box_For_PointerBox

kv = """
"""
Builder.load_string(kv)

class Root(BoxLayout):
	"""The methods with target in their names are passed as callback functions
		The rest of their name gives information regarding what event they are associated with

		Manager functions (those with manage in their names) are controlled by target functions
		They contain the logic which controls decision making and control monitoring/control variables
		For eg, promptsManager checks if another prompt is already present and decides what to do if one is

		To nest and re-arrange child widgets, over-write build-internal
	"""
	def __init__(self, **kwargs):
		super(Root, self).__init__(**kwargs)

		self.promptPopUp = None
		self.adt = dummyADT(logTarget = self.logTarget, 
							endTarget = self.actionEndTarget,
							codeTarget = self.codeTarget)

		self.buildInternal()

	def buildInternal(self):
		self.orientation = 'vertical'

		self.actionIsRunning = False
		self.pseudoCode = PseudoCode()

		self.commandsBox = CommandsBox(actions = self.adt.actions,
			target = self.cmdTarget)
		self.add_widget(self.commandsBox)

		self.logBox = ScrollableLabel()
		self.add_widget(self.logBox)

		self.pesudoCodeBox = PseudoCodeBox(source = self.pseudoCode)
		self.add_widget(self.pesudoCodeBox)

		self.dataTable = Scroll_Box_For_DataBoxColor(source = self.adt.data)
		self.add_widget(self.dataTable)

		self.pointerTable = Scroll_Box_For_PointerBox(source = self.adt.pointers)
		self.add_widget(self.pointerTable)

	def parse(self, logTexts):
		"""Takes a list and gives a string where the items are indivisual statements,"""
		logString = ""

		for statement in logTexts:
			logString += statement + "\n"

		return logString

	def getActionFromName(self, name):
		"""CallableActions objects belonging to a particular ADT
			need to be assigned the name property uniquely
			The name is used to as text for the CommandsBox button which 
			is associated with that CallableActions object
			The name is passed on submission to build the prompt

			This function uses the name of a CallableActions object
			to return a reference

			Returns False if no match found

			The name is ensured to be lowercase since CallableActionss object 
			ensures the name it is initialized with is lowercase"""

		name = name.lower()

		for action in self.adt.actions:
			if action.name == name:
				return action

		return False 

	def promptEndTarget(self, name, promptedValues):	
		self.action = self.getActionFromName(name)
		self.promptedValues = promptedValues

		if self.action != False:
			self.pseudoCode = self.action.codeObj

			#source needs to be re-linked because of the above overwriting
			self.pesudoCodeBox.source = self.pseudoCode 
			self.pesudoCodeBox.buildInternal()
			self.navManager()

		self.promptPopUp.dismiss()
		self.promptPopUp = None

	def navManager(self):
		"""If an action is not running, create a navButton (i.e Unfreeze_Action_Button)
			and set actionIsRunning to True
		"""

		if not self.actionIsRunning:
			self.action.executeAssociatedFunction(self.promptedValues)
			self.createNav()

			self.actionIsRunning = True

	def createNav(self):
		self.navButton = Unfreeze_Action_Button(action = self.action)
		self.add_widget(self.navButton)

	def logTarget(self, logTexts):
		self.dataTable.dataBox.updateContent()
		self.pointerTable.pointerBox.updateContent()

		text = self.parse(logTexts)
		self.logBox.setText(text)

	def codeTarget(self, indices):
		print("Code Target Running")
		pass

	def actionEndTarget(self):
		self.actionIsRunning = False
		self.dataTable.dataBox.updateContent()
		
		self.destroyNav()
		# self.logBox.setText("")

	def destroyNav(self):
		if not self.actionIsRunning:
			self.navButton.parent.remove_widget(self.navButton)

	def cmdTarget(self, actionName):
		"""Recieves name property of the relevant CallableActions object 
			through submission at CommandsBox"""

		if not self.actionIsRunning:

			print(actionName) ### Montoring info
			self.managePrompts(actionName)

		else:
			self.displayErrorMsg("An actiom is already running. It must first reach completion.")

	def displayErrorMsg(self, msg):
		content = Label(text = msg)
		self.errorPopUp = Popup(title = "Error",
								size_hint = (0.6, 0.3),
								content = content)
		self.errorPopUp.open()

	def createPrompt(self, action):
		promptBox = PromptBox(action = action, 
									endTarget = self.promptEndTarget)
		self.promptPopUp = Popup(title = 'Values', 
								content = promptBox,
								size_hint = (0.6, 0.3),
								on_dismiss = self.onPromptDismiss)
		self.promptPopUp.open()

	def onPromptDismiss(self, *args):
		self.promptPopUp = None
		print("Dismissed") ### For Monitoring

	def managePrompts(self, actionName):
		if self.promptPopUp != None:
			self.promptPopUp.parent.remove_widget(self.promptPopUp)

		action = self.getActionFromName(actionName)

		if action != False: #If match found
			if action.prompts != []: # If values needed to be prompted for
				self.createPrompt(action)

			else: #Directly run the function that would be fired by a promptBox doing a submission
				self.promptEndTarget(actionName, {})

		else: # Error report in case an action match is not found for some reason
			print("Matching action not found!", actionName)			

class guiApp(App):
	def build(self):
		return Root()

guiApp().run()