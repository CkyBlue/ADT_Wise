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

from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle 

from colors import ColorAwareLabel, HeaderLabel
from data import PointerData
from boxes import DataBox

from kivy.lang import Builder

kv = """
"""

text = """DO A
DO B
DO C
DO D
"""

class PseudoCode:
	def __init__(self):
		""""A list of strings, each string is a seperate line,	the list is prepared by the extract method
			One additional 0 index entry is added in the beginning of the statements fetched by extract.
			This is to indicate invalid attempts to change statement activity
			For eg, if indices go upto 15 statements and someone attempts to change activity
			for index 17, the change shows for index 0
			Activity means on or off, active statements are those that
			are highlighted, each entry in the statements has an on or off propertry associated with it

			The additional 0 index entry also ensures that the line-numbers that show up in text-editors
			for the pseudocode text which start from 1 match the statement's index here

			Index 0 cannot be made active like the other indices can be since it is an error flag

			Activate means set activity to True for corresponding entry
			"""

		# Each entry is going to be a dictionary with the keys 'statement' and 'activity'
		self.statements = [{"statement": "", "activity": False}] # Index 0 that is automatically added
		self.length = 1

	def extract(self, text):
		statements = text.split("\n")

		# Overwrite
		self.statements = [{"statement": "", "activity": False}] # Index 0 that is automatically added
		self.length = 1

		for statement in statements:
			self.length += 1
			self.statements.append({"statement": statement, "activity": False})

	def highlight(self, indices):
		# Parameter indices is a list of index values for which statements need to be highlighted

		for index in indices: # For each index
			if str(index).isdigit(): # If it is a number value
				self.activate(int(index)) # Try to activate it

	def activate(self, index):
		# Activate the entry at a particular index
		if index > self.length - 1: # If index invalid
			self.statements[0]["activity"] = True

		else:
			if index != 0: # If index is not 0, only then set is as active
				self.statements[index]["activity"] = True

class AltLabel(BoxLayout):
	"""		"""
	active = BooleanProperty(False)
	def __init__(self, **kwargs):
		super(AltLabel, self).__init__(**kwargs)

		self.onColor = (1, 0, 0, 1)
		self.offColor = (0, 1, 0, 1)

		self.bold = False
		self.font_size = 14

		self.instr = InstructionGroup()
		self.canvas.before.add(self.instr)

	def on_active(self, *args):
		self.evaluateColor()

	def evaluateColor(self):
		print("Evaluating")
		if self.active:
			self.colorTuple = self.onColor

		else:
			self.colorTuple = self.offColor

		self.instr.clear()
		self.instr.add(Color(*self.colorTuple))
		self.instr.add(Rectangle(pos=self.pos, size=self.size))

	def on_size(self, *args):
		self.evaluateColor()

class Root(BoxLayout):
	def __init__(self, **kwargs):
		super(Root, self).__init__(**kwargs)

		self.alt = AltLabel()

		self.btn = Button(on_press = self.func)

		self.add_widget(self.alt)
		self.add_widget(self.btn)

	def func(self, *args):
		print("Running")
		print(self.alt.active)
		self.alt.active = not self.alt.active

Builder.load_string(kv)

ps = PseudoCode()
ps.extract(text)
ps.highlight()
print(ps.statements)

class pseudoApp(App):
	def build(self):
		return Root()

pseudoApp().run()
