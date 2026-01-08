# Rock–Paper–Scissors – AI Game Referee

## Overview
This project is a simple AI referee for the Rock–Paper–Scissors-Bomb game. It explains the rules, takes user input, checks if moves are valid, tracks scores and rounds, and automatically ends the game after three rounds.

## State Model
The game state is stored in a single dictionary that tracks the current round, user and bot scores, bomb usage, and whether the game is over. The state is updated only through functions, which keeps the game behavior consistent.

## Agent and Tool Design
The agent acts as a referee that talks to the user and explains each round. Google ADK is used with the **Gemini 2.5 Flash** model to generate round explanations. All game logic such as move validation, winner decision, and state updates is handled using separate functions, keeping logic and conversation separate.

## Output

### Rock–Paper–Scissors
• Game is best of 3 rounds

• Moves: rock, paper, scissors, bomb: once per game

• Bomb beats all; bomb vs bomb is a draw

### Round 1 — Your move: bomb
You played **bomb**, and the bot played **paper**. 

Since bomb beats everything, you won the round.  

Score → You 1 : Bot 0

### Round 2 — Your move: paper
You played **paper**, but the bot played **bomb**, so the bot won this round.  

Score → You 1 : Bot 1

### Round 3 — Your move: rock
You played **rock** and the bot played **paper**. 

Paper beats rock, so the bot won the round. 

Score → You 1 : Bot 2

### GAME OVER
Final Result: **Bot wins**

## Tradeoffs
The game uses a command-line interface instead of a UI to keep things simple. The bot uses random moves instead of a smart strategy, and the game state is stored only in memory, so it resets when the program restarts. Google ADK is used only to generate natural language explanations for each round,

## Future Improvements
With more time, the game could support natural language inputs, use the LLM for smarter bot decisions, allow multiple games in one session, and provide more consistent conversational responses.
