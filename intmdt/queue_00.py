from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from kivy.lang import Builder

from dummys import dummyData, ADT
from boxes import ScrollableLabel, PromptBox, CommandsBox

from customs import DataTableColor

kv = """
"""

Builder.load_string(kv)
