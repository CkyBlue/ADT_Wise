### Add documentation to this!

from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.lang import Builder

from actions import Prompts, CallableActions
from data import DataStructure, dummyData
from boxes import DataBox

class DataBoxColor(DataBox):
	def __init__(self, **kwargs):
		super(DataBoxColor, self).__init__(**kwargs)

	def buildInternal(self):
		# Produces the labels that populate self.dataStructure 
		for i in range(self.source.size):
			b = BoxLayout()

			for key in self.source.keys:

				value = self.source.getValue(key, i)
				l = Label(text = value, )
				self.dataStructure.setValue(key, i, l)
				b.add_widget(l)
				
			self.add_widget(b)

def editData(arg):
	for i in range(12):
		dummyData.setValue("ID", i, str(i))
		dummyData.setValue("Value", i, "Hari" + str(i))
		dummyData.setValue("Pointer", i, str(i + 1))

		theContent.updateContent()

theContent = DataBox(source = dummyData)

class Root(BoxLayout):
	def __init__(self, **kwargs):
		super(Root, self).__init__(**kwargs)

		self.add_widget(theContent)
		self.add_widget(Button(on_press= editData))		

class myApp(App):
	def build(self):
		return Root()

myApp().run()