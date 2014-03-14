"""A module defining basic functions and generic classes for games"""

import abc
import sys

class Player(object):
    """Defines a Player for a game"""
    def __init__(self, name, term=sys.stdout):
        self.name = name
        self._term = term

    def __str__(self):
        return "{name}".format(**self.__dict__)

    def __repr__(self):
        return ("Player(name={name!r}, "
                "term={_term.name!r})".format(**self.__dict__))

    def message(self, mesg):
        """Display a message on the plaayer's terminal"""
        self._term.write(mesg)
        self._term.write("\n")

class Game(object, metaclass=abc.ABCMeta):
    """Defines a Game"""
    def __init__(self, players=None):
        if players:
            self.players = players
        else:
            self.players = []
        self.name = "Game"

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Game(players={players!r})".format(**self.__dict__)

    def add_player(self, player):
        """Adds a player to the game"""
        self.players.append(player)

    @abc.abstractmethod
    def play(self):
        """Interface for playing the game"""
        pass
