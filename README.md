# Rock–Paper–Scissors – AI Game Referee

## Overview
This project is a simple AI referee for the Rock–Paper–Scissors game. The system explains the rules, takes user input, checks if moves are valid, keeps track of scores and rounds, and ends the game automatically after three rounds.

## State Model
The game state is stored in a single dictionary that keeps track of the current round, user and bot scores, bomb usage, and whether the game is over. The state is updated only through functions, not through prompts, so the game behaves consistently across turns.

## Agent and Tool Design
The agent acts as a referee that interacts with the user and explains what happens in each round. The actual game logic is handled using tools such as move validation, round resolution, and state updates. This keeps the logic separate from the conversation.

## Output

### Round 1 — Your move: rock

You played: rock

Bot played: rock

Round result: draw (Same move)

Score → You 0 : Bot 0

### Round 2 — Your move: papwe

Invalid move. Round wasted.

### Round 3 — Your move: bomb

You played: bomb

Bot played: rock

Round result: user (Bomb beats everything)

Score → You 1 : Bot 0

### GAME OVER

Final Result: You win


## Tradeoffs
The game runs in a command-line interface instead of a UI to keep the implementation simple. The bot uses random moves instead of an intelligent strategy to avoid unnecessary complexity.

## Future Improvements
With more time, the following improvements i  could add like 
* Support for natural language inputs like “I choose rock”
* A smarter bot strategy using the LLM instead of random moves
* Option to play multiple games in one session
* Better conversational responses

