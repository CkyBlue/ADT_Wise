"""Contains the classes
used to produce the color related behaviors of the program

Refer to their individual docstrings for more information"""
from kivy.uix.label import Label

from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle 

class ColorCollection:
	"""The self.colors property is dictionary with standard color names serving keys
		and rgba values at a scale of 0 to 255 in a (r, g, b, a) tuple serving as values

		ColorAwareLabel and KeyToColor classes are designed to work with these
		colors in an automatically updating fashion

		If new colors are added, the integer value upto which there are distinct colors increases
		automatically

		The self.default color name is used for names that are not recognized
		"""

	def __init__(self):
		self.colors = {
			"crimson" : (220,20,60,255),
			"firebrick" : (178,34,34,255),
			"salmon" : (250,128,114,255),
			#"golden rod" : (218,165,32,255),
			"tomato" : (255,99,71,255),
			#"indian red" : (205,92,92,255),
			"dark khaki" : (189,183,107,255),
			"sea green" : (46,139,87, 255),
			"medium aqua marine" : (102,205,170,255),
			"turquoise" : (64,224,208,255),
			"cadet blue" : (95,158,160,255),
			"steel blue" : (70,130,180,255),
			"indigo" : (75,0,130,255),
			"slate blue" : (106,90,205,255),
			#"dark magenta" : (139,0,139,255),
			"medium orchid" : (186,85,211,255),
			"dark orchid" : (153,50,204,255),
			#"thistle" : (216,191,216,255),
			#"plum" : (221,160,221,255),
			"violet" : (238,130,238,255),
			#"light steel blue" : (176,196,222,255),
			#"azure" : (240,255,255,255),
			"gray" : (128,128,128, 255)
			}
		self.default = "gray"

	def get_255(self, colorName):
		"""Allows retrieving a 0 to 255 scale rgba tuple using standard color name
			if name is not recognized, the self.default color is used
			Case is not a problem
		"""
		colorName = colorName.lower()

		if colorName in list(self.colors.keys()):
			return self.colors[colorName]

		else:
			return self.colors[self.default]

	def make_255_to_1(self, tuple_255):
		""" Uses map to produce a tuple scale 0 to 1 from a tuple scaled 0 to 255"""
		return tuple(list(map(lambda x: round(x/255, 3), tuple_255)))

	def get_1(self, colorName):
		"""Allows retrieving a 0 to 1 scale rgba tuple using standard color name
			if name is not recognized, the self.default color is used
			Case is not a problem
		"""
		colorName = colorName.lower()

		if colorName in list(self.colors.keys()):
			
			tuple_255 = self.colors[colorName]
			tuple_1 = self.make_255_to_1(tuple_255)

			return tuple_1
			
		else:

			tuple_255 = self.colors[self.default]
			tuple_1 = self.make_255_to_1(tuple_255)

			return tuple_1

class KeyToColor:
	"""Allows mapping integers to unique colors, eg: 1 -> Crimson, 2 -> Indigo
		By default uses all colors available in ColorCollection

		To customize, inherit and redefine the self.Mapping method
		which is responsible for preparing the self.mapping dictionary property used
		to map numbers to colors

		By default, colors are assigned alphabetically, with 0 getting the very first

		keys are lowercase strings, values are rgba tuples scale 0 to 1: (r, g, b, a)"""

	def __init__(self):
		### With its own default, set it to map keys like '1' to colors through a loop'
		### Allow reading ColorCollection's self.color's length and fetching with index
		self.colorCollection = ColorCollection()
		self.mapping = {}
		self.default = "gray"

		self.setMapping()

	def setMapping(self):
		# Get a sorted lt of possible colors
		colorKeys = list(self.colorCollection.colors.keys())
		colorKeys.sort()
		length = len(colorKeys) - 1

		count = 0
		for i in range(length):
			if colorKeys[i] != self.default:
				self.mapping[str(count)] = self.colorCollection.get_1(colorKeys[i])
				count += 1

	def getColor(self, key):
		"""Produces a color tuple (r, g, b, a) with values on a 0 to 1 scale based on input key"""

		# Case and int is not a problem 
		key = str(key).lower()

		# If key is recognized
		if key in list(self.mapping.keys()):
			return self.mapping[key]

		else:
			return self.colorCollection.get_1(self.default)

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

