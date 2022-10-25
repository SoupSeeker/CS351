import re
import shlex
import tkinter.messagebox
from tkinter import *


class LexerData:
    def __init__(self):
        self.lexdata = []
        self.parsedata = []         # saving a separate copy we can pop for parser
        self.lexsize = 0

    def dump_lexdata(self):
        print(self.lexdata)

    def add_line(self, currentline):
        self.lexdata.append(currentline)
        self.parsedata.append(currentline)
        self.lexsize += 1

    def tokenize(self, currentinput):
        semicolon = re.findall(';', currentinput)  # first things first, checking if there is a semicolon
        colon = re.findall(':', currentinput)

        if semicolon:
            currentinput = currentinput[:-1]  # take away ;
            wordlist = re.split('\s+', currentinput)  # next, form a 'wordlist' by splitting the current line
            wordlist.append(';')

        elif colon:
            currentinput = currentinput[:-1]
            wordlist = re.split('\s+', currentinput)
            wordlist.append(':')

        else:
            return "Improper"

        keywords = re.compile(r'^(?=print|float|int|if|else)\w+')
        identifiers = re.compile(r'\S*\b(?<!\")(?!if|or|print|else|float|int|[0-9])\w+\b(?!\"| ")\S*')
        operators = re.compile(r'\S*\W*\+|\*|>|=\W*\S*')
        separators = re.compile('[()\":;]')
        intLiterals = re.compile(r'(?<!\.)\b[0-9]+\b(?!\.)')
        floatLiterals = re.compile(r'\S*\d+\.\d+\S*')
        stringLiterals = re.compile(r'\"(\s*\w+\s*)+\"')

        for word in wordlist:

            keyResult = keywords.search(word)
            identResult = identifiers.search(word)
            opResult = operators.search(word)
            sepResult = separators.search(word)
            intResult = intLiterals.search(word)
            floatResult = floatLiterals.search(word)
            stringResult = stringLiterals.match(word)

            if keyResult is not None:
                lexerData.add_line(f"Type, {keyResult.group(0).strip()}")
            if stringResult:
                lexerData.add_line(f"String, {stringResult.group(0).strip()}")
            elif identResult:
                lexerData.add_line(f"Identifier, {identResult.group(0).strip()}")
            if opResult:
                lexerData.add_line(f"Operator, {opResult.group(0).strip()}")
            if floatResult:
                lexerData.add_line(f"Float, {floatResult.group(0).strip()}")
            if intResult:
                lexerData.add_line(f"Int, {intResult.group(0).strip()}")
            if sepResult:
                lexerData.add_line(f"Separator, {sepResult.group(0).strip()}")


class MyFirstGUI:
    def __init__(self, root):

        self.master = root
        self.master.title("Lexer GUI")
        self.currentline = 0

        self.codelabel = Label(self.master, text="Source Code Input: ")
        self.codelabel.grid(row=0, column=0, sticky=NW, padx=50)

        self.sourcecode = Text(self.master, font=("Verdana", 12), height=30, width=45)
        self.sourcecode.grid(row=1, column=0, sticky=W, padx=10, pady=10)

        self.nextlinebutton = Button(self.master, text="Next Line", command=self.nextline)
        self.nextlinebutton.grid(row=2, column=0, sticky=W, padx=10, pady=10)

        self.cplabel = Label(self.master, text="Current Processing Line: ")
        self.cplabel.grid(row=2, column=3, sticky=S, pady=10)

        self.linecountlabel = Label(self.master, text=self.currentline)
        self.linecountlabel.grid(row=2, column=3, sticky=SE, padx=10, pady=10)

        self.tokenlabel = Label(self.master, text="Tokens ")
        self.tokenlabel.grid(row=0, column=1, sticky=N)

        self.lexoutput = Text(self.master, font=("Verdana", 12), height=30, width=45)
        self.lexoutput.grid(row=1, column=1, sticky=E, padx=10, pady=10)
        # add parse tree label and box
        self.parselabel = Label(self.master, text="Parse Output")
        self.parselabel.grid(row=0, column=3, sticky=N, padx=10, pady=10)

        self.parseoutput = Text(self.master, font=("Verdana", 12), height=30, width=45)
        self.parseoutput.grid(row=1, column=3, sticky=E, padx=10, pady=10)

        self.parsesb = Scrollbar(self.master, command=self.parseoutput.yview)
        self.parsesb.grid(row=1, column=4, sticky=E)

        self.exit_button = Button(self.master, text="Quit", command=root.destroy)
        self.exit_button.grid(row=2, column=4, sticky=SE, padx=10, pady=10)


    # were going to change the nextline so that we print out the token pairs from each line, rather the line
    def nextline(self):
        self.lexoutput.delete("0.0", END)
        self.parseoutput.delete("0.0", END)
        self.previoussize = lexerData.lexsize

        text = self.sourcecode.get("1.0", END).split('\n')  # read the whole text widget, split by newlines

        if self.currentline == len(text) - 1:
            exit()                              # exit if we enter a blank line

        if lexerData.tokenize(text[self.currentline]) == "Improper":   # tokenize call is hidden in this line
            self.lexoutput.insert(END, "Improper use of ; or :")        # as of hw 7 we REQUIRE ; or :
            self.lexoutput.insert(END, '\n')
            return

        # this loop will print correct info to the LEXOUTPUT section
        #  ex: let startindex = previous size = k. let current size = n, then range = n - k
        startingindex = self.previoussize
        for x in range(lexerData.lexsize - self.previoussize):

            insertedtext = lexerData.lexdata[startingindex]
            startingindex += 1

            self.lexoutput.insert(END, f"<{insertedtext}>\n")

        self.currentline += 1
        self.linecountlabel.config(text=self.currentline)

        self.parser()   # finally we call recursive parser algorithm


# #---------------------------------parser code below------------------------------------------------------# #
# all the print functions can be replaced with stuff to send text to the 3rd text box
    def accept_token(self):
        global inToken
        self.parseoutput.insert(END, "\n             !!!!!accepted token!!!!! ->" + inToken[1])
        inToken = lexerData.parsedata.pop(0)
        inToken = tuple(inToken.split(","))


    def math(self):
        self.parseoutput.insert(END, "\n----------PARENT: math----------")
        global inToken

        if (inToken[0] == "Float"):
            self.parseoutput.insert(END, "\n  child node found! -> float")
            self.parseoutput.insert(END, "\n     float has child node! -> " + inToken[1])
            self.accept_token()

            if (inToken[1] == " +"):
                self.parseoutput.insert(END, "\n       inner child node found! -> " + inToken[1])
                self.accept_token()

                self.parseoutput.insert(END, "\n*****Going to inner child node! -> math")
                self.math()
            elif (inToken[1] == " *"):
                self.parseoutput.insert(END, "\n       inner child node found! -> " + inToken[1])
                self.accept_token()

                self.parseoutput.insert(END, "\n*****Going to inner child node! -> math")
                self.math()

        elif (inToken[0] == "Int"):
            self.parseoutput.insert(END, "\n  child node found! -> int")
            self.parseoutput.insert(END, "\n     int has child node! -> " + inToken[1])
            self.accept_token()

            if (inToken[1] == " +"):
                self.parseoutput.insert(END, "\n       child node (token):" + inToken[1])
                self.accept_token()

                self.parseoutput.insert(END, "\n*****Going to inner child node! -> math")
                self.math()
            elif (inToken[1] == " *"):
                self.parseoutput.insert(END, "\n       child node (token):" + inToken[1])
                self.accept_token()

                self.parseoutput.insert(END, "\n*****Going to inner child node! -> math")
                self.math()

        else:
            self.parseoutput.insert(END, "\nerror, math expects float or int")


    def exp(self):
        self.parseoutput.insert(END, "\n----------PARENT: exp----------")
        global inToken
        typeT, token = inToken                 # need to read in either by string or direct tokens, refer to pdf #

        if (typeT == "Type"):
            self.parseoutput.insert(END, "\n  child node found! -> type")
            self.parseoutput.insert(END, "\n     type has child! -> " + token)
            self.accept_token()
        else:
            self.parseoutput.insert(END, "\nexpect type as the first element of the expression!\n")
            return

        if (inToken[0] == "Identifier"):
            self.parseoutput.insert(END, "\n  inner child found! -> identifier")
            self.parseoutput.insert(END, "\n     identifier has child node! -> " + token)
            self.accept_token()
        else:
            self.parseoutput.insert(END, "\nexpected identifier as the second element of the expression!")
            return

        if (inToken[1] == " ="):
            self.parseoutput.insert(END, "\n  child node found! -> " + inToken[1])
            self.accept_token()

        self.parseoutput.insert(END, "\n*****Going to inner child node! -> math")
        self.math()


    def parser(self):
        global inToken
        inToken = lexerData.parsedata.pop(0)
        inToken = tuple(inToken.split(","))
        self.exp()
        if inToken[1] == " ;":          # this line requires the command have semicolon
            self.parseoutput.insert(END, "\nparse tree building success!")
        return


if __name__ == '__main__':
    lexerData = LexerData()
    myTkRoot = Tk()
    my_gui = MyFirstGUI(myTkRoot)
    myTkRoot.mainloop()
