from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button

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
			canvas.before:
				Color:
					rgba: 0.5,1,0.5,1
				Rectangle:
					size: self.size
					pos: self.pos
			Label:
				text: 'Cmds'
			BoxLayout:
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
		super().__init__(**kwargs)
		self.base = App.get_running_app().root
		self.add_widget(Label(text= "Prompt"))
		self.valNames = ["Id", "Item"]
		self.vals = {"Id": TextInput(), "Item": TextInput()}
		for valName in self.valNames:
			self.add_widget(self.vals[valName])
		self.add_widget(Button(text="Destruct",on_press=self.selfDestruct))

	def selfDestruct(self, *args):
		myDict = {}
		for valName in self.valNames:
			myDict[valName] = self.vals[valName].text
		self.base.doSomethingWithValue(**myDict)


class Root(BoxLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.promptLock = False

	def doSomethingWithValue(self, **kwargs):
		print(kwargs)
		self.ids.overlay.remove_widget(self.prompt)

	def makePrompt(self):
		if not self.promptLock:
			self.prompt = Prompt()
			self.ids.overlay.add_widget(self.prompt)
			self.promptLock = True

class myApp(App):
	def build(self):
		return Root()

myApp().run()