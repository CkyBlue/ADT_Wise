
Screenshot gif of CLI implementation below.

The table shows data relevant to an algorithm (variable values, index values, items values, pointer values etc.)
The text below it tries to explain what is going to happen next in the algorithm. 
Each index cell has a unique color and the color is the same across index and pointer columns. 
This was intended to make it easier to follow the changes to pointers and index values.

The framework implemented allows easily breaking down a complex algorithm such as an ADT operation
like 'insert into Queue' and let's you see how the data changes as the method moves to completion.

The GUI version at work hopes to take it further with an additional pseudocode window where the
pseudocode (code not associated with any particuar programming language) relevant is highlighted.

Hopefully, it should be possible to extend the use of the framework to make any type of algorithm which 
controls a lot of data easier to understand and follow along with.

I think I'll try to produce a complete working program for an Insertion sort soon to show
what the framework can do and how it makes it easy to do that in code.

Notice how the colors of the cells (in the following gifs) change as the explanation moves forward.

The command line version project requires the colorama library to work.
Run it through CLI/main.py. It uses a clear screen function which 
only seems to work when running the program on a command line so it'll be best to 
view there. The function is different for the repl.it version which is linked below.

The way I've set things up for breaking down, explaining and freezing algorithms hopwfully will also make the task
of setting up the explanation and freeze points within a function simple. Here's what the code might look like.

-----------------------
log("Explanation text") """Provides text explaining what changes are going to be made by this part of the method's algorithm through a string being passed into the log function. Eg: 'The item at index 0 should be change to Ram because blah ... blah'. The log function is passed into the function. """

log("Some more explanation text")

light([1,2,3]) """Highlight line 1,2 & 3 in the pseudocode"""

lock() """Freeze the function at this point and update visuals to show added explanation text and changes made to data and pseudocode
	so far, once user gives the go, unfreeze the function and continue"""

"""Carry out the changes described in above in program code, eg: self.dataStructure.setValue("Item", 0, "Ram")"""

lock() #The next time the method freezes, the changes made will show up, the tables will show that the item Ram has been added to index 0


-----------------------

Freezing the code works by temporarily setting up a slowly looping infinite loop, the whole function runs on its own thread
seperate from the one on which the rest of the program is running so the rest of the program does not freeze

Question 6 at "https://papers.gceguide.com/A%20Levels/Computer%20Science%20(for%20final%20examination%20in%202021)%20(9608)/9608_s15_qp_41.pdf" 
should give you an idea of what kind of CS questions it's supposed to be helpful for.

Run the command line version on browser: https://repl.it/@OverCky/ADT-Wise

Screenshots from the command line version on repl.it:

![Screenshot](ADTWIse.gif)
![Screenshot](Screenshot1.PNG)

The GUI version is still under work. It relies on the Kivy framework.
The framework used to freeze algorithms and control their behavior is is also being worked from scratch for the GUI.
See dummys.py for the implementation of the ADT methods and adt_wise_gui.py for how the GUI below was put together

How the GUI is coming along:

![Screenshot](GUI.gif)
