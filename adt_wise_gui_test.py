### Develop a convention for tracking widgets and comments

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button

from adt_queue import Queue

myQueue = Queue("Micro", 12)

"""To Do:
Set up validation for prompt destruct
"""

"""Heirarchy reference
<Root>
	<Overlay>
		<Prompt>
		<Description>

	<Inteface>
		<Commands Box>
			<Commmands>
		<Table Box>
			<Table>
		<Pointer box>
			<Pointers>

	<Nav Box>
"""

kv = """
<Root>:
	orientation: "vertical"
	BoxLayout:
		id: overlay
		BoxLayout:
			id: prompt
			canvas.before:
				Color:
					rgba: 0.5,0.5,0.5,1
				Rectangle:
					size: self.size
					pos: self.pos
			Label:
				text: 'Prompt'
			BoxLayout:
		BoxLayout:
			id: description
			canvas.before:
				Color:
					rgba: 1,0.5,0,1
				Rectangle:
					size: self.size
					pos: self.pos
			Label:
				text: 'Description'
			BoxLayout:
	BoxLayout:
		id: interface
		BoxLayout:
			id: commands_box
			orientation: 'vertical'
			canvas.before:
				Color:
					rgba: 0.5,1,0.5,1
				Rectangle:
					size: self.size
					pos: self.pos
			Label:
				text: 'Commands Box'
			BoxLayout:
				id: cmds
				Button:
					text: 'Make prompt'
					on_press: app.root.makePrompt()
		BoxLayout:
			id: table_box
			canvas.before:
				Color:
					rgba: 0.75,0,0.5,1
				Rectangle:
					size: self.size
					pos: self.pos
			Label:
				text: 'Table'
			BoxLayout:
				id: table
		BoxLayout:
			id: pointer_box
			canvas.before:
				Color:
					rgba: 0,0.5,0.5,1
				Rectangle:
					size: self.size
					pos: self.pos
			Label:
				text: 'Pointer'
			BoxLayout:
				id: pointers
	BoxLayout:
		id: nav_box
		canvas.before:
			Color:
				rgba: 0,0,1,1
			Rectangle:
				size: self.size
				pos: self.pos
		Label:
			text: 'Nav'
		Button:
			text: 'Next'
"""
Builder.load_string(kv)

class Prompt(BoxLayout):
	def __init__(self, **kwargs):
		# Fetch values needed for prompt
		self.cmdParamaters = kwargs["cmdParamaters"]
		self.orientation = "vertical"

		del kwargs["cmdParamaters"]

		super().__init__(**kwargs)
		self.base = App.get_running_app().root
		self.setUp()

	def setUp(self):
		self.add_widget(Label(text= "Prompt"))

		# Store references to textInput widgets, validator funcs and parmeter names
		self.textFields = {}
		self.validators = {}
		self.parameterNames = [] 

		for param in self.cmdParamaters:
			# For each parameter, create a new box layout b
			b = BoxLayout()

			# Create label and input field for the box
			t = Label(text=param["promptMsg"])
			i = TextInput()

			# parameterName array tracks the names of the various fields, eg: ID, Data
			name = param["valueName"]
			self.parameterNames.append(name)

			# store regerences to textInput, key is parameter name
			self.textFields[name] = i

			# stores validator function, key is parameter name
			self.validators[name] = param["validator"]

			b.add_widget(t)
			b.add_widget(i)
			self.add_widget(b)
		
		# Submit button destroys prompt if it is filled properly	
		self.add_widget(Button(text="Destruct",on_press=self.selfDestruct))

	# Destroy prompt if submission is successful
	def selfDestruct(self, *args):

		#Stores values that need to be sent to the ADT for processing if submit is successful
		myDict = {}

		# For each field, i.e item in parameterNames
		for param in self.parameterNames:

			# Get data from textInput
			myDict[param] = self.textFields[param].text

			### Add validation using validator functions

		### If validation successful, only then send data to root
		### Else, find a way to display error message

		self.base.doSomethingWithValue(**myDict)
		self.base.destroyPrompt(self)

class Root(BoxLayout):
	def __init__(self, **kwargs):
		super(Root, self).__init__(**kwargs)
		self.promptLock = False
		self.adt = myQueue

		# Reads commands available to an ADT and appropriately constructs list
		self.constructCommandsList()

	def constructCommandsList(self):
		self.ids.cmds.clear_widgets()

		# Fetch commands
		listOfCmds = self.adt.calls
		self.cmds = list(map(lambda x: x.title(), listOfCmds)) # Mapping to set correct case

		# For each command fetched, create an new button
		### Later on create a new button class with behavior built in
		for cmd in self.cmds:
			self.ids.cmds.add_widget(Button(text=cmd, on_press=self.makePrompt))		

	# When values prompted for are validated and sent, this is run

	### Should alter data 
	def doSomethingWithValue(self, **kwargs):
		print(kwargs)

	def destroyPrompt(self, prompt):
		# The parent to prompt is 'Overlay' so the prompt widget is deleted from there
		self.ids.overlay.remove_widget(prompt)

		# 
		self.promptLock = False
		
	def makePrompt(self, wid):
		cmd = wid.text.lower()

		dictOfCmdToParam = self.adt.getInputPrompts()
		cmdParamaters = dictOfCmdToParam[cmd]

		if not self.promptLock:
			self.prompt = Prompt(cmdParamaters = cmdParamaters)
			self.ids.overlay.add_widget(self.prompt)
			self.promptLock = True

class myApp(App):
	def build(self):
		return Root()

myApp().run()