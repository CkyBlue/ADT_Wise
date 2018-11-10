###Create a base LabelB with pre-defined ColorCollection
### Add documentation
from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.lang import Builder
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle 

from colors import ColorCollection

class CodeToColor:
	"""To bring to use, inherit and redefine the self.colors property
		keys must be totally lowercase strings, values must be a rgba tuple: (r, g, b, a)
	"""
	def __init__(self):
		### With its own default, set it to map keys like '1' to colors through a loop'
		### Allow reading ColorCollection's self.color's length and fetching with index
		self.colorCollection = ColorCollection()
		self.mapping = {}
		self.default = "-1"

		self.setMapping()

	def setMapping(self):
		# Get a sorted lt of possible colors
		colorKeys = list(self.colorCollection.colors.keys())
		colorKeys.sort()
		length = len(colorKeys)

		count = -1
		for i in range(length):
			self.mapping[str(count)] = self.colorCollection.get_1(colorKeys[i])
			count += 1

		print(self.mapping)

	def getColor(self, key):
		"""Produces a color tuple (r, g, b, a) with values on a 0 to 1 scale based on input key"""

		# Case and int is not a problem 
		key = str(key).lower()

		# If key is recognized
		if key in list(self.mapping.keys()):
			return self.mapping[key]

		else:
			return self.mapping[self.default]

class LabelB(Label):
	def __init__(self, **kwargs):
		super(LabelB, self).__init__(**kwargs)
		self.colorRef = CodeToColor()

		self.instr = InstructionGroup()
		self.canvas.before.add(self.instr)

	def evaluateColor(self):
		self.instr.clear()
		self.instr.add(Color(*self.colorRef.getColor(self.text)))
		self.instr.add(Rectangle(pos=self.pos, size=self.size))

	def on_text(self, *args):
		self.evaluateColor()

	def on_size(self, *args):
		self.evaluateColor()

class Root(BoxLayout):
	def __init__(self, **kwargs):
		super(Root, self).__init__(**kwargs)

		self.l = LabelB()
		self.add_widget(self.l)
		self.l.text = "1"

		self.add_widget(Button(on_press= self.edit))

	def edit(self, arg):
		self.l.text = "4"

class MyApp(App):
	def build(self):
		return Root()

kv = """
<Root>:
	LabelB: 
		id: lbl
		text: '1'
	Button:
		text: "Click me"
		on_press: lbl.text = 'red' 
"""

# Builder.load_string(kv)

MyApp().run()