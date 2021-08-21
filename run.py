class Table:
    """
    Holds the player's chip stack and card deck(s).
    Maintains game state and has methods for displaying game status to the user.
    """

    def __init__(self):
        self.player_stack = 1000


class Deck:
    """
    Standard 52 card deck (indexed 0 to 51)
    """

    card_value = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    card_suit = ['C', 'D', 'H', 'S']

    def __init__(self):
        self.cards = range(51)

    def get_value(self, x):
        return x % 4

    def get_suit(self, x):
        return x % 13
