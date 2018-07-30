from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder 

kv = """
#:import Transition kivy.uix.screenmanager.SlideTransition

<Root>:
	canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
	transition: Transition()
	ScreenBase:
	ScreenOver:

<ScreenBase>:
	name: 'screen_base'
	BoxLayout:
		canvas.before:
	        Color:
	            rgba: 0, 1, 0, 1
	        Rectangle:
	            pos: self.pos
	            size: self.size
		Label:
			text: 'Base'
		Button:
			text: 'Goto Over'
			on_press: root.manager.current = 'screen_over'

<ScreenOver>:
	name: 'screen_over'
	BoxLayout:
		canvas.before:
	        Color:
	            rgba: 0, 0, 1, 1
	        Rectangle:
	            pos: self.pos
	            size: self.size
		Label:
			text: 'Over'
		Button:
			text: 'Goto Base'
			on_press: root.manager.current = 'screen_base'

"""

Builder.load_string(kv)

class ScreenBase(Screen):
	pass

class ScreenOver(Screen):
	pass

class Root(ScreenManager):
	pass

class b3App(App):
	def build(self):
		return Root()

if __name__ == "__main__":
	b3App().run()