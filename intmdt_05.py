###Create a base ColorAwareLabel with pre-defined ColorCollection
### Add documentation
from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.lang import Builder

from colors import ColorAwareLabel

class Root(BoxLayout):
	def __init__(self, **kwargs):
		super(Root, self).__init__(**kwargs)

		self.l = ColorAwareLabel()
		self.add_widget(self.l)
		self.l.text = "-2"

		self.add_widget(Button(on_press= self.edit))

	def edit(self, arg):
		self.l.text = str(int(self.l.text)+1)

class MyApp(App):
	def build(self):
		return Root()

kv = """
<Root>:
	ColorAwareLabel: 
		id: lbl
		text: '1'
	Button:
		text: "Click me"
		on_press: lbl.text = 'red' 
"""

# Builder.load_string(kv)

MyApp().run()