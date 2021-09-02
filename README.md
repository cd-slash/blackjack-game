# Blackjack CLI Game

User's goal:
  - _The application user wants to play a single-player card game through the command line_
  - _The user wants to practice / memorise "perfect" [blackjack strategy](https://wizardofodds.com/games/blackjack/strategy/4-decks/)_

## How to play

The rules of the game are based on standard casino [blackjack](https://en.wikipedia.org/wiki/Blackjack).

Upon loading the game, a blank table is shown with a prompt to enter a bet:

[![Screenshot of board on entering game](https://i.gyazo.com/304e516a0ba2b442d4602f15a7a76234.png)](https://gyazo.com/304e516a0ba2b442d4602f15a7a76234)

After entering a valid bet value, the game will deal 2 cards to the player (both face-up), and 2 cards to the dealer (1 face-up, 1 face-down), with a prompt to take an [action](https://en.wikipedia.org/wiki/Blackjack#Player_decisions) (only valid actions are shown):

[![Screenshot of board after bet](https://i.gyazo.com/fd6c248baac9f96b3395575d62cc88e8.png)](https://gyazo.com/fd6c248baac9f96b3395575d62cc88e8)

Opting to hit will deal another card and prompt again for action (if appropriate, i.e. the extra card did not cause the hand value to be > 21). Stand will end the user's play and reveal the dealer cards, while double will double the original bet (if enough chips are available) in return for 1 additional card only. Split allows 2 cards of equal value to be separated into 2 individual hands, with the bet value of each matching the original bet, if enough chips are available.

[![Screenshot of board after hit](https://i.gyazo.com/a97fb8c80da27a70a721cd2bb8c8498f.png)](https://gyazo.com/a97fb8c80da27a70a721cd2bb8c8498f)

When play is completed, the game will show the result and update the player's chip stack accordingly:

[![Image from Gyazo](https://i.gyazo.com/fd71e6f81008fd885e6c62bf49663a40.png)](https://gyazo.com/fd71e6f81008fd885e6c62bf49663a40)

Play continues until any of the following happen:

 - Player has no chips left
 - Player's chip stack exceeds 999,999
 - The randomly chosen "reshuffle" point is reached

### Blackjack rule variations

Individual casinos [adjust the rules of blackjack](https://en.wikipedia.org/wiki/Blackjack#Rule_variations_and_effects_on_house_edge) to achieve a suitable balance of risk vs. attracting players, since some rules work in favour of the player, while others favour the casino. The optional blackjack rules built into this game are summarised below:

 - Blackjack pays 3:2
 - Dealer stands on soft 17
 - Doubles permitted with any hand value
 - One split permitted with any 2 equally-valued cards
 - No double after split
 - No double-for-less (i.e. double value must match original bet)
 - No blackjack after split
 - Hit permitted after splitting Aces
 - No re-splitting (splitting again after splitting)
 - No check for dealer blackjack until player has acted ("no hole card")
    - Note: although a face-down card is shown for the dealer, it is not consulted until after the player has acted so this is considered a "no hole card" game
 - No Original Bets Only (OBO)
 - No insurance
 - No surrender
 - Dealer cards not revealed on player bust
 - Between 1 and 6 decks per shoe (configurable)

## Features

### Existing features

List of existing features

### Future features

List of future features

## Data model

Each game is transient and state is maintained with in-memory variables only; no persistent data model is used.

Game state is maintained in the `Table` class, which acts as a container for all cards, chip stacks and bets, along with methods for controlling gameplay such as `play_hand()` and functions to assess the outcome of a hand.

## Testing

### Player input

 - [x] Entering a valid bet starts the hand
 - [ ] Bet greater than available chips is rejected
 - [x] Entering non-numeric bet prompts that bet must be a number
 - [ ] User is prompted to press enter to start new hand once each hand ends
 - [ ] Double is not permitted when remaining chip stack < bet value
 - [ ] Split is not permitted when remaining chip stack < bet value
 - [ ] User is shown prompt when action does not match perfect strategy
 - [ ] User can take action not matching perfect strategy by entering same option again
 - [ ] Chevrons are shown to identify active hand after split

### Game play

 - [ ] Player is dealt 2 cards initially
 - [ ] Dealer is dealt 1 face-up card and 1 face-down card initially
 - [ ] `hit` action deals 1 additional card to player
 - [ ] `stand` ends player input and reveals dealer cards
 - [ ] `double` action increments bet by original bet value and deals 1 card only
 - [ ] `split` action moves 1 card to second hand and plays each hand independently
 - [ ] player hand value > 21 ends hand
 - [ ] dealer cards are not revealed when player is bust
 - [ ] Game exits when shuffle point reached
 - [ ] Game exits when chip stack > 999,999
 - [ ] Game exits when chip stack == 0
 - [ ] Game displays reason when exiting

### Hand outcome

 - [ ] Player hand value <= 21 and > dealer hand value is win
 - [ ] Player hand value <= 21 and dealer hand value > 21 is win
 - [ ] Player blackjack and no dealer blackjack is win
 - [ ] Player blackjack and dealer blackjack is push (draw)
 - [ ] Player hand value <= 21 and == dealer hand value is push
 - [ ] Player hand value <= 21 and < dealer hand value is loss
 - [ ] Player hand value > 21 is loss
 - [ ] Player hand value <= 21 and dealer blackjack is loss
 - [ ] Player hand value > 21 and dealer hand value > 21 is not observed
 - [ ] Message bar shows hand result once complete
 - [ ] 2 message bars show result of each hand after split hand is complete

### After hand

 - [ ] `Bet * 2` is added to chip stack on win
 - [ ] `Bet * 3` is added to chip stack on win after doubling
 - [ ] No value added to chip stack on loss
 - [ ] `Bet` is added to chip stack on push
 - [ ] Chip stack is updated according to tests above for each hand independently after split

### Linter

Linter testing details

### Validator

### Checklists

Checklists for testing features

### Bugs

  - [x] ~~2 of clubs is index 0 so is falsy and interpreted as face down card by print function~~
  - [x] ~~Game requests user press any key for next hand, but spacebar does not trigger new hand~~
  - [x] ~~Betting full value of chip stack throws error (stack must be greater than 0)~~
  - [x] ~~Entering invalid key for action during hand causes crash~~
  - [x] ~~User is prompted to split when that is not a valid action~~
  - [x] ~~User is prompted to double when that is not a valid action~~
  - [x] ~~Double is possible after additional cards have been dealt, but should not be~~
  - [x] ~~Double key is active when double is not shown as an available option~~
  - [x] ~~Double is shown as available option when player has insufficient chips to double~~
  - [x] ~~Split does not show additional player hand~~
  - [x] ~~Player stack > 999999 causes print overflow~~
  - [x] ~~Double increases bet but does not remove incremental value from stack~~
  - [x] ~~Double causes crash when doubled bet value > remaining stack~~
  - [x] Input is requested when player has blackjack and dealer does not (hand should be over)
  - [x] ~~Status message displays decimal on round number when winning with blackjack~~
  - [x] ~~Player stack shows decimal when round number after winning with blackjack~~
  - [x] ~~Game exits without warning when shoe reshuffle point is hit~~
  - [x] ~~Game crashes if bet > stack is entered~~
  - [x] ~~No input when bet requested results in `invalid literal for int() with base 10: ''` error message~~
  - [x] ~~`IndexError: list index out of range` when concatenating `action_request_string`~~
  - [x] ~~Round ends on player blackjack without checking if dealer has blackjack~~
  - [x] ~~Result is push on player blackjack when dealer does not have blackjack~~
  - [x] ~~Standing requires key to be pressed twice before revealing dealer cards~~
  - [x] ~~Hitting on split hand deals card to main hand~~
  - [x] ~~Table shows split card from previous hand at start of new hand~~
  - [x] ~~Split is not permitted when split was previously done in same shoe~~
  - [x] ~~Stand is permitted when only 1 card dealt to split hand~~
  - [x] ~~Split hand stands after 2nd card dealt without permitting hit~~
  - [x] ~~Player can have blackjack after split, but should only have 21~~
  - [x] ~~Not obvious which hand messages are referring to after split~~
  - [x] ~~2 cards are dealt when hitting on split hand~~
  - [x] ~~Main hand labelled as blackjack and input stopped after split~~
  - [x] ~~`Press Enter for new hand` message duplicated after split~~
  - [x] ~~Optimal strategy advises splitting 5s~~
  - [x] ~~Optimal strategy advises splitting 10s~~
  - [x] ~~Optimal strategy advises hitting with 3s against dealer 5~~
  - [x] ~~Dealer cards are revealed after player is bust~~
  - [x] ~~List index error when concatenating action string when standing on split hand~~
  - [x] ~~Optimal strategy suggests standing on split hand with 10 vs Ace~~


## Deployment

Deployed on Heroku

## Credits

  - Design inspiration for the printed card layout from [Stack Exchange answer](https://codereview.stackexchange.com/a/82109), though the code was re-written entirely.
  - Code for joining a string using a different final separator from [Stack Overflow](https://stackoverflow.com/a/30084022/726221)
  - Code for stripping decimals from floats when round from [Stack Overflow](https://stackoverflow.com/questions/2440692/formatting-floats-without-trailing-zeros)
  - Optimal blackjack strategy table from [Wizard of Odds](https://wizardofodds.com/games/blackjack/strategy/4-decks/)
