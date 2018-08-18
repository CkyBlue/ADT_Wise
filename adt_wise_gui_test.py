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
			canvas.before:
				Color:
					rgba: 1,0.5,0,1
				Rectangle:
					size: self.size
					pos: self.pos
			Label:
				text: 'Overlay'
			BoxLayout:
	BoxLayout:
		BoxLayout:
			orientation: 'vertical'
			canvas.before:
				Color:
					rgba: 0.5,1,0.5,1
				Rectangle:
					size: self.size
					pos: self.pos
			Label:
				text: 'Cmds'
			BoxLayout:
				id: cmds
				Button:
					text: 'Make prompt'
					on_press: app.root.makePrompt()
		BoxLayout:
			canvas.before:
				Color:
					rgba: 0.75,0,0.5,1
				Rectangle:
					size: self.size
					pos: self.pos
			Label:
				text: 'Table'
			BoxLayout:
		BoxLayout:
			canvas.before:
				Color:
					rgba: 0,0.5,0.5,1
				Rectangle:
					size: self.size
					pos: self.pos
			Label:
				text: 'Pointer'
			BoxLayout:
	BoxLayout:
		canvas.before:
			Color:
				rgba: 0,0,1,1
			Rectangle:
				size: self.size
				pos: self.pos
		Label:
			text: 'Nav'
"""
Builder.load_string(kv)

class Prompt(BoxLayout):
	def __init__(self, **kwargs):
		self.cmdParamaters = kwargs["cmdParamaters"]
		self.orientation = "vertical"

		del kwargs["cmdParamaters"]

		super().__init__(**kwargs)
		self.base = App.get_running_app().root
		self.setUp()

	def setUp(self):
		self.add_widget(Label(text= "Prompt"))

		self.textFields = {}
		self.validators = {}
		self.parameterNames = [] 

		for param in self.cmdParamaters:
			b = BoxLayout()
			t = Label(text=param["promptMsg"])
			i = TextInput()

			name = param["valueName"]
			self.parameterNames.append(name)

			self.textFields[name] = i
			self.validators[name] = param["validator"]

			b.add_widget(t)
			b.add_widget(i)
			self.add_widget(b)
			
		self.add_widget(Button(text="Destruct",on_press=self.selfDestruct))

	def selfDestruct(self, *args):
		myDict = {}
		for param in self.parameterNames:
			myDict[param] = self.textFields[param].text
		self.base.doSomethingWithValue(**myDict)
		self.base.destroyPrompt(self)

class Root(BoxLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.promptLock = False
		self.adt = myQueue
		self.constructCommandsList()

	def constructCommandsList(self):
		self.ids.cmds.clear_widgets()

		listOfCmds = self.adt.calls
		self.cmds = list(map(lambda x: x.title(), listOfCmds)) # Mapping to set correct case

		for cmd in self.cmds:
			self.ids.cmds.add_widget(Button(text=cmd, on_press=self.makePrompt))		

	def doSomethingWithValue(self, **kwargs):
		print(kwargs)

	def destroyPrompt(self, prompt):
		self.ids.overlay.remove_widget(prompt)
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