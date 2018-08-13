class func():
	def __init__(self, parameters):
		self.p = parameters
		self.log = []

		self.log.append("Firing")
		return self.fn1

	def fn1(self):
		self.log.append("All done")
		return lambda x: False

class Queue():
	def doSmth(self, par):
		return func(par)

class Model():
	pass

class Prompt():
	pass

class View():
	def __init__(self):
		self.controller = myController
		self.fireCommand("Call1")

	def fireCommand(self, cmd):
		self.setPrompt(self.controller.qns["Call1"])

	def setPrompt(self, para):
		x = input(para)

	def giveValInPrompt

class Controller():
	adt = Queue()
	calls = ["Call1"]
	qns = {"Call1": "Do you?"}
	funcs = [Queue.doSmth]

if __name__ == "__main__":
	myController = Controller()
	myView = View()
