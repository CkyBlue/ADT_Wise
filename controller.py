from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from boxes import PromptBox, CommandsBox, PseudoCodeBox, ScrollBox
from labels import ScrollableLabel, HeaderLabel
from customs import DataBoxColor, PointerBox, VariableBox, CustomCmdBox, PseudoBoxWithCount
from boxes import PromptBox, CommandsBox, ScrollBox
from actions import Unfreeze_Action_Button, PseudoCode

class Controller(BoxLayout):
	"""The controller relies on an Operations class based class 
		for the sources to data-driven objects (like boxes.DataBox which needs
		data.DataStructure to be passed through the source keyword during intialization)

		The buildInternal and doUpdate methods are the only ones you'd normally need to touch
		They need to be worked keeping in mind the source Operations class

		createNav may also need to be over-written to change where the unlocking button needs to be 
		generated

		The methods with target in their names are used as callback functions
		The rest of their name gives information regarding what event they are associated with

		Manager functions (those with manage in their names) are controlled by target functions
		They contain the logic which controls decision making and control monitoring/control variables
		For eg, promptsManager checks if another prompt is already present and decides what to do if one is

		To nest and re-arrange child widgets, over-write build-internal

		Base Controller can accept base Operations

		Those methods that have '## Over-writable' written on top of them are probably the only one's
		you might need to overwrite after inheriting 
	"""
	def __init__(self, **kwargs):
		self.source = kwargs["source"]

		del kwargs["source"]
		super(Controller, self).__init__(**kwargs)

		self.promptPopUp = None
		self.navButton = None

		self.actionIsRunning = False
		self.pseudoCode = PseudoCode()

		# lockCallBack recieves the logtexts array and runs everytime lock is hit
		# actionEndTarget is run when action ends

		self.source = self.source(lockCallBack = self.lockCallBack, 
		 					actionEndTarget = self.actionEndTarget)

		self.buildInternal()

	## Over-writable
	def doUpdates(self):
		"""Update methods that keeps the view synchronized with the data"""
		self.pseudoCodeBox.updateContent()

	## Over-writable
	def buildInternal(self):
		"""This method controls what boxes are used in the GUI and
			how they are arranged. References to those boxes can 
			be used in the doUpdates method to ensure the boxes 
			update with changes to their source data.

			Overwrite to customize visuals

			Since self.pseudoCodeBox is used in a number of other 
			methods, do not forget to create this reference to
			a PseudoCodeBox based object"""
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

	#Over-writable
	def createNav(self):
		self.navButton = Unfreeze_Action_Button(action = self.action, 
			endTarget = self.navEndTarget)
		self.add_widget(self.navButton)

	def navEndTarget(self):
		self.actionIsRunning = False

		if self.navButton != None:
			self.navButton = None

	def lockCallBack(self, logTexts):
		self.doUpdates()

		text = self.parse(logTexts)
		self.logBox.setText(text)

	def actionEndTarget(self):
		self.actionIsRunning = False
		self.doUpdates()
		
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

class CustomController(Controller):

	def buildInternal(self):
		self.orientation = 'vertical'

		self.allCmds = BoxLayout()
		self.allCmds.size_hint_y = 0.5
		self.commandsBox = CustomCmdBox(actions = self.source.actions,
			target = self.cmdTarget)
		self.allCmds.add_widget(self.makeTitled("Commands", self.makeScroll(self.commandsBox)))
		self.add_widget(self.allCmds)

		explanations = BoxLayout()

		self.logBox = ScrollableLabel()
		self.logScroll = self.makeTitled("Explanations", self.logBox)
		self.logScroll.size_hint_x = 0.6
		explanations.add_widget(self.logScroll)

		self.pseudoCodeBox = PseudoBoxWithCount(source = self.pseudoCode)
		explanations.add_widget(self.makeTitled("Pseudocode", self.makeScroll(self.pseudoCodeBox)))

		self.add_widget(explanations)

		data = BoxLayout()

		self.dataTable = DataBoxColor(source = self.source.data)
		data.add_widget(self.makeTitled("Data", self.makeScroll(self.dataTable)))

		variables = BoxLayout()

		self.variableBox = VariableBox(source = self.source.variables)
		variables.add_widget(self.makeTitled("Variables", self.makeScroll(self.variableBox)))

		self.pointerBox = PointerBox(source = self.source.pointers)
		variables.add_widget(self.makeTitled("Pointers", self.makeScroll(self.pointerBox)))

		data.add_widget(variables)

		self.add_widget(data)

	def makeTitled(self, title, box):
		b = BoxLayout(padding = "2px", spacing = "2px", orientation = "vertical")

		h = HeaderLabel(size_hint_y = None, height = "40px")
		h.text = title

		b.add_widget(h)
		b.add_widget(box)

		return b

	def makeScroll(self, box):
		s = ScrollBox()
		s.add_widget(box)
		return s

	def createNav(self):
		self.navButton = Unfreeze_Action_Button(action = self.action,
			endTarget = self.navEndTarget,
			size_hint = (0.3, 1))
		self.allCmds.add_widget(self.navButton)

	def doUpdates(self):
		self.variableBox.updateContent()
		self.pointerBox.updateContent()
		self.dataTable.updateContent()
		self.pseudoCodeBox.updateContent()