### Add documentation

class ColorCollection:
	def __init__(self):
		self.colors = {
			"crimson" : (220,20,60,255),
			"firebrick" : (178,34,34,255),
			"salmon" : (250,128,114,255),
			"golden rod" : (218,165,32,255),
			"tomato" : (255,99,71,255),
			"indian red" : (205,92,92,255),
			"dark khaki" : (189,183,107,255),
			"light green" : (144,238,144,255),
			"medium aqua marine" : (102,205,170,255),
			"turquoise" : (64,224,208,255),
			"cadet blue" : (95,158,160,255),
			"sky blue" : (135,206,235,255),
			"indigo" : (75,0,130,255),
			"slate blue" : (106,90,205,255),
			"dark magenta" : (139,0,139,255),
			"medium orchid" : (186,85,211,255),
			"dark orchid" : (153,50,204,255),
			"thistle" : (216,191,216,255),
			"plum" : (221,160,221,255),
			"violet" : (238,130,238,255),
			"light steel blue" : (176,196,222,255),
			"azure" : (240,255,255,255),
			"gainsboro" : (220,220,220,255)
			}
		self.default = "gainsboro"	

	def get_255(self, colorName):
		colorName = colorName.lower()

		if colorName in list(self.colors.keys()):
			return self.colors[colorName]

		else:
			return self.colors[self.default]

	def make_255_to_1(self, tuple_255):
		""" Uses map to produce a tuple scale 0 to 1 from a tuple scaled 0 to 255"""
		return tuple(list(map(lambda x: round(x/255, 3), tuple_255)))

	def get_1(self, colorName):
		colorName = colorName.lower()

		if colorName in list(self.colors.keys()):
			
			tuple_255 = self.colors[colorName]
			tuple_1 = self.make_255_to_1(tuple_255)

			return tuple_1
			
		else:

			tuple_255 = self.colors[self.default]
			tuple_1 = self.make_255_to_1(tuple_255)

			return tuple_1
