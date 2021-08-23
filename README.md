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
  - [ ] Betting full value of chip stack throws error (stack must be greater than 0)
  - [ ] Entering invalid key for action during hand causes crash
  - [ ] User is prompted to split when that is not a valid action
  - [ ] User is prompted to double when that is not a valid action
  - [ ] Split does not show additional player hand
  - [ ] Player stack > 999999 causes print overflow


## Deployment

Deployed on Heroku

## Credits

  - Design inspiration for the printed card layout from [Stack Exchange answer](https://codereview.stackexchange.com/a/82109), though the code was re-written entirely.