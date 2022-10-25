#This is an example of using the tkinter python extension to create a basic window with button
import tkinter.messagebox
from tkinter import *

class CatDatabase:
    def __init__(self):
        self.ourCats = []    #save (catname, catid) tuples in the list

    def add_cat(self, catinfo):
        self.ourCats.append(catinfo)

    def print_cat(self):
        print(ourCats)
class MyFirstGUI: #class definition

    #This is the initialize function for a class.
    #Variables belonging to this class will get created and initialized in this function
    #What is the self parameter? It represents this class itself.
    #By using self.functionname, you can call functions belonging to this class.
    #By using self.variablename, you can create and use variables belonging to this class.
    #It needs to be the first parameter of all the functions in your class

    def __init__(self, root):
        #Master is the default prarent object of all widgets.
        #You can think of it as the window that pops up when you run the GUI code.

        self.master = root
        self.master.title("My Cat Registration System")

        #grid function puts a widget at a certain location
        # return value is none, please do not use it like self.label=Label().grad()
        #it will make self.label=none and you will no longer be able to change the label's content
        self.label = Label(self.master, text="Cat Name: ")
        self.label.grid(row=0, column=0, sticky=E)

        self.catnameentry = Entry(self.master)
        self.catnameentry.grid(row=0, column=1, sticky =E)

        self.catidlabel = Label(self.master, text="Cat ID: ")
        self.catidlabel.grid(row=0, column=2, sticky=E)

        self.catidentry = Entry(self.master)
        self.catidentry.grid(row=0, column=3, sticky=E)
        
        self.submitbutton = Button (self.master, text="Submit name", command=self.submitname)
        self.submitbutton.grid(row=0,column=5, sticky=E)

        self.registerednamelabel = Label(self.master, text="Registered name: ")
        self.registerednamelabel.grid(row=1, column=0, sticky=E)

        self.registerednameentry = Entry(self.master)
        self.registerednameentry.grid(row=1, column=1, sticky=E)

        self.registeredidlabel = Label(self.master, text="Registered ID: ")
        self.registeredidlabel.grid(row=1, column=2, sticky=E)

        self.registeredidentry = Entry(self.master)
        self.registeredidentry.grid(row=1, column=3, sticky=E)

        self.printbutton = Button (self.master, text="Print Database", command=self.printdb)
        self.printbutton.grid(row=1,column=5, sticky=E)
    def submitname (self):
        if not self.catidentry.get():
            tkinter.messagebox.showwarning("No ID", "Please include something for an ID")
            return

        print(f"A cat name submitted: {self.catnameentry.get()} ID: {self.catidentry.get()}")

        self.registerednameentry.delete( 0, END)
        self.registeredidentry.delete(0, END)

        self.registerednameentry.insert(0, self.catnameentry.get())
        self.registeredidentry.insert(0, self.catidentry.get())

        cattuple = (self.registerednameentry.get(), self.registeredidentry.get())

        catDatabase.add_cat(cattuple)


    def printdb (self):
        print("*************************")
        print(" The Cat Database System")
        print("*************************")
        print("Cat Name     |     Cat ID")
        for x in catDatabase.ourCats:
            print(f"  {x[0]}       ,    {x[1]} ")

if __name__ == '__main__':
    catDatabase = CatDatabase()
    myTkRoot = Tk()
    my_gui = MyFirstGUI(myTkRoot)
    myTkRoot.mainloop()

