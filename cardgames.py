"""A module defining functions for playing card games"""

import random
import itertools

class Card(object):
    """Defines a Card class for easy access to a card's suit and value"""
    VALUES = ('ace', '2', '3', '4', '5', '6', '7', '8', '9', '10',
              'jack', 'queen', 'king')
    SUITS = ('spades', 'clubs', 'hearts', 'diamonds')

    def __init__(self, value, suit):
        self.value = str(value)
        self.suit = str(suit)

    def __eq__(self, other):
        if isinstance(other, Card) and \
        self.value == other.value and self.suit == other.suit:
            return True
        else:
            return False

    def __str__(self):
        if self.value == 'ace':
            val = 'A'
        elif self.value == 'jack':
            val = 'J'
        elif self.value == 'queen':
            val = 'Q'
        elif self.value == 'king':
            val = 'K'
        else:
            val = self.value

        if self.suit == 'spades':
            suit = '♠'
        elif self.suit == 'clubs':
            suit = '♣'
        elif self.suit == 'hearts':
            suit = '♥'
        elif self.suit == 'diamonds':
            suit = '♦'

        return "{}{}".format(val, suit)

    def __repr__(self):
        return str([self.value, self.suit])

class CardCollection(list):
    def __init__(self, cards=None):
        if cards:
            if isinstance(cards, list):
                super(CardCollection, self).__init__(cards)
            else:
                super(CardCollection, self).__init__([cards])
        else:
            super(CardCollection, self).__init__([])

    def __eq__(self, other):
        if isinstance(other, Card) and len(self) == 1 and self[0] == other:
            return True
        elif isinstance(other, CardCollection) and len(self) == len(other):
            for i in range(len(self)):
                if self[i] != other[i]:
                    return False
            return True
        else:
            return False

    def __str__(self):
        return ', '.join(map(str, self))

    def __repr__(self):
        return super(CardCollection, self).__repr__(list(map(repr, self)))

class Deck(object):

    def __init__(self, shuffled=True):
        self.deck = [Card(*card) \
                     for card in itertools.product(Card.SUITS, Card.VALUES)]
        if shuffled:
            self.shuffle()

    def __repr__(self):
        return ', '.join(map(repr,self.deck))

    def __str__(self):
        return ', '.join(map(str,self.deck))

    def __len__(self):
        return len(self.deck)

    def __getitem__(self, val):
        return self.deck[val]

    def __iter__(self):
        return iter(self.deck)

    def shuffle(self):
        new_deck = []
        while self.deck:
            rand = random.randrange(len(self.deck))
            new_deck.append(self.deck.pop(rand))
        self.deck = new_deck

    def draw(self):
        return self.deck.pop(0)

class Hand(object):

    def __init__(self, initial_cards=None, sort_by_value=True):
        self.cards = {}
        self.sort_by_value = sort_by_value
        self.length = 0

        if initial_cards:
            for card in initial_cards:
                if sort_by_value:
                    if card.value in self.cards:
                        self.cards[card.value][card.suit] = card
                    else:
                        self.cards[card.value] = {card.suit:card}
                else:
                    if card.suit in self.cards:
                        self.cards[card.suit][card.value] = card
                    else:
                        self.cards[card.suit] = {card.value:card}
                self.length += 1

    def __len__(self):
        return self.length

    def __repr__(self):
        return ', '.join(map(repr,self.cards))

    def __str__(self):
        hand = []
        if self.sort_by_value:
            for val in Card.VALUES:
                if val in self.cards:
                    for suit in Card.SUITS:
                        if suit in self.cards[val]:
                            hand.append(self.cards[val][suit])
        else:
            for suit in Card.SUITS:
                if suit in self.cards:
                    for val in Card.VALUES:
                        if val in self.cards[suit]:
                            hand.append(self.cards[suit][val])
        return ', '.join(map(str,hand))
