### Document this

from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.lang import Builder

from dummys import dummyData, dummyADT

def target(actionName):
	print(actionName)

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

class Root(BoxLayout):
	def __init__(self, **kwargs):
		super(Root, self).__init__(**kwargs)
		self.add_widget(CommandsBox(actions = dummyADT.actions, target = target))

class MyApp(App):
	def build(self):
		return Root()

MyApp().run()