from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle 

from colors import ColorAwareLabel, HeaderLabel
from dummys import dummyADT
from customs import PointerBox

ADT = dummyADT()

class TestApp(App):
	def build(self):
		return Root()

class Root(BoxLayout):
	def __init__(self, **kwargs):
		super(Root, self).__init__(**kwargs)
		self.add_widget(PointerBox(source = ADT.pointers))

	### Move controlling functions to a contained Controller object

TestApp().run()