from kivy.app import App
from kivy.lang import Builder

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout 
from kivy.uix.widget import Widget

from kivy.properties import ListProperty, StringProperty, DictProperty

# ADT
from adt_queue import Queue
myQueue = Queue("Micro", 5)

for i in range(5):
	myQueue.insert(chr(i + ord("a")))

# Root
	#Tabulation
		# Prompt
		# Overlay
		# Content
			# DataTable
			# Pointer

	# Controller

kv = """
<Tabulation>:
	Button:
		text: "Press"
		on_press: app.setUp()
	Content:
		id: content
	Prompt:
		id: prompt
"""
Builder.load_string(kv)

class Prompt(FloatLayout):
	pass

class Controller():
	def __init__(self, model):
		self.model = model

class DataTable(BoxLayout):
	pass

class PointerTable(BoxLayout):
	pass

class adtWiseGUIApp(App):
	def build(self):
		return Tabulation()

	def setUp(self):
		myModel = Model(adt = myQueue)

		myModel.buildData()
		print(myModel.data)

		myModel.updataData()
		print(myModel.data)

class Content(FloatLayout):
	def buildSet(self, controller):
		self.controller = controller
		self.adt = self.controller.adt

		nodes = self.adt.noOfNodes
		items = self.adt.dataItems

		funcs = self.adt.dataItemsRetrievingFunc

		for i in range(nodes):
			values = [i]
			for j in items:
				values.append(funcs[j](i))

			l = Row(itemsToFeed = values)
			self.add_widget(l)

class Tabulation(BoxLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.content = self.ids.content
		self.prompt = self.ids.prompt

		self.app = App.get_running_app()

	def setController(self, controller):
		self.controller = controller

		self.content.buildSet(self.controller)

class Row(BoxLayout):
	def __init__(self, **kwargs):
		items = kwargs["itemsToFeed"]
		del kwargs["itemsToFeed"]

		super().__init__(**kwargs)
		# print(kwargs[itemsToFeed])

		for item in items:
			self.add_widget(Label(text=str(item)))

class Model(Widget):
	data = DictProperty()

	def __init__(self, **kwargs):
		self.adt = kwargs["adt"]
		del kwargs["adt"]

		super().__init__(**kwargs)

		self.numberOfNodes = self.adt.numberOfNodes
		print(self.data)

	def buildData(self):
		# Constructs dictionary holding data as
		# {<Header-name>: [<value-1, value-2,>]}

		for header in self.adt.dataItems:

			self.data[header] = []

			for index in range(self.numberOfNodes):
				self.data[header].append("")

		self.data["Index"] = []

		for index in range(self.numberOfNodes):
			self.data["Index"].append(index)		

	def updataData(self):
		
		for header in self.adt.dataItems:

			func = self.adt.dataItemsRetrievingFunc[header]
			
			tempList = []
			for index in range(self.numberOfNodes):
				tempList.append(func(index))

			self.data[header] = tempList

def constructTabulation():
	pass

if __name__ == "__main__":
	adtWiseGUIApp().run()

