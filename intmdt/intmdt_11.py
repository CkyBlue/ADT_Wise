### Document this

from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

from kivy.lang import Builder

from dummys import dummyData, dummyADT
from boxes import CommandsBox

def target(actionName):
	print(actionName)

class Root(BoxLayout):
	def __init__(self, **kwargs):
		super(Root, self).__init__(**kwargs)
		self.add_widget(CommandsBox(actions = dummyADT.actions, target = target))

class MyApp(App):
	def build(self):
		return Root()

MyApp().run()