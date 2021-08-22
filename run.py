import random
import math


class Table:
    """
    Holds the player's chip stack and card deck(s).
    Maintains game state and has methods for displaying game status
    to the user.
    """

    def __init__(self, player_stack, num_decks):
        self.player_stack = player_stack
        self.dealer_cards = []
        self.player_cards = []
        self.bet = 0
        self.shoe = Shoe(num_decks)

    def print(self):
        f"Dealer cards: {self.dealer_cards}"
        f"Your cards: {self.player_cards}"
        f"Current bet: {self.bet}"
        f"Chip stack: {self.player_stack}"

    @property
    def player_stack(self):
        return self.player_stack

    @player_stack.setter
    def player_stack(self, v):
        if not (v > 0):
            raise Exception("Player stack must be greater than 0")


class Deck:
    """
    Standard 52 card deck
    """

    card_ranks = [
        '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'
        ]

    card_suits = [
        'c', 'd', 'h', 's'
        ]

    def __init__(self):
        self.cards = range(52)
        random.shuffle(self.cards)

    # card values are in 0-12 indexed array
    # 4 suits of 13 cards, so label index is remainder after dividing by 13
    def get_rank(self, x):
        return self.card_ranks[x % 13]

    # 52 cards in 4 suits, so round down after dividing by 13 for suit
    def get_suit(self, x):
        return self.card_suits[math.floor(x / 13)]

    # pass array of all cards to get the combined value
    def get_hand_value(self, cards):
        hand_value = 0
        ace_count = 0

        for card in cards:
            # Number cards
            if (card % 13) <= 7:
                hand_value += (card % 13 + 2)
            # Ten and face cards
            elif (card % 13) >= 8 and (card % 13) <= 11:
                hand_value += 10
            # Ace
            elif (card % 13) == 12:
                ace_count += 1
                hand_value += 11

        # allow for aces to be 1 or 11
        for _ in range(ace_count):
            if hand_value > 21:
                hand_value -= 10

        # test for blackjack
        if cards.length == 2 and hand_value == 21:
            return [21, True]
        else:
            return [hand_value, False]


class Shoe:
    """
    Contains one or more decks of cards and a cut point that defines when a
    reshuffle (i.e. a new shoe) is needed
    """

    def __init__(self, num_decks):
        self.num_decks = num_decks
        self.cards = []
        for _ in range(self.num_decks):
            new_deck = Deck()
            self.cards += new_deck.cards

    @property
    def num_decks(self):
        return self.num_decks

    @num_decks.setter
    def num_decks(self, v):
        if not (v > 0 and v < 7):
            raise Exception("Number of decks must be between 1 and 6")
