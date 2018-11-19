from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.properties import BooleanProperty

from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle 

from colors import KeyToColor

class AltLabel(Label):
	"""		"""
	active = BooleanProperty(False)
	def __init__(self, **kwargs):
		self.instr = InstructionGroup()
		self.offColor = (1, 1, 1, 1)
		self.onColor = (0.8, 0.8, 0.8, 1)

		super(AltLabel, self).__init__(**kwargs)

		self.bold = False
		self.font_size = 14

		self.halign="left"
		self.valign="middle"

		self.size_hint=(1.0, None)

		self.color = (0, 0, 0, 1)
		self.canvas.before.add(self.instr)

	def on_active(self, *args):
		self.evaluateColor()

	def evaluateColor(self):
		if self.active:
			self.colorTuple = self.onColor

		else:
			self.colorTuple = self.offColor

		self.instr.clear()
		self.instr.add(Color(*self.colorTuple))
		self.instr.add(Rectangle(pos=self.pos, size=self.size))

	def on_size(self, *args):
		self.evaluateColor()

class ColorAwareLabel(Label):
	"""Uses the default KeyToColor Object and thus the default ColorColleciton object
		to automatically assign itself a background color depending on its text

		When the text is updated, so is the background color depending on how KeyToColor
		is configured

		Important Note: Do not pass text as keyword as the method to evaluate color uses
		properties that are defined after super is run, when super runs the evaluateColor
		method, they will be missing
		"""

	def __init__(self, **kwargs):
		super(ColorAwareLabel, self).__init__(**kwargs)

		self.colorRef = KeyToColor()
		self.bold = False
		self.font_size = 14

		self.colorTuple = self.colorRef.getColor(self.text)

		self.instr = InstructionGroup()
		self.canvas.before.add(self.instr)

	def evaluateColor(self):
		self.colorTuple = self.colorRef.getColor(self.text)

		self.instr.clear()
		self.instr.add(Color(*self.colorTuple))
		self.instr.add(Rectangle(pos=self.pos, size=self.size))

	def on_text(self, *args):
		self.evaluateColor()

	def on_size(self, *args):
		self.evaluateColor()

class HeaderLabel(Label):
	def __init__(self, **kwargs):
		super(HeaderLabel, self).__init__(**kwargs)

		# Customizing the visuals
		self.instr = InstructionGroup()
		self.canvas.before.add(self.instr)

		self.color = (1, 1, 1, 1) #Font color in the 0 to 1 scale

		self.bgColor_255 = (60,60,60,255) #BG color in the 0 to 255 scale

		#Using map to produce a tuple scale 0 to 1 from a tuple scaled 0 to 255
		self.bgColor_1 = tuple(list(map(lambda x: round(x/255, 3), self.bgColor_255)))

		self.bold = True
		self.font_size = 16

	def on_size(self, *args):
		self.instr.clear()

		self.instr.add(Color(*self.bgColor_1)) #BG
		self.instr.add(Rectangle(pos=self.pos, size=self.size))

class ScrollableLabel(ScrollView):
	"""Has a Label child which is controlled to ensure text wraps
		Since this class inherits from ScrollView, it ensures scrolling
		Text in the child is controlled by using get/setText methods

		Use when scrolling and wrapping is nexcessary 
		and lack of text centering is not a problem
	"""

	def __init__(self, **kwargs):
		super(ScrollableLabel, self).__init__(**kwargs)

		self.instr = InstructionGroup()
		self.canvas.before.add(self.instr)
	
		self.label = Label(size_hint=(1, None))
		self.add_widget(self.label)

		# self.colorTuple = (1,  1, 1, 1)

		# StackOverflow solution to ensure text wrapping
		self.label.bind(
			width=lambda *x: self.label.setter('text_size')(self.label, (self.label.width, None)),
			texture_size=lambda *x: self.label.setter('height')(self.label, self.label.texture_size[1]))

	# def evaluateColor(self):
	# 	self.instr.clear()
	# 	self.instr.add(Color(*self.colorTuple))
	# 	self.instr.add(Rectangle(pos=self.pos, size=self.size))

	# def on_size(self, *args):
	# 	self.evaluateColor()

	def setText(self, text):
		self.label.text = text
		# self.evaluateColor()

	def getText(self):
		return self.label.text
