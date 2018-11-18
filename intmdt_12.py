"""Create an object that can read a doc string and maintain information regarding what lines are active
A BoxObject will read it and update with it, The object needs to be passed into the CallabelActions
object where it will be modified (resetin completion) and read

The box will have each line with
its own AltLabel. Test controlling that with a method which accepts lines"""

from kivy.app import App

from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.properties import BooleanProperty

from labels import ColorAwareLabel, HeaderLabel
from data import PointerData
from boxes import DataBox, PseudoCodeBox
from pseudo import PseudoCode

from kivy.lang import Builder

kv = """
"""

text = """DO A
DO B
DO C
DO D
"""

p = PseudoCode()
p.extract(text)

class Root(BoxLayout):
	def __init__(self, **kwargs):
		super(Root, self).__init__(**kwargs)

		self.pseudo = PseudoCodeBox(source = p)

		self.btn = Button(on_press = self.func)

		self.add_widget(self.pseudo)
		self.add_widget(self.btn)

	def func(self, *args):
		p.highlight([1, 2, 3])
		self.pseudo.updateContent()

Builder.load_string(kv)



class pseudoApp(App):
	def build(self):
		return Root()

pseudoApp().run()
