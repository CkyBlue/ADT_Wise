from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.lang import Builder

from boxes import ScrollableLabel

text = """
	Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus rutrum quis turpis ac fermentum. Vestibulum justo nisl, faucibus non urna id, condimentum convallis metus. Sed non quam quis enim lacinia condimentum. Nulla suscipit sit amet elit sit amet cursus. Interdum et malesuada fames ac ante ipsum primis in faucibus. Vestibulum ut libero nibh. Etiam facilisis ante a aliquam tincidunt. Mauris semper risus et sem porttitor gravida. Aenean id vulputate lacus. Sed mollis risus et tellus sollicitudin ultricies. Vivamus laoreet, sapien ut ullamcorper lobortis, ante velit tincidunt nulla, sed feugiat nunc erat sed tellus. Sed dictum varius molestie.

	Maecenas cursus sapien eu posuere ullamcorper. Nam finibus aliquam nisl ac accumsan. Cras in pellentesque mi. Nullam rutrum massa interdum felis vehicula dictum. Phasellus venenatis, metus eu rutrum accumsan, diam sapien feugiat tortor, eget tristique ante erat placerat dui. Aenean lobortis imperdiet magna nec pharetra. Vivamus non lorem eget justo gravida porttitor. Maecenas nec rhoncus lorem, eu imperdiet ligula. In consectetur, erat a tempor iaculis, ex tellus ornare tellus, vel tempor elit diam ac quam. Praesent efficitur sapien et libero ultrices, et accumsan augue viverra. Quisque ornare aliquet ex congue pretium. In ut tellus eu quam tincidunt faucibus. Integer ultricies eros at sem mollis ornare.

	Ut luctus metus nibh, in hendrerit arcu pellentesque eget. Duis quis nisl sit amet dolor dictum commodo at iaculis turpis. Phasellus placerat, arcu sed rhoncus vehicula, lacus urna luctus massa, sit amet sodales nunc ex vel orci. Donec sodales venenatis scelerisque. Etiam id pharetra lorem. Pellentesque pellentesque, nisi sit amet maximus lobortis, nisl mauris tincidunt orci, quis mollis ipsum ligula a velit. In auctor tincidunt nibh.

	Nunc ornare in lectus ac tincidunt. Vivamus tincidunt malesuada fermentum. Maecenas vitae pretium orci. Nullam risus ex, fermentum non tincidunt eu, suscipit id odio. Interdum et malesuada fames ac ante ipsum primis in faucibus. Vivamus congue eleifend nisi sit amet cursus. In euismod ipsum at urna aliquam, quis rhoncus felis scelerisque.

	Donec eget ex sit amet sem faucibus dignissim. Vestibulum purus turpis, tempor vel ipsum in, posuere tempus nibh. Integer posuere tortor ex, at cursus felis congue a. Phasellus tempor quis metus et suscipit. Curabitur facilisis tincidunt commodo. Praesent ut metus elementum, sodales eros nec, posuere justo. Phasellus porta blandit enim, vel malesuada odio luctus id.
	"""

class Root(BoxLayout):
	def __init__(self, **kwargs):
		super(Root, self).__init__(**kwargs)

		self.lbl = ScrollableLabel()
		self.lbl.setText(text)

		self.add_widget(self.lbl)

class MyApp(App):
	def build(self):
		return Root()

MyApp().run()