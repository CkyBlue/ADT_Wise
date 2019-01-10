### Add documentation to this!
### Contain DataBoxColor in a ScrollView object which has the same BG color
### Create something similar to DataStructures and DataBoxColor for pointers

from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.lang import Builder

from actions import Prompts, CallableActions
from data import DataStructure

from dummys import dummyData

from customs import DataTableColor

def editData(arg):
	for i in range(12):
		dummyData.setValue("ID", i, str(i - 1))
		dummyData.setValue("Value", i, "Hari" + str(i))
		dummyData.setValue("Pointer", i, str(i))

		theContent.updateContent()

class myApp(App):
	def build(self):
		return DataTableColor(source = dummyData)

myApp().run()