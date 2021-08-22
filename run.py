class Table:
    """
    Holds the player's chip stack and card deck(s).
    Maintains game state and has methods for displaying game status to the user.
    """

    def __init__(self):
        self.player_stack = 1000


class Deck:
    """
    Standard 52 card deck
    """

    card_values = [
        '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'
        ]

    card_suits = [
        'C', 'D', 'H', 'S'
        ]

    def __init__(self):
        self.cards = range(52)
        random.shuffle(self.cards)

    # card values are in 0-12 indexed array
    # 4 suits of 13 cards, so value is remainder after dividing by 13
    def get_value(self, x):
        return self.card_values[x % 13]

    # 52 cards in 4 suits, so round down after dividing by 13 for suit
    def get_suit(self, x):
        return self.card_suits[math.floor(x / 13)]


class Shoe:
    """
    Contains one or more decks of cards and a cut point that defines when a
    reshuffle (i.e. a new shoe) is needed
    """

    def __init__(self, num_decks):
        self.cards = []
        for _ in range(num_decks):
            new_deck = Deck()
            self.cards += new_deck.cards
