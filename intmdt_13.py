from kivy.app import App

from controller import Controller
from dummys import dummyADT

class dummyController(Controller):
	pass

newDummy = dummyController(source = dummyADT)

class guiApp(App):
	def build(self):
		return newDummy

guiApp().run()