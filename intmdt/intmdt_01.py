### Add documentation

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder

from actions import Prompts, CallableActions

def parse(log):
	"""Takes a list and gives a string where the items are indivisual statements"""

	content = ""

	for statement in log:
		content += statement + "\n"

	return content

def dummyInsert(itemToBeInserted, idToBeInserted, lock, log):
	print(itemToBeInserted, idToBeInserted)

def dummyValidator(data):
	if data:
		return True
	else:
		return "Error Message"


class CommandsBox(BoxLayout):
	def __init__(self, **kwargs):
		super(CommandsBox, self).__init__(**kwargs)
		self.clear_widgets()

		self.buttonArea = BoxLayout()
		self.add_widget(self.buttonArea)

	def buildInternal(self, allActions): #List of CallableActions objects
		for action in allActions:
			pass

class PromptDevApp(App):
	def build(self):
		return Root()

# Define within ADT
insertAction = CallableActions("insert", dummyInsert, lambda x: print(parse(x)))

insertAction.addPrompt(Prompts("itemToBeInserted", "Enter item to be inserted", dummyValidator))
insertAction.addPrompt(Prompts("idToBeInserted", "Enter id to be inserted", dummyValidator))
# --

class Root(BoxLayout):
	def __init__(self, **kwargs):
		super(Root, self).__init__(**kwargs)
		self.add_widget(PromptBox(action = insertAction))

	### Move controlling functions to a contained Controller object

PromptDevApp().run()
