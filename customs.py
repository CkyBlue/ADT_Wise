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

from colors import ColorAwareLabel, HeaderLabel
from boxes import DataBox

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
				l.text = value

				self.dataStructure.setValue(key, i, l)
				b.add_widget(l)
				
			self.add_widget(b)

	def buildInternal(self):
		self.buildHeader()
		self.buildBody()

		#---

class DataTableColor(ScrollView):
	"""A ScrollView object which contains a DataBoxColor widget inside
	DataStructure to be used by the DataBoxCOlor widget is passed in the source keyword"""
	def __init__(self, **kwargs):
		self.source = kwargs["source"]

		del kwargs["source"]
		super(DataTableColor, self).__init__(**kwargs)

		self.dataBox = DataBoxColor(source = self.source)
		self.add_widget(self.dataBox)	

		self.bgColor_1 = (1, 1, 1, 1) #White

		self.instr = InstructionGroup()
		self.canvas.before.add(self.instr)

	def on_size(self, *args):
		self.instr.clear()

		self.instr.add(Color(*self.bgColor_1)) 
		self.instr.add(Rectangle(pos=self.pos, size=self.size))
