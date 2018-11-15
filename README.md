
The command line version project requires the colorama library to work.
Run it through CLI/main.py. It uses a clear screen function which 
only seems to work when running the program on a command line so it'll be best to 
view there.

The table shows data relevant to the ADT (index values, items values, pointer values etc.)
The text below it tries to explain what is going to happen next. 
Each index value has a unique color and is the same across index and pointer columns. 
This was intended to make it easier to follow the changes to pointers and index values.
IThe program breaks down a complex ADT operation
such as insert and let's you see how the data changes as the method moves to completion.

Notice how the colors change as the explanation moves forward.
In the actual program, the program waits for user input before moving onto the next fragment of the 
ADT method so it is easier to follow.

The framework I've set up for breaking down and explaining ADT methods also makes the task
simple for would-be contributers. Here's what the code might like.

-----------------------
log("Explanation text") """Provide text explaining what changes are going to be made by this part of the method's algorithm"""

log("Some more explanation text")

lock() """Freeze the method at this point and update visuals to show added explanation text and changes made to data so far, once user gives the go, unfreeze and continue"""

"""Carry out the changes described in above in program code, eg: self.dataStructure.setValue("Item", 0, "Ram")"""

lock() #The next time the method freezes, the changes made will show up, the tables will show that the item Ram has been added to index 0


-----------------------

Run the command line version on browser: https://repl.it/@OverCky/ADT-Wise

Screenshots from the command line version on repl.it:

![Screenshot](ADTWIse.gif)
![Screenshot](Screenshot1.PNG)

The GUI version is still under work. It relies on the Kivy framework.
The ADT backbone is also being worked from scratch for the GUI.

How the GUI is coming along:

![Screenshot](GUI.gif)
