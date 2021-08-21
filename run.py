class Table:
    """
    Primary class for all Blackjack logic.
    Holds the player's chip stack and card deck(s).
    Maintains game state and has methods for displaying game status to the user.
    """

    def __init__(self):
        self.player_stack = 1000


class Deck:
    """
    Standard 52 card deck (indexed 0 to 51)
    """

    def __init__(self):
        self.cards = range(51)