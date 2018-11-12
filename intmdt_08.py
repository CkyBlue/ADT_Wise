from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button

class Root(ScrollView):
	def __init__(self, **kwargs):
		super(Root, self).__init__(**kwargs)
		label = Label(text=text, size_hint=(1, None))

		# StackOverflow solution to ensure text wrapping and scrolling
		label.bind(
			width=lambda *x: label.setter('text_size')(label, (label.width, None)),
			texture_size=lambda *x: label.setter('height')(label, label.texture_size[1]))
		self.add_widget(label)

class MyApp(App):
	def build(self):
		return Root()


MyApp().run()