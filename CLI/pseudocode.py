from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle 

from colors import ColorAwareLabel, HeaderLabel
from data import PointerData
from boxes import DataBox

from kivy.lang import Builder

kv = """
<Root@BoxLayout>:
	AltLabel:
	Button:
"""

Builder.load_string(kv)

class AltLabel(BoxLayout):
	"""		"""

	def __init__(self, **kwargs):
		super(AltLabel, self).__init__(**kwargs)

		self.onColor = (1, 0, 0, 1)
		self.offColor = (0, 1, 0, 1)

		self.bold = False
		self.font_size = 14

		self.active = False

		self.instr = InstructionGroup()
		self.canvas.before.add(self.instr)

	def on_active(self):
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


class pseudoApp(App):
	def build(self):
		return Root()

pseudoApp().run()
