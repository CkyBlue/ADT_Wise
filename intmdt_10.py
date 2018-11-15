### Thoroughly Document this
### Should output an error message saying that an action is already running if it is

from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from kivy.lang import Builder

from dummys import dummyData, ADT
from boxes import ScrollableLabel, PromptBox, CommandsBox

from customs import DataTableColor

kv = """
"""

Builder.load_string(kv)

class UnlockButton(Button):
	"""Used with a CallableActions object,
		The function frozen using CallableActions periodically checks a lock Boolean
		CallableActions class's unlock method sets the Boolean 
		such that the frozen function can continue executing
		Initializes with a CallableActions object reference passed through the action keyword
	"""
	def __init__(self, **kwargs):
		self.action = kwargs["action"]
		del kwargs["action"]

		super(UnlockButton, self).__init__(**kwargs)

		self.text = "Next"
		self.bold = True

	def on_press(self, *args):
		self.action.unlock()

class Root(BoxLayout):
	"""The methods with target in their names are passed as callback functions
		The rest of their name gives information regarding what event they are associated with

		Manager functions (those with manage in their names) are controlled by target functions
		They contain the logic which controls decision making and control monitoring/control variables
		For eg, promptsManager checks if another prompt is already present and decides what to do if one is

		To nest and re-arrange child widgets, over-write build-internal and 
	"""
	def __init__(self, **kwargs):
		super(Root, self).__init__(**kwargs)

		self.promptPopUp = None
		self.adt = ADT(self.logTarget, self.actionEndTarget)

		self.buildInternal()

	def buildInternal(self):
		self.orientation = 'vertical'

		self.commandsBox = CommandsBox(actions = self.adt.actions,
			target = self.cmdTarget)
		self.add_widget(self.commandsBox)

		self.logBox = ScrollableLabel()
		self.add_widget(self.logBox)

		self.dataTable = DataTableColor(source = self.adt.data)
		self.add_widget(self.dataTable)

		self.actionIsRunning = False

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
			self.navManager()

		self.promptPopUp.dismiss()
		self.promptPopUp = None

	def navManager(self):
		"""If an action is not running, create a navButton (i.e UnlockButton)
			and set actionIsRunning to True
		"""

		if not self.actionIsRunning:
			self.action.executeAssociatedFunction(self.promptedValues)
			self.createNav()

			self.actionIsRunning = True

	def createNav(self):
		self.navButton = UnlockButton(action = self.action)
		self.add_widget(self.navButton)

	def logTarget(self, logTexts):
		self.dataTable.dataBox.updateContent()

		text = self.parse(logTexts)
		self.logBox.setText(text)

	def actionEndTarget(self):
		self.actionIsRunning = False
		self.dataTable.dataBox.updateContent()
		
		self.destroyNav()
		self.logBox.setText("")

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

			### Deploy a dismissable error message on the GUI			
			print("An actiom is already running. It must first reach completion.")

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

class MyApp(App):
	def build(self):
		return Root()

MyApp().run()