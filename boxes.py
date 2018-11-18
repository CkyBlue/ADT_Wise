"""Contains container classes,
Refer to their individual docstrings for more information"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle 

from labels import ColorAwareLabel, AltLabel, HeaderLabel
from data import DataStructure

class DataBox(BoxLayout):
	"""Takes a DataStructure object as parameter through the source keyword
		Develops a mirror object to track the label associated with each data item
		updateContent method reads the source DataStructure again and updates the label contents
	"""
	def __init__(self, **kwargs):
		# The DataStructure object to be used for as the source of data
		self.source = kwargs["source"]

		del kwargs["source"]
		super(DataBox, self).__init__(**kwargs)

		# A DataStructure object which mirrors self.source but stores Label widgets corresponding
		# to each data item in the source at the matching key and index position
		self.dataStructure = DataStructure(list(self.source.keys), size = self.source.size, name = "Mirror")

		self.orientation = 'vertical'

		self.buildInternal()

	def buildInternal(self):

		# Produces the labels that populate self.dataStructure 
		for i in range(self.source.size):
			b = BoxLayout()

			for key in self.source.keys:

				value = self.source.getValue(key, i)
				l = Label(text = str(value))
				self.dataStructure.setValue(key, i, l)
				b.add_widget(l)
				
			self.add_widget(b)

	def updateContent(self):
		#The controller should run this through the logTarget function which is 
		# called by the CallableActions object with each freeze

		# Updates the labels accessed through self.dataStructure using the data from the source
		for i in range(self.source.size):

			for key in self.source.keys:

				value = self.source.getValue(key, i)
				l = self.dataStructure.getValue(key, i)
				
				l.text = str(value)

class PromptBox(BoxLayout):
	"""Widget which requires a CallableActions object in the keyword parameter action
		Fire the buildInternal method to set up the inputs and the submit button
		Submit validates inputs, then generates error messages, or removes widget and 
		feeds inputs to the function controlled by CallableActions object

		Is divided into two Boxes: self.formArea (for inputs and the submit button)
		and self.msgArea (for error messages)

		###Consider building so that the msgArea Box is hidden and shown as appropriate
	"""
	def __init__(self, **kwargs):
		self.action = kwargs["action"]
		del kwargs["action"]

		self.endTarget = kwargs["endTarget"]
		del kwargs["endTarget"]

		super(PromptBox, self).__init__(**kwargs)
		self.clear_widgets()
		self.orientation = 'vertical'

		self.formArea = BoxLayout()
		self.msgArea = BoxLayout(size_hint_y=0.5, orientation='vertical')

		self.add_widget(self.formArea)
		self.add_widget(self.msgArea)

		self.buildInternal() # CallableActions object

	def buildInternal(self):
		self.textInputs = {} #Key is the valueName assoicated with the input
		self.validators= {} #Same

		for prompt in self.action.prompts:
			# For each parameter, create a new box layout b
			b = BoxLayout()

			# Create label and input field for the box
			t = Label(text=prompt.promptMsg)
			i = TextInput()

			# Get valueName to use as key to access from dictionaries associated textInputs and validators 
			name = prompt.valueName
			self.textInputs[name] = i
			self.validators[name] = prompt.validatorFunc

			b.add_widget(t)
			b.add_widget(i)

			self.formArea.add_widget(b)
		
		# Submit button destroys prompt if it is filled properly	
		self.formArea.add_widget(Button(text="Submit", on_press=self.submitInputs))

	def displayErrors(self, listOfErrors):
		self.msgArea.clear_widgets()

		for error in listOfErrors:
			t = Label(text=error)
			self.msgArea.add_widget(t)

	def submitInputs(self, *arg):

		values = {} #Key is the valueName assoicated with the input

		for valueName, textInput in self.textInputs.items():

			value = textInput.text #Get text from the textInput widget associated with the valueName
			validator = self.validators[valueName]
			valid = validator(value)

		noErrors = True
		errorMessages = []

		for valueName, textInput in self.textInputs.items():

			value = textInput.text #Get text from the textInput widget associated with the valueName
			validator = self.validators[valueName]

			# validator returns True or error message if input is invalid
			valid = validator(value)

			if valid == True:
				values[valueName] = value

			else:
				noErrors = False
				errorMsgReturnedByValidator = valid
				errorMessages.append(errorMsgReturnedByValidator)

		if noErrors:
			self.endTarget(self.action.name, values)
			self.parent.remove_widget(self)

		else:
			self.displayErrors(errorMessages)

class CommandsBox(BoxLayout):
	"""Requires 2 keyword arguments: actions and target
		actions is the list of CallableActions objects that should populate the CommandBox
		target is the function to which the name of the CallableActions object to be used is passed
		For display purposes, the name string is title cased,
		The name sent to target is lowercase since the CallableActions class def ensures a lowercase name
	"""
	def __init__(self, **kwargs):
		self.actions = kwargs["actions"]
		del kwargs["actions"]

		self.target = kwargs["target"]
		del kwargs["target"]

		super(CommandsBox, self).__init__(**kwargs)

		self.orientation = 'vertical'

		self.buildInternal()

	def buildInternal(self):
		for action in self.actions:
			b = Button(text = action.name.title(), on_press = self.submitCmd)
			self.add_widget(b)

	def submitCmd(self, source):
		"""Function which sends the target function the name of the relevant CallableActions object
		after fetching the title cased version from the buttons text and turning it to lowercase"""
		self.target(source.text.lower())

class PseudoCodeBox(BoxLayout):
	"""This box uses a PseudoCode object for a source, the source is passed through the
		source keyword at initialization. The buildInternal method of this box differs from
		that of most other boxes in that it was designed to allow resconstruction from a new source.
		This is so that the same box can display pseudoCode for numerous different actions.

		The PseudoCode object passed is usually controlled by a CallableActions object"""
	def __init__(self, **kwargs):
		self.source = kwargs["source"]

		del kwargs["source"]
		super(PseudoCodeBox, self).__init__(**kwargs)

		self.labels = []
		self.orientation = 'vertical'

		self.buildInternal()

	def buildInternal(self):
		self.clear_widgets()
		for statement in self.source.statements:

			l = AltLabel()
			l.text = statement["statement"]
			l.active = statement["activity"]

			self.labels.append(l)	
			self.add_widget(l)

	def updateContent(self):
		for index in range(len(self.labels)):

			self.labels[index].active = self.source.statements[index]["activity"]