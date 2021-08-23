import random
import math
import os


class Table:
    """
    Holds the player's chip stack and card deck(s).
    Maintains game state and has methods for displaying game status
    to the user.
    """

    def __init__(self, player_stack, num_decks):
        self.player_stack = player_stack
        self.shoe = Shoe(num_decks)
        self.reshuffle = False

    def print(self):
        dealer_card_images = [Deck.print_card(card) for card in self.dealer_cards]
        player_card_images = [Deck.print_card(card) for card in self.player_cards]

        # top border row; total width = 65 characters
        view = [f'┌{"".join(["-"] * 63)}┐']
        # dealer status and cards
        view += f'|<-- Dealer: {evaluate_hand(self.dealer_cards)["value"]} -->'
        for row in range(5):
            view += f'|{"".join([image[row] for image in dealer_card_images])}'
        # player status and cards
        view += f'|<-- Player: {evaluate_hand(self.player_cards)["value"]} -->'
        for row in range(5):
            view += f'|{"".join([image[row] for image in player_card_images])}'
        # current bet and chip stack with spacer rows
        view += '|'
        view += f'|<--  Current bet: {self.bet}     |     Remaining chips: {self.player_stack}  -->'
        view += '|'
        # message row
        # if spacer length is an odd number, add 1 extra block to right spacer
        spacer_left = math.floor(63 - len(self.status_message)) / 2
        spacer_right = math.ceil(63 - len(self.status_message)) / 2
        view += f'|{"".join(["░"] * spacer_left}{self.status_message}{"".join(["░"] * spacer_right)}'
        # bottom border row
        view = [f'└{"".join(["-"] * 63)}┘']

        # clear the screen and print the new view
        os.system('clear')
        print("\n".join(view))

    def print_cards(self):
        print(f"Dealer cards: {[Deck.get_label(card) for card in self.dealer_cards]}: {evaluate_hand(self.dealer_cards)['value']}")
        print(f"Your cards: {[Deck.get_label(card) for card in self.player_cards]}: {evaluate_hand(self.player_cards)['value']}")

    def print_bet(self):
        print(f"Current bet: {self.bet}")
        print(f"Chip stack: {self.player_stack}")

    def process_result(self):
        """
        Once all actions have been taken, determine if the player
        won or lost the hand and update their stack accordingly
        """
        player_hand_evaluation = evaluate_hand(self.player_cards)
        dealer_hand_evaluation = evaluate_hand(self.dealer_cards)
        player_hand_value = player_hand_evaluation['value']
        dealer_hand_value = dealer_hand_evaluation['value']
        player_blackjack = player_hand_evaluation['blackjack']
        dealer_blackjack = dealer_hand_evaluation['blackjack']

        # player has blackjack, dealer does not: winnings are 1.5x bet
        # note: bet is also returned when player wins so bet is * 2.5 not 1.5
        if player_blackjack and not dealer_blackjack:
            winnings = self.bet * 2.5
            self.player_stack += winnings
            print(f"Blackjack! You won {winnings}")
            return

        # player is not bust
        if player_hand_value <= 21:
            # player hand beats dealer or dealer is bust
            if player_hand_value > dealer_hand_value or dealer_hand_value > 21:
                winnings = self.bet * 2
                self.player_stack += winnings
                print(f"You won {winnings}!")
                return
            # tie: return the bet only
            if (not dealer_blackjack and
                (player_hand_value == dealer_hand_value)) or (
                    player_blackjack and dealer_blackjack):
                self.player_stack += self.bet
                print(f"push: returning {self.bet} bet")
                return

        # if function gets to here, dealer has won
        print("Dealer won :-(")

    def reveal_dealer_cards(self):
        # deal 1 additional dealer card, since dealer already has one
        self.dealer_cards += [self.shoe.cards.pop()]
        # check for blackjack
        if evaluate_hand(self.dealer_cards)['blackjack']:
            return
        # continue drawing cards until dealer has > 17
        while evaluate_hand(self.dealer_cards)['value'] < 17:
            self.dealer_cards += [self.shoe.cards.pop()]

    def process_action(self, key):
        # h = hit, s = stick, d = double, 2 = split
        if key == 'h':
            self.player_cards += [self.shoe.cards.pop()]
        if key == 's':
            self.player_input_ended = True
        if key == 'd':
            self.bet += self.bet
            self.player_cards += [self.shoe.cards.pop()]
            self.player_input_ended = True

    def play_hand(self):
        self.player_bust = False
        self.player_input_ended = False
        # set the bet first to ensure valid before subtracting from stack
        self.bet = int(input(
            f'You have {str(self.player_stack)} chips. How much would you like to bet on this hand? '
            ))
        self.player_stack -= self.bet
        # deal 2 cards to player and 1 to dealer
        self.dealer_cards = []
        self.player_cards = []
        self.player_cards += [self.shoe.cards.pop(), self.shoe.cards.pop()]
        self.dealer_cards += [self.shoe.cards.pop()]
        # get player action
        while not self.player_input_ended:
            os.system('clear')
            self.print_bet()
            self.print_cards()
            action_request_string = 'Hit (h), Stick (s), Double (d) or Split (2)? '
            # Loop will run until valid input is entered to trigger break
            while True:
                try:
                    action = input(action_request_string)
                    break
                except ValueError:
                    print("invalid action - please try again...")
            if action in ['h', 's', 'd', '2']:
                self.process_action(action)
            else:
                print("invalid action! Please press h, s, d or 2...")
            # end the hand if player is bust
            if evaluate_hand(self.player_cards)['value'] > 21:
                self.player_input_ended = True
                self.player_bust = True
        # only deal additional dealer cards if player is not bust
        if not self.player_bust:
            self.reveal_dealer_cards()
        os.system('clear')
        print("All cards dealt - hand complete")
        self.print_cards()
        self.process_result()
        if len(self.shoe.cards) < self.shoe.reshuffle_point:
            self.reshuffle = True

    @property
    def player_stack(self):
        return self._player_stack

    @player_stack.setter
    def player_stack(self, v):
        if not (v > 0):
            raise ValueError("Player stack must be greater than 0")
        else:
            self._player_stack = v

    @property
    def bet(self):
        return self._bet

    @bet.setter
    def bet(self, v):
        if not (v > 0):
            raise ValueError("Bet must be greater than 0")
        elif not (v <= self.player_stack):
            raise ValueError("Bet must not be larger than remaining chips")
        else:
            self._bet = v


class Deck:
    """
    Standard 52 card deck
    """

    card_ranks = [
        '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'
        ]

    card_suits = [
        '♣', '♦', '♥', '♠'
        ]

    def __init__(self):
        self.cards = list(range(52))
        random.shuffle(self.cards)

    # card values are in 0-12 indexed array
    # 4 suits of 13 cards, so label index is remainder after dividing by 13
    @staticmethod
    def get_rank(x):
        return Deck.card_ranks[x % 13]

    # 52 cards in 4 suits, so round down after dividing by 13 for suit
    @staticmethod
    def get_suit(x):
        return Deck.card_suits[math.floor(x / 13)]

    # combined rank and suit, e.g. As or 4d
    @staticmethod
    def get_label(x):
        return f"{Deck.get_rank(x)}{Deck.get_suit(x)}"

    # print an ascii representation of a card
    @staticmethod
    def print_card(card):
        r = Deck.get_rank(card)
        s = Deck.get_suit(card)
        # add a spacer if rank is a single character
        p = '' if r == '10' else ' '

        card_list = '┌─────┐'
        # card value is specified
        if card:
            card_list += f'│{r}{s}{p}  │'
            card_list += '│     │'
            card_list += f'│   {p}{r}{s}│'
        # no card value, i.e. card is face-down
        else:
            card_list += ['│░░░░░│'] * 3
        card_list += '└─────┘'

        return card_list


class Shoe:
    """
    Contains one or more decks of cards and a cut point that defines when a
    reshuffle (i.e. a new shoe) is needed
    """

    def __init__(self, num_decks=6):
        self.num_decks = num_decks
        self.cards = []
        for _ in range(self.num_decks):
            new_deck = Deck()
            self.cards += new_deck.cards
        self.reshuffle_point = random.randint(30, 52 * num_decks)

    @property
    def num_decks(self):
        return self._num_decks

    @num_decks.setter
    def num_decks(self, v):
        if not (v > 0 and v < 7):
            raise ValueError("Number of decks must be between 1 and 6")
        else:
            self._num_decks = v


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
    if len(cards) == 2 and hand_value == 21:
        return {'value': 21, 'blackjack': True}
    else:
        return {'value': hand_value, 'blackjack': False}


# Create a new table and play until player has no chips or
# shoe hits reshuffle marker
table = Table(1000, 6)
while table.player_stack > 0 and not table.reshuffle:
    table.play_hand()
