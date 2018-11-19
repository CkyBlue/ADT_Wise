"""Classes that are supposed to be adaptable for multiple purposes
are not directly customized for the distinct visuals required.

Instead polymorphism is used. These inheriting classes are defined 
in this customs.py file"""

from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle 

from labels import ColorAwareLabel, HeaderLabel
from data import PointerData, VariableData
from boxes import DataBox, PseudoCodeBox

class DataBoxColor(DataBox):
	"""Adds ColorAwareLabel to the DataBox def
	along with spacing and padding definition
	and """
	def __init__(self, **kwargs):
		super(DataBoxColor, self).__init__(**kwargs)

		# For the purpose of ensuring that the widget works as
		#  a child of the ScrollView object
		#  widget's height is binded to and set as the minimum height
		self.size_hint_y = None
		self.bind(minimum_height = self.setter('height'))

		# Customizing the visuals

		self.spacing = "5px"
		self.padding = "5px"

	def buildHeader(self):
		#Creates a box-layout which serves as the row
		h = BoxLayout(spacing = "2px", size_hint_y = None ,height = "40px")
		
		for key in self.source.keys: # For each key (i.e header)

			l = HeaderLabel()
			l.text = key

			h.add_widget(l)

		self.add_widget(h)

	def buildBody(self):
		# Produces the labels that populate self.dataStructure 
		for i in range(self.source.size):

			#Creates a box-layout which serves as the row
			b = BoxLayout(spacing = "2px", size_hint_y = None ,height = "40px")

			for key in self.source.keys:

				value = self.source.getValue(key, i)

				#Note that text cannot be passed as keyword here
				l = ColorAwareLabel()
				l.text = str(value)

				self.dataStructure.setValue(key, i, l)
				b.add_widget(l)
				
			self.add_widget(b)

	def buildInternal(self):
		self.buildHeader()
		self.buildBody()

class Scroll_Box_For_DataBoxColor(ScrollView):
	"""A ScrollView object which contains a DataBoxColor widget inside
	DataStructure to be used by the DataBoxCOlor widget is passed in the source keyword"""
	def __init__(self, **kwargs):
		self.source = kwargs["source"]

		del kwargs["source"]
		super(Scroll_Box_For_DataBoxColor, self).__init__(**kwargs)

		self.dataBox = DataBoxColor(source = self.source)
		self.add_widget(self.dataBox)	

		self.bgColor_1 = (1, 1, 1, 1) #White

		self.instr = InstructionGroup()
		self.canvas.before.add(self.instr)

	def on_size(self, *args):
		self.instr.clear()

		self.instr.add(Color(*self.bgColor_1)) 
		self.instr.add(Rectangle(pos=self.pos, size=self.size))

class VariableBox(BoxLayout):
	"""Takes a VariableData object as parameter through the source keyword
		Develops a mirror object to track the label associated with each data item
		updateContent method reads the source Pointer again and updates the label contents
	"""
	def __init__(self, **kwargs):
		# The DataStructure object to be used for as the source of data
		self.source = kwargs["source"]

		del kwargs["source"]
		super(VariableBox, self).__init__(**kwargs)

		# A PointerBox object which mirrors self.source but stores Label widgets corresponding
		# to each data item in the source at the matching key and index position
		self.mirror = VariableData(self.source.keys)

		self.orientation = 'vertical'

		# For the purpose of ensuring that the widget works as
		#  a child of the ScrollView object
		#  widget's height is binded to and set as the minimum height
		self.size_hint_y = None
		self.bind(minimum_height = self.setter('height'))

		# Customizing the visuals

		self.spacing = "5px"
		self.padding = "5px"

		self.buildInternal()

	def buildInternal(self):
		#Creates a box-layout which serves as the header
		h = BoxLayout(spacing = "2px", size_hint_y = None ,height = "40px")
		
		for item in ["Variable", "Value"]: #The header contains those two titles

			l = HeaderLabel()
			l.text = item

			h.add_widget(l)

		self.add_widget(h)

		# Produces the labels that populate self.mirror 
		for key in self.source.keys:

			#Creates a box-layout which serves as the row
			b = BoxLayout(spacing = "2px", size_hint_y = None ,height = "40px")

			value = self.source.getValue(key)

			#Note that text cannot be passed as keyword into ColorAwareLabel
			d = ColorAwareLabel() #Label for variable name
			d.text = key.title()

			l = ColorAwareLabel() #Label for pointer value
			l.text = str(value)
			
			self.mirror.setValue(key, l) #Only this value needs to be updated
			
			b.add_widget(d)
			b.add_widget(l)				
			self.add_widget(b)

	def updateContent(self):
		# The controller should run this through the logTarget function which is 
		#  called by the CallableActions object with each freeze

		# Updates the labels accessed through self.mirror using the data from the source
		for key in self.source.keys:
			
			value = self.source.getValue(key)
			l = self.mirror.getValue(key)
			l.text = str(value) 

class PointerBox(VariableBox):
	"""Takes a PointerData object as parameter through the source keyword
		Develops a mirror (VariableData) object to track the label associated with each data item
		updateContent method reads the source Pointer again and updates the label contents

		Differs from Variable box in that the text 'Pointer' is added automatically to PointerData's
		keys ('Free', 'Head') and that the header text mentions 'Pointer' istead of 'Variable'
	"""

	def buildInternal(self):
		#Creates a box-layout which serves as the header
		h = BoxLayout(spacing = "2px", size_hint_y = None ,height = "40px")
		
		for item in ["Pointer", "Value"]: #The header contains those two titles

			l = HeaderLabel()
			l.text = item

			h.add_widget(l)

		self.add_widget(h)

		# Produces the labels that populate self.mirror 
		for key in self.source.keys:

			#Creates a box-layout which serves as the row
			b = BoxLayout(spacing = "2px", size_hint_y = None ,height = "40px")

			value = self.source.getValue(key)

			#Note that text cannot be passed as keyword into ColorAwareLabel
			d = ColorAwareLabel() #Label for pointer name
			d.text = key.title() + " " + "Pointer" # Eg: "Head" + " " + "Pointer" => "Head Pointer"

			l = ColorAwareLabel() #Label for pointer value
			l.text = str(value)
			
			self.mirror.setValue(key, l) #Only this value needs to be updated
			
			b.add_widget(d)
			b.add_widget(l)				
			self.add_widget(b)

	def updateContent(self):
		# The controller should run this through the logTarget function which is 
		#  called by the CallableActions object with each freeze

		# Updates the labels accessed through self.mirror using the data from the source
		for key in self.source.keys:
			
			value = self.source.getValue(key)
			l = self.mirror.getValue(key)
			l.text = str(value) 