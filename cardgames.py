"""A module defining functions for playing card games"""

import abc
import bisect
import collections.abc
import itertools
import random
import sys

import base

class Card(object):
    """Defines a Card class for easy access to a card's suit and value"""
    VALUES = ("ace", "2", "3", "4", "5", "6", "7", "8", "9", "10",
              "jack", "queen", "king")
    SUITS = ("spades", "hearts", "diamonds", "clubs")
    _value_aliases = {"ace":"A", "jack":"J", "queen":"Q", "king":"K"}
    _suit_aliases = {"spades":"♠", "hearts":"♥", "diamonds":"♦", "clubs":"♣"}

    def __init__(self, value, suit):
        short_suits = {suit[0]:suit for suit in Card.SUITS}

        if isinstance(value, int):
            if value in range(1, len(Card.VALUES)+1):
                self.value = Card.VALUES[value-1]
            else:
                raise ValueError("%d is not a valid value for a card." % value)
        elif str(value).lower() in Card.VALUES:
            self.value = str(value).lower()
        else:
            raise ValueError("%s is not a valid value for a card." % value)

        if str(suit).lower() in short_suits:
            self.suit = short_suits[str(suit).lower()]
        elif str(suit).lower() in Card.SUITS:
            self.suit = str(suit).lower()
        else:
            raise ValueError("%s is not a valid suit for a card." % suit)

    def __eq__(self, other):
        if (isinstance(other, Card) and
            self.value == other.value and self.suit == other.suit):
            return True
        else:
            return False

    def __neq__(self, other):
        return not self == other

    def __lt__(self, other):
        if Card.VALUES.index(self.value) < Card.VALUES.index(other.value):
            return (Card.VALUES.index(self.value) <
                    Card.VALUES.index(other.value))
        else:
            return Card.SUITS.index(self.suit) < Card.SUITS.index(other.suit)

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other

    def __str__(self):
        return "{:1}{:1}".format(
            Card._value_aliases.get(self.value, self.value),
            Card._suit_aliases.get(self.suit, self.suit))

    def __repr__(self):
        return "Card(value={value!r}, suit={suit!r})".format(**self.__dict__)

class Deck(collections.abc.Sized, collections.abc.Iterable):
    """Defines a Deck class to store cards"""
    def __init__(self, shuffled=True):
        self.cards = [Card(value, suit) for
                     suit in Card.SUITS for value in Card.VALUES]
        if shuffled:
            self.shuffle()

    def __repr__(self):
        return ', '.join(repr(card) for card in self.cards)

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)

    def __len__(self):
        return len(self.cards)

    def __iter__(self):
        return self.draw(len(self.cards))

    def shuffle(self):
        """Shuffle the deck"""
        random.shuffle(self.cards)

    def draw(self, num_cards):
        """Draw num_cards card from the Deck using a generator"""
        for _ in range(num_cards):
            yield self.cards.pop(0)

    def deal(self, num_cards, *players):
        """Deals num_cards cards to each player"""
        for i, card in enumerate(self.draw(num_cards * len(players))):
            players[i % len(players)].hand.add_card(card)

class Hand(collections.abc.Sized):
    """Defines a Hand class to store Player's hands"""
    def __init__(self, *cards, sort_by_val=True):
        self.cards = []
        if sort_by_val:
            self.sort_by = "value"
        else:
            self.sort_by = "suit"
        self._keys = []

        if cards:
            for card in cards:
                self.add_card(card)

    def __add__(self, other):
        for card in other:
            self.add_card(card)

    def __len__(self):
        return len(self.cards)

    def __repr__(self):
        return ', '.join(repr(card) for card in self.cards)

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)

    def add_card(self, card):
        """Add a card to the Hand"""
        if self.sort_by == "value":
            key = (Card.VALUES.index(card.value)*4 +
                   Card.SUITS.index(card.suit))
            index = bisect.bisect(self._keys, key)
            self._keys.insert(index, key)
            self.cards.insert(index, card)
        elif self.sort_by == "suit":
            key = (Card.SUITS.index(card.suit)*13 +
                   Card.VALUES.index(card.values))
            index = bisect.bisect(self._keys, key)
            self._keys.insert(index, key)
            self.cards.insert(index, card)
        else:
            raise ValueError("%s is not a valid sorting for a hand" %
                             self.sort_by)

    def sort_by_value(self):
        """Sorts the hand by value"""
        if self.sort_by != "value":
            self.sort_by = "value"

            temp_hand = self.cards
            self.cards = []
            self._keys = []

            for card in temp_hand:
                self.add_card(card)

    def sort_by_suit(self):
        """Sorts the hand by suit"""
        if self.sort_by != "suit":
            self.sort_by = "suit"

            temp_hand = self.cards
            self.cards = []
            self._keys = []

            for card in temp_hand:
                self.add_card(card)

class CardgamePlayer(base.Player):
    """Defines a Player for a card game"""
    def __init__(self, name, term=sys.stdout, hand=None):
        super().__init__(name, term)
        if hand:
            self.hand = hand
        else:
            self.hand = Hand()

class Cardgame(base.Game, metaclass=abc.ABCMeta):
    """Defines a card game"""
    def __init__(self, *players):
        super().__init__(self, *players)
        self.deck = Deck()
        self.hand_size = 5

    def pregame(self):
        """Function exectuted before the main game logic"""
        pass

    @abc.abstractmethod
    def move(self, player):
        """Interface for defining a player's move"""
        pass

    @abc.abstractmethod
    def is_game_over(self):
        """Interface for determining whether the game is over"""
        return False

    def postgame(self):
        """Function exectuted after the main game logic"""
        pass

    def play(self):
        """Defines the flow of execution in a card games"""
        self.pregame()
        self.deck.deal(self.hand_size, self.players)
        player_cycle = itertools.cycle(self.players)
        while not self.is_game_over:
            self.move(player_cycle.next())
        self.postgame()
