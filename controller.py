from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from boxes import PromptBox, CommandsBox, PseudoCodeBox, ScrollBox
from labels import ScrollableLabel

from actions import Unfreeze_Action_Button, PseudoCode
from customs import PointerBox, DataBoxColor

class Controller(BoxLayout):
	"""The methods with target in their names are used as callback functions
		The rest of their name gives information regarding what event they are associated with

		Manager functions (those with manage in their names) are controlled by target functions
		They contain the logic which controls decision making and control monitoring/control variables
		For eg, promptsManager checks if another prompt is already present and decides what to do if one is

		To nest and re-arrange child widgets, over-write build-internal

		Those methods that have '## Over-writable' written on top of them are probably the only one's
		you might need to overwrite after inheriting 

		The source keyword here does not take in an object but a class definition based on 
		the Operations class. The source property is then overwritten by an object created from the class

	"""
	def __init__(self, **kwargs):
		self.source = kwargs["source"]

		del kwargs["source"]
		super(Controller, self).__init__(**kwargs)

		self.promptPopUp = None
		self.navButton = None

		self.actionIsRunning = False
		self.pseudoCode = PseudoCode()

		self.source = self.source(lockCallBack = self.lockCallBack, 
		 					actionEndTarget = self.actionEndTarget)

		self.buildInternal()

	## Over-writable
	def buildInternal(self):
		self.orientation = 'vertical'

		self.commandsBox = CommandsBox(actions = self.source.actions,
			target = self.cmdTarget)
		self.add_widget(self.commandsBox)

		self.logBox = ScrollableLabel()
		self.add_widget(self.logBox)
		
		self.pseudoCodeBox = PseudoCodeBox(source = self.pseudoCode)
		self.pseudoCodeScrollBox = ScrollBox()
		self.pseudoCodeScrollBox.add_widget(self.pseudoCodeBox)
		self.add_widget(self.pseudoCodeScrollBox)

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

		for action in self.source.actions:
			if action.name == name:
				return action

		return False 

	def promptEndTarget(self, name, promptedValues):	
		self.action = self.getActionFromName(name)
		self.promptedValues = promptedValues

		if self.action != False:
			self.pseudoCode = self.action.codeObj

			#source needs to be re-linked because of the above overwriting
			self.pseudoCodeBox.source = self.pseudoCode 
			self.pseudoCodeBox.buildInternal()
			self.navManager()

		if self.promptPopUp != None:
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
		self.navButton = Unfreeze_Action_Button(action = self.action, endTarget = self.navEndTarget)
		self.add_widget(self.navButton)

	def navEndTarget(self):
		self.actionIsRunning = False

		if self.navButton != None:
			self.navButton = None

	## Over-writable
	def lockCallBack(self, logTexts):
		self.pseudoCodeBox.updateContent()

		text = self.parse(logTexts)
		self.logBox.setText(text)

	## Over-writable
	def actionEndTarget(self):
		self.actionIsRunning = False
		
		self.destroyNav()
		# self.logBox.setText("")

	def destroyNav(self):
		if not self.actionIsRunning and self.navButton != None:
			self.navButton.parent.remove_widget(self.navButton)
			self.navButton = None

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
			displayErrorMsg("Action '{}' not found!".format(actionName))			