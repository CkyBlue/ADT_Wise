from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout 

kv = """
<Sub>:
	Button:
		text: "Press"
		on_press: print(app.root)
"""

Builder.load_string(kv)

class Sub(BoxLayout):
	pass

class Root(BoxLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.add_widget(Sub())

class myApp(App):
	def build(self):
		return Root()

myApp().run()