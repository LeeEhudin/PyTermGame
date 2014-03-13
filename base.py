"""A module defining basic functions and generic classes for games"""

import abc
import sys

class Player(object):
    """Defines a Player for a game"""
    def __init__(self, name, term=sys.stdout):
        self.name = name
        self.term = term

    def __str__(self):
        return "{name}".format(**self.__dict__)

    def __repr__(self):
        return ("Player(name={name!r}, "
                "term={term.name!r})".format(**self.__dict__))

    def message(self, mesg):
        """Display a message on the plaayer's terminal"""
        self.term.write(mesg)
        self.term.write("\n")

class Game(object, metaclass=abc.ABCMeta):
    """Defines a Game"""
    def __init__(self, *players):
        self.players = players
        self.name = "Game"

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Game(players={players!r})".format(**self.__dict__)

    @abc.abstractmethod
    def play(self):
        """Iinterface for playing the game"""
        pass
