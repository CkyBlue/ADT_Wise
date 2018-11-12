### Start putting things together with a controller
from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.lang import Builder

from dummys import dummyData, dummyADT
from boxes import ScrollableLabel, PromptBox

from customs import DataTableColor

kv = """
<Root>:
	BoxLayout:
	BoxLayout:
"""

Builder.load_string(kv)

class Root(BoxLayout):
	def __init__(self, **kwargs):
		super(Root, self).__init__(**kwargs)

class MyApp(App):
	def build(self):
		return Root()

MyApp().run()