# Reads color.txt and produces a version formatted for .py

f = open("Color.txt", "r") #Read from
g = open("intmdt_07.py", "w+") #Written to

items = f.readlines()

for x in items:
	a = x.index("(")
	colorCode = x[a:]
	name = x[:a - 1]
	g.write('"' + name +'" : ' + colorCode)

f.close()
g.close()
