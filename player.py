from sys import stdout

class Player():
    def __init__(self, name, term=stdout):
        self.name = name
        self.term = term

    def message(self, mesg):
        self.term.write(mesg)
        self.term.write("\n")
