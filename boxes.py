"""Contains container classes,
Refer to their individual docstrings for more information"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle 

from colors import ColorAwareLabel
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
		self.dataStructure = DataStructure(*self.source.keys, size = self.source.size, name = "Mirror")

		self.orientation = 'vertical'

		self.buildInternal()

	def buildInternal(self):

		# Produces the labels that populate self.dataStructure 
		for i in range(self.source.size):
			b = BoxLayout()

			for key in self.source.keys:

				value = self.source.getValue(key, i)
				l = Label(text = value)
				self.dataStructure.setValue(key, i, l)
				b.add_widget(l)
				
			self.add_widget(b)

	def updateContent(self):
		### The controller should run this through the logTarget function which is 
		### called by the CallableActions object with each freeze

		# Updates the labels accessed through self.dataStructure using the data from the source
		for i in range(self.source.size):

			for key in self.source.keys:

				value = self.source.getValue(key, i)
				l = self.dataStructure.getValue(key, i)
				l.text = value

class PromptBox(BoxLayout):
	"""Widget which requires a CallableActions object in the keyword parameter action
		Fire the buildInternal method to set up the inputs and the submit button
		Submit validates inputs, then generates error messages, or removes widget and 
		feeds inputs to the function controlled by CallableActions object
	"""
	def __init__(self, **kwargs):
		self.action = kwargs["action"]
		del kwargs["action"]

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
			self.action.executeAssociatedFunction(values)
			self.parent.remove_widget(self)

		else:
			self.displayErrors(errorMessages)

class ScrollableLabel(ScrollView):
	"""Has a Label child which is controlled to ensure text wraps
		Since this class inherits from ScrollView, it ensures scrolling
		Text in the child is controlled by using get/setText methods

		Use when scrolling and wrapping is nexcessary 
		and lack of text centering is not a problem
	"""

	def __init__(self, **kwargs):
		super(ScrollableLabel, self).__init__(**kwargs)

		self.instr = InstructionGroup()
		self.canvas.before.add(self.instr)
	
		self.label = Label(size_hint=(1, None))
		self.add_widget(self.label)

		# self.colorTuple = (1,  1, 1, 1)

		# StackOverflow solution to ensure text wrapping
		self.label.bind(
			width=lambda *x: self.label.setter('text_size')(self.label, (self.label.width, None)),
			texture_size=lambda *x: self.label.setter('height')(self.label, self.label.texture_size[1]))

	# def evaluateColor(self):
	# 	self.instr.clear()
	# 	self.instr.add(Color(*self.colorTuple))
	# 	self.instr.add(Rectangle(pos=self.pos, size=self.size))

	# def on_size(self, *args):
	# 	self.evaluateColor()

	def setText(self, text):
		self.label.text = text
		# self.evaluateColor()

	def getText(self):
		return self.label.text

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
		self.target(source.text.lower())