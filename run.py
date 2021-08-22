import random
import math
import keyboard


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

    def process_result(self):
        """
        Once all actions have been taken, determine if the player
        won or lost the hand and update their stack accordingly
        """
        player_hand_evaluation = evaluate_hand(self.player_cards)['value']
        dealer_hand_evaluation = evaluate_hand(self.dealer_cards)['value']
        player_hand_value = player_hand_evaluation['value']
        dealer_hand_value = dealer_hand_evaluation['value']
        player_blackjack = player_hand_evaluation['blackjack']
        dealer_blackjack = dealer_hand_evaluation['blackjack']

        # player has blackjack, dealer does not: winnings are 1.5x bet
        # note: bet is also returned when player wins so bet is * 2.5 not 1.5
        if player_blackjack and not dealer_blackjack:
            self.player_stack += self.bet * 2.5
            return

        # player is not bust
        if player_hand_value <= 21:
            # player hand beats dealer or dealer is bust
            if player_hand_value > dealer_hand_value or dealer_hand_value > 21:
                self.player_stack += self.bet * 2
                return
            # tie: return the bet only
            if (not dealer_blackjack and
                (player_hand_value == dealer_hand_value)) or (
                    player_blackjack and dealer_blackjack):
                self.player_stack += self.bet

    def play_hand(self, bet):
        self.player_input_ended = False
        # set the bet first to ensure valid before subtracting from stack
        self.bet = bet
        self.player_stack -= self.bet
        # deal 2 cards to player and 1 to dealer
        self.player_cards += self.shoe.cards.pop(2)
        self.dealer_cards += self.shoe.cards.pop()
        # get player action
        while not self.player_input_ended:
            self.print()
            key_pressed = keyboard.read_key()
            if key_pressed in ['h', 's', 'd', '2']:
                self.process_action(input(key_pressed))
            else:
                print("invalid key!")
            # end the hand if player is bust
            if evaluate_hand(self.player_cards)['value'] > 21:
                self.player_input_ended = True


    def process_action(self, key):
        # h = hit, s = stick, d = double, 2 = split
        if key == 'h':
            self.player_cards += self.shoe.cards.pop()
        if key == 's':
            self.player_input_ended = True
        if key == 'd':
            self.bet += self.bet
            self.player_cards += self.shoe.cards.pop()
            self.player_input_ended = True


    @property
    def player_stack(self):
        return self.player_stack

    @player_stack.setter
    def player_stack(self, v):
        if not (v > 0):
            raise Exception("Player stack must be greater than 0")

    @property
    def bet(self):
        return self.bet

    @bet.setter
    def bet(self, v):
        if not (v > 0):
            raise Exception("Bet must be greater than 0")
        if not (v <= self.player_stack):
            raise Exception("Bet must not be larger than remaining chips")


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


def evaluate_hand(cards):
    """
    Evaluate the value of a full hand by passing in an array of cards
    """
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
        return {'value': 21, 'blackjack': True}
    else:
        return {'value': hand_value, 'blackjack': False}
