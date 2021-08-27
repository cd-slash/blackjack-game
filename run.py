import random
import math
import os


def round_float(x):
    if '.' in str(x):
        return str(x).rstrip("0").rstrip(".")
    else:
        return x


class Table:
    """
    Holds the player's chip stack and card deck(s).
    Maintains game state and has methods for displaying game status
    to the user.
    """

    def __init__(self, player_stack, num_decks=6):
        self.player_stack = player_stack
        self.shoe = Shoe(num_decks)
        self.reshuffle = False
        self.dealer_cards = []
        self.player_cards = []
        self.split_cards = []
        # give bet an intial value to avoid bet <= 0 error
        self.bet = 1
        self.bet_placed = False

    def print(self, messages, columns=65):
        dealer_card_images = [Deck.print_card(card) for card in self.dealer_cards]
        # add a face down card for the dealer if only 1 dealer card dealt
        if len(self.dealer_cards) == 1:
            dealer_card_images += [Deck.print_card()]
        player_card_images = [Deck.print_card(card) for card in self.player_cards]

        view = []
        # dealer status and cards
        dealer_hand_rank = evaluate_hand(self.dealer_cards)
        dealer_hand_label = "Blackjack" if dealer_hand_rank['blackjack'] else dealer_hand_rank['value']
        view += [f'|<-- Dealer: {dealer_hand_label} -->']
        for row in range(5):
            view += [f'|{"".join([image[row] for image in dealer_card_images])}']
        # player status and cards
        player_hand_rank = evaluate_hand(self.player_cards)
        player_hand_label = "Blackjack" if player_hand_rank['blackjack'] else player_hand_rank['value']
        if self.bet_placed:
            view += [f'|<-- Player: {player_hand_label} | Bet: {round_float(self.bet)} -->']
        else:
            view += [f'|<-- Player: {player_hand_label} -->']
        # print all cards row-by-row
        for row in range(5):
            row_string = [f'|{"".join([image[row] for image in player_card_images])}']
            # marker if primary hand is active and there's a split
            if self.split_cards and row in [1, 2, 3] and not self.player_input_ended:
                row_string[0] += f'{"".join([" " * (columns - 5 - len(row_string[0]))])}<<<<'
            view += row_string
        # second row of player cards if there's a split
        if self.split_cards:
            split_hand_rank = evaluate_hand(self.split_cards)
            # split hand can't be blackjack, so always display numeric value
            split_hand_label = split_hand_rank['value']
            view += [f'|<-- Player split: {split_hand_label} | Bet: {round_float(self.split_bet)} -->']
            split_card_images = [Deck.print_card(card) for card in self.split_cards]
            for row in range(5):
                row_string = [f'|{"".join([image[row] for image in split_card_images])}']
                # marker if split hand is active
                if self.player_input_ended and row in [1, 2, 3] and not self.split_input_ended:
                    row_string[0] += f'{"".join([" " * (columns - 5 - len(row_string[0]))])}<<<<'
                view += row_string
        # current bet and chip stack with spacer rows
        view += ['|']
        bet_spacer = "".join([' ' * (6 - len(str(round_float(self.bet))))])
        stack_spacer = "".join([' ' * (6 - len(str(round_float(self.player_stack))))])
        # strip decimal from stack value if round number
        if self.bet_placed:
            view += [f'|<--   Total bet: {bet_spacer}{round_float(self.bet)}  -->|<--  Remaining chips: {stack_spacer}{round_float(self.player_stack)}   -->']
        else:
            view += [f'|<--     No bet placed     -->|<--  Remaining chips: {stack_spacer}{round_float(self.player_stack)}  -->']
        view += ['|']
        # message rows; if spacer length is an odd number, add 1 extra block to right spacer
        for message in messages:
            spacer_left = int(math.floor(((columns - 2) - len(message)) / 2) - 1)
            spacer_right = int(math.ceil(((columns - 2) - len(message)) / 2) - 1)
            view += [f'|{"".join(["░"] * spacer_left)} {message} {"".join(["░"] * spacer_right)}']
        # create a new list for printing and add top border
        print_view = [f'┌{"".join(["-"] * (columns - 2))}┐']
        # add right border with spacers to all but first and last rows
        for row in view:
            spacers = "".join([" " * ((columns - 1) - len(row))])
            print_view += [f'{row}{spacers}|']
        # bottom border
        print_view += [f'└{"".join(["-"] * (columns - 2))}┘']

        # clear the screen and print the new view
        os.system('clear')
        print("\n".join(print_view))

    def process_result(self, cards, bet):
        """
        Once all actions have been taken, determine if the player
        won or lost the hand and update their stack accordingly
        """
        player_hand_evaluation = evaluate_hand(cards)
        dealer_hand_evaluation = evaluate_hand(self.dealer_cards)
        player_hand_value = player_hand_evaluation['value']
        dealer_hand_value = dealer_hand_evaluation['value']
        player_blackjack = player_hand_evaluation['blackjack']
        dealer_blackjack = dealer_hand_evaluation['blackjack']

        # player has blackjack, dealer does not and no split: winnings are 1.5x bet
        # note: bet is also returned when player wins so bet is * 2.5 not 1.5
        if player_blackjack and not dealer_blackjack and not self.split_cards:
            winnings = bet * 2.5
            """
            remove decimal if winnings is a round number
            source: https://stackoverflow.com/questions/2440692/formatting-floats-without-trailing-zeros
            """
            return {
                'result_string': f'Blackjack! You won {round_float(winnings)}. Press Enter for new hand.',
                'winnings': winnings
            }

        # player is not bust
        if player_hand_value <= 21:
            # player hand beats dealer or dealer is bust
            if player_hand_value > dealer_hand_value or dealer_hand_value > 21:
                winnings = bet * 2
                return {
                    'result_string': f'You won {round_float(winnings)}! Press Enter for new hand.',
                    'winnings': winnings
                }

            # tie: return the bet only
            if (not dealer_blackjack and
                (player_hand_value == dealer_hand_value)) or (
                    player_blackjack and dealer_blackjack):
                winnings = bet
                return {
                    'result_string': f'Push: returning {round_float(bet)} bet. Press Enter for new hand.',
                    'winnings': winnings
                }

        # if function gets to here, dealer has won
        return {
            'result_string': 'Dealer won :-( Press Enter for new hand.',
            'winnings': 0
        }

    def reveal_dealer_cards(self):
        # deal 1 additional dealer card, since dealer already has one
        self.dealer_cards += [self.shoe.cards.pop()]
        # check for dealer or player blackjack
        if evaluate_hand(self.dealer_cards)['blackjack'] or evaluate_hand(self.player_cards)['blackjack']:
            return
        # continue drawing cards until dealer has > 17
        while evaluate_hand(self.dealer_cards)['value'] < 17:
            self.dealer_cards += [self.shoe.cards.pop()]

    def action_permitted(self, action, split_hand=False):
        """
        Returns True or False indicating if the action
        passed in (hit, stand, double or split) is permitted
        """
        if split_hand:
            # no split hand actions permitted if main hand still active
            # or no split hand input required
            if not self.player_input_ended or self.split_input_ended:
                return False
        else:
            # no main hand actions permitted if input ended
            if self.player_input_ended:
                return False
        # no actions permitted if player has blackjack
        # no blackjack permitted after split
        if evaluate_hand(self.player_cards)['blackjack'] and not self.split_cards:
            return False
        # hit and stand allowed except when player has blackjack or input ended
        if (action == 'hit' or action == 'stand'):
            return True
        # double allowed as first action only, and not after split
        elif (action == 'double' and
                len(self.player_cards) == 2 and
                not self.split_cards and
                self.player_stack >= self.bet):
            return True
        # split allowed only as first action, when cards have equal rank,
        # when enough chips are available to split, and when split hasn't
        # already happened
        elif (action == 'split' and
                not self.split_cards and
                len(self.player_cards) == 2 and
                Deck.get_value(self.player_cards[0]) == Deck.get_value(self.player_cards[1]) and
                self.player_stack >= self.bet):
            return True
        else:
            return False

    def actions_permitted(self, **kwargs):
        # set the variables if they were passed in as keyword args
        split_hand = kwargs['split_hand'] if 'split_hand' in kwargs else False
        req_str = kwargs['req_str'] if 'req_str' in kwargs else False
        action_list = []
        if self.action_permitted('hit', split_hand):
            # append the key prompt if returning the request string
            action_list += [f'hit{" (h)" if req_str else ""}']
        if self.action_permitted('stand', split_hand):
            action_list += [f'stand{" (s)" if req_str else ""}']
        if self.action_permitted('double', split_hand):
            action_list += [f'double{" (d)" if req_str else ""}']
        if self.action_permitted('split', split_hand):
            action_list += [f'split{" (2)" if req_str else ""}']

        if req_str:
            """
            Join the actions together into a comma-separated string but
            join last 2 words with ' and '
            source: https://stackoverflow.com/a/30084022/726221
            """
            action_request_string = f'{" or ".join([", ".join(action_list[:-1]),action_list[-1]])}?'
            return [action_request_string.capitalize()]
        else:
            return action_list

    def process_action(self, key, split=False):
        actions_permitted = self.actions_permitted(split_hand=split)
        # h = hit, s = stick, d = double, 2 = split
        if key == 'h':
            if split:
                self.split_cards += [self.shoe.cards.pop()]
            else:
                self.player_cards += [self.shoe.cards.pop()]
            return
        elif key == 's':
            if split:
                self.split_input_ended = True
            else:
                self.player_input_ended = True
            return
        elif key == 'd' and 'double' in actions_permitted:
            # new variable to avoid risk of changing bet then using it
            incremental_bet = self.bet
            # increase bet first to avoid value error because bet > stack
            self.bet += incremental_bet
            self.player_stack -= incremental_bet
            self.player_cards += [self.shoe.cards.pop()]
            self.player_input_ended = True
            return
        elif key == '2' and 'split' in actions_permitted:
            # set a flag to get user actions on the split hand
            self.split_input_ended = False
            # create a second bet pot
            self.split_bet = self.bet
            self.player_stack -= self.split_bet
            # move one card to the split hand and deal a second card to the main hand
            self.split_cards += [self.player_cards.pop()]
            self.player_cards += [self.shoe.cards.pop()]

    def play_hand(self):
        self.player_input_ended = False
        # Don't prompt for action on split hand
        self.split_input_ended = True
        self.bet_placed = False
        self.player_cards = []
        self.dealer_cards = []
        self.split_cards = []
        bet_request_string = f'How much would you like to bet? (max. {round_float(self.player_stack)})'
        self.print([bet_request_string])
        while not self.bet_placed:
            try:
                self.bet = input()
                self.player_stack -= self.bet
                self.bet_placed = True
            except ValueError as error_message:
                self.print([bet_request_string, str(error_message)])
        # deal 2 cards to player and 1 to dealer
        self.dealer_cards = []
        self.player_cards = []
        self.player_cards += [self.shoe.cards.pop(), self.shoe.cards.pop()]
        self.dealer_cards += [self.shoe.cards.pop()]
        # get player action
        while not self.player_input_ended or not self.split_input_ended:
            # Loop will run until valid input is entered to trigger break
            # or no actions are permitted
            while self.actions_permitted():
                req_str = self.actions_permitted(req_str=True)
                self.print(req_str)
                try:
                    action = input()
                    self.process_action(action)
                    break
                except ValueError as error_message:
                    # ignores invalid keypress, but prints an error e.g. bet exceeds stack
                    self.print([req_str, str(error_message)])
            # end the hand if player is bust or player has blackjack
            player_hand = evaluate_hand(self.player_cards)
            if player_hand['value'] > 21 or player_hand['blackjack']:
                self.player_input_ended = True
            while self.actions_permitted(split_hand=True):
                # deal second card to split hand initially
                if len(self.split_cards) == 1:
                    self.split_cards += [self.shoe.cards.pop()]
                req_str = self.actions_permitted(split_hand=True, req_str=True)
                self.print(req_str)
                try:
                    action = input()
                    self.process_action(action, True)
                    break
                except ValueError as error_message:
                    # ignores invalid keypress, but prints an error e.g. bet exceeds stack
                    self.print([req_str, str(error_message)])
            # end main hand if bust or blackjack
            player_hand = evaluate_hand(self.player_cards)
            if player_hand['value'] > 21 or (player_hand['blackjack'] and not self.split_cards):
                self.player_input_ended = True
            # end split hand if bust (no blackjack after split)
            if evaluate_hand(self.split_cards)['value'] > 21:
                self.split_input_ended = True
        # deal additional dealer cards if main hand or split hand is not bust
        if evaluate_hand(self.player_cards)['value'] <= 21 or evaluate_hand(self.split_cards)['value'] <= 21:
            self.reveal_dealer_cards()
        result = self.process_result(self.player_cards, self.bet)
        self.player_stack += result['winnings']
        if self.split_cards:
            split_result = self.process_result(self.split_cards, self.split_bet)
            self.player_stack += split_result['winnings']
            self.print([f'Hand 1: {result["result_string"]}', f'Hand 2: {split_result["result_string"]}'])
        else:
            self.print([result['result_string']])
        # wait for key before moving to next hand
        input()
        # trigger game exit if shoe is at or beyond reshuffle point
        if len(self.shoe.cards) < self.shoe.reshuffle_point:
            self.reshuffle = True

    @property
    def player_stack(self):
        return self._player_stack

    @player_stack.setter
    def player_stack(self, v):
        if v < 0 or v > 999999:
            raise ValueError("Player stack must be between 0 and 999999")
        else:
            self._player_stack = v

    @property
    def bet(self):
        return self._bet

    @bet.setter
    def bet(self, v):
        try:
            bet_input = float(v)
        except ValueError:
            raise ValueError("Bet must be a number")
        if (bet_input <= 0):
            raise ValueError("Bet must be greater than 0")
        elif (bet_input > self.player_stack):
            if self.bet_placed and (bet_input - self.bet) <= self.player_stack:
                self._bet = bet_input
            else:
                raise ValueError("Bet must not be larger than remaining chips")
        else:
            self._bet = bet_input


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

    # Blackjack card value (i.e. 10 for all face cards)
    @staticmethod
    def get_value(card):
        # Number cards
        if (card % 13) <= 7:
            return (card % 13) + 2
        # Ten and face cards
        elif (card % 13) >= 8 and (card % 13) <= 11:
            return 10
        # Ace
        elif (card % 13) == 12:
            return 11

    # print an ascii representation of a card
    @staticmethod
    def print_card(card=-1):
        r = Deck.get_rank(card)
        s = Deck.get_suit(card)
        # add a spacer if rank is a single character
        p = '' if r == '10' else ' '

        print_list = ['┌─────┐']
        # card value is specified
        if card >= 0:
            print_list += [f'│{r}{s}{p}  │']
            print_list += ['│     │']
            print_list += [f'│  {p}{r}{s}│']
        # no card value, i.e. card is face-down
        else:
            print_list += ['│░░░░░│'] * 3
        print_list += ['└─────┘']

        return print_list


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
        card_value = Deck.get_value(card)
        hand_value += card_value
        if card_value == 11:
            ace_count += 1

    # allow for aces to be 1 or 11
    for _ in range(ace_count):
        if hand_value > 21:
            hand_value -= 10

    # test for blackjack
    if len(cards) == 2 and hand_value == 21:
        return {'value': 21, 'blackjack': True}
    else:
        return {'value': hand_value, 'blackjack': False}


# Create a new table and play until player has no chips,
# >= 1m chips, or shoe hits reshuffle marker
table = Table(1000, 6)
while True:
    table.play_hand()
    if table.player_stack <= 0:
        table.print(['Exiting: out of chips'])
        break
    if table.player_stack > 999999:
        table.print(['Exiting: stack >= 1,000,000 - you win!'])
        break
    if table.reshuffle:
        table.print(['Exiting: shoe hit resuffle point'])
        break
