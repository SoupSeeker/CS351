import re
import tkinter.messagebox
from tkinter import *

class LexerData:
    def __init__(self):
        self.lexdata = []
        self.lexsize = 0

    def dump_lexdata(self):
        print(self.lexdata)

    def add_line(self, currentline):
        self.lexdata.append(currentline)
        self.lexsize += 1

    def tokenize(self, currentinput):
        keywords = re.compile('\s*\W*if|float|else|print|int\W*\s*')
        identifiers = re.compile(r'\s*\b(?!if|else|float|print|int)\b\S+\s*')
        operators = re.compile('\s*\W*\+|\*|>|=\W*\s*')
        separators = re.compile('\s*[()":;]\s*')
        intLiterals = re.compile(r'(?<!\.)\b[0-9]+\b(?!\.)')
        floatLiterals = re.compile('\s*\d+\.\d+')
        stringLiterals = re.compile('\"\s*\w+(\s+\w+)*\s*\"')

        keyResult = keywords.search(currentinput)
        identResult = identifiers.search(currentinput)
        opResult = operators.findall(currentinput)  # using findall in operators, seperators, int, float, and strings
        sepResult = separators.findall(currentinput)
        intResult = intLiterals.findall(currentinput)
        floatResult = floatLiterals.findall(currentinput)
        stringResult = stringLiterals.findall(currentinput)

        if keyResult is not None:
            lexerData.add_line([f"Type, {keyResult.group(0)}"])
        if identResult:
            lexerData.add_line([f"<Identifier, {identResult.group(0)}>"])
        if opResult:
            for x in opResult:
                lexerData.add_line([f"<Operator, {x}>"])
        if floatResult:
            for x in floatResult:
                lexerData.add_line([f"<Float, {x}>"])
        if intResult:
            for x in intResult:
                lexerData.add_line([f"<Int, {x}>"])
        if stringResult:
            lexerData.add_line([f"<String, {stringResult}>"])
        if sepResult:
            for x in sepResult:
                lexerData.add_line([f"<Separator, {x}>"])

class MyFirstGUI:
    def __init__(self, root):
        # Master is the default prarent object of all widgets.

        self.master = root
        self.master.title("Lexer GUI")

        self.codelabel = Label(self.master, text="Source Code Input: ")
        self.codelabel.grid(row=0, column=0, sticky=NW, padx=50)

        self.sourcecode = Text(self.master, font=("Times New Roman", 11))
        self.sourcecode.grid(row=1, column=0, sticky=W, padx=10, pady=10)

        self.nextlinebutton = Button(self.master, text="Next Line", command=self.nextline)
        self.nextlinebutton.grid(row=2, column=0, sticky=W, padx=10, pady=10)

        self.currentline = 0

        self.cplabel = Label(self.master, text="Current Processing Line: ")
        self.cplabel.grid(row=2, column=1, sticky=S, pady=10)

        self.linecountlabel = Label(self.master, text=self.currentline)
        self.linecountlabel.grid(row=2, column=2, sticky=S, padx=10, pady=10)

        self.tokenlabel = Label(self.master, text="Tokens ")
        self.tokenlabel.grid(row=0, column=1, sticky=N)

        self.lexoutput = Text(self.master, font=("Times New Roman", 11))
        self.lexoutput.grid(row=1, column=1, sticky=E, padx=10, pady=10)

        #add parse tree label and box


        self.exit_button = Button(self.master, text="Quit", command=root.destroy)
        self.exit_button.grid(row=2, column=3, sticky=SE, padx=10, pady=10)


    #were going to change the nextline so that we print out the token pairs from each line, rather the line
    def nextline(self):
        #self.lexoutput.delete("0.0", END)

        self.previoussize = lexerData.lexsize

        text = self.sourcecode.get("1.0", END).split('\n')  #read the whole text widget, split by newlines

        if self.currentline == len(text)-1:     #will simply exit the terminal if we hit newline and the newline is blank
            exit()

        lexerData.tokenize(text[self.currentline])  #tokenize the currentline and store it in the lexdata list

        #after tokenize, the lexsize increases
        startingindex = self.previoussize
        for x in range(lexerData.lexsize - self.previoussize): #this prints out the correct section of info to the text

            insertabletext = lexerData.lexdata[startingindex]
            startingindex += 1

            self.lexoutput.insert(END, insertabletext)
            self.lexoutput.insert(END, '\n')

        self.currentline += 1
        self.linecountlabel.config(text=self.currentline)   #current line goes up only AFTER we use it



if __name__ == '__main__':
    lexerData = LexerData()
    myTkRoot = Tk()
    my_gui = MyFirstGUI(myTkRoot)
    myTkRoot.mainloop()


