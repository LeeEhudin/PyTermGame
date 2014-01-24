"""A module defining functions for playing card games"""

import random
import itertools

class Card(object):
    """Defines a Card class for easy access to a card's suit and value"""
    SUITS = ('spades', 'clubs', 'hearts', 'diamonds')
    VALUES = ('ace', '2', '3', '4', '5', '6', '7', '8', '9', '10',
              'jack', 'queen', 'king')

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        if self.suit == 'spades':
            suit = u'♠'
        elif self.suit == 'clubs':
            suit = u'♣'
        elif self.suit == 'hearts':
            suit = u'♥'
        elif self.suit == 'diamonds':
            suit = u'♦'

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

        return val + suit

class Deck(object):

    def __init__(self, shuffled=True):
        self.deck = [Card(*card) for card in itertools.product(Card.SUITS, Card.VALUES)]
        if shuffled:
            self.shuffle()

    def __repr__(self):
        return ', '.join([str(card) for card in self.deck])

    def __getitem__(self, val):
        return self.deck[val]

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

    def __repr__(self):
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
        return ', '.join([str(card) for card in hand])


