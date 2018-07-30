from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder 

kv = """
<Row@BoxLayout>:
	canvas.before:
		Color:
			rgba: 0.5, 0.5, 0.5, 1
		Rectangle:
			pos: self.pos
			size: self.size

	col1: ''
	col2: ''

	orientation: 'horizontal'
	Label:
		text: "Col1"


<Root>:
	rv: rv
	orientation: 'vertical'

	GridLayout:
		size_hint_y: None
		height: dp(54)
		spacing: dp(12)
		padding: dp(8)

		rows: 1
		cols: 3

		BoxLayout:
			spacing: dp(6)
			Button:
				text: 'Add Entry'
				on_press: root.addEntry(new_item_input.text)

			TextInput:
				id: new_item_input
				text: 'Default'

		Button:
			text: 'Delete Entry'
			on_press: root.delEntry()

		Label:
			text: 'Number of Entries: {}'.format(len(root.rv.data))
	
	RecycleView:
		id: rv
		viewclass: 'Row'

		RecycleBoxLayout:
			default_size: None, dp(56)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height

            orientation: 'vertical'
            spacing: dp(2)
"""

Builder.load_string(kv)

class Root(BoxLayout):
	def addEntry(self, value):
		self.rv.data.append({"Col2": value})

	def delEntry(self):
		self.rv.data.pop()

class b2App(App):
	title = "Bin - 02"

	def build(self):
		return Root()

if __name__ == "__main__":
	b2App().run() 