# Blackjack CLI Game

User's goal:
  - _The application user wants to play a single-player card game through the command line_

## How to play

Instructions

## Features

### Existing features

List of existing features

### Future features

List of future features

## Data model

Data model description

## Testing

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
  - [ ] Split does not show additional player hand
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
  - [x] Round ends on player blackjack without checking if dealer has blackjack
  - [ ] Result is push on player blackjack when dealer does not have blackjack
  - [ ] Standing requires key to be pressed twice before revealing dealer cards
  - [x] ~~Hitting on split hand deals card to main hand~~
  - [x] ~~Table shows split card from previous hand at start of new hand~~
  - [x] ~~Split is not permitted when split was previously done in same shoe~~
  - [ ] Stand is permitted when only 1 card dealt to split hand
  - [ ] Split hand stands after 2nd card dealt without permitting hit


## Deployment

Deployed on Heroku

## Credits

  - Design inspiration for the printed card layout from [Stack Exchange answer](https://codereview.stackexchange.com/a/82109), though the code was re-written entirely.
  - Code for joining a string using a different final separator from [Stack Overflow](https://stackoverflow.com/a/30084022/726221)
  - Code for stripping decimals from floats when round from [Stack Overflow](https://stackoverflow.com/questions/2440692/formatting-floats-without-trailing-zeros)