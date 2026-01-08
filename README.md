# Rock–Paper–Scissors–Plus — AI Game Referee

## Overview
This project is a simple AI referee for the Rock–Paper–Scissors–Plus game.  
The referee explains the rules, accepts user moves, checks validity, tracks scores and rounds, and decides the winner automatically after three rounds. The game runs in a conversational, CLI-based format and handles invalid inputs gracefully.

---

## State Model
The game uses a single persistent in-memory state dictionary to track progress across turns.  

The state includes:
- Current round number  
- User and bot scores  
- Whether the user or bot has already used the `bomb` move  
- Whether the game is over  

This state is **not stored in the prompt**. It is updated only through dedicated tool functions, which ensures predictable behavior and makes the logic easy to debug.

---

## Agent and Tool Design
The system separates responsibilities clearly:

### Agent (Referee)
- Explains the game rules briefly
- Prompts the user for input
- Interprets the user’s intent
- Orchestrates calls to tools
- Explains the outcome of each round and the final result

The agent does not contain game rules or directly modify state.

### Tools (Game Logic)
Three explicit tools are used:
- `validate_move`: checks if a move is valid and enforces one-time bomb usage  
- `resolve_round`: decides the winner of a round based on the rules  
- `update_game_state`: updates rounds, scores, bomb usage, and game completion  

All rule enforcement and state updates happen inside these tools.

---

## Tradeoffs Made
- A **CLI interface** was used instead of a UI to keep the focus on logic and agent design.
- The bot uses a **simple random strategy** instead of LLM-based reasoning to ensure correctness and avoid unnecessary complexity.
- A **single-agent design** was chosen since multiple agents were not required for this scope.
- The program fails early if the API key is missing to encourage secure configuration practices.

---

## Future Improvements
With more time, the following improvements could be added:
- Natural language input handling (e.g., “I choose rock”)
- Smarter bot strategy using the LLM
- Structured JSON responses for easier frontend or chat integration
- Support for multiple games in one session
- Streaming responses for a more conversational experience

---

## Status
This project focuses on correctness, clear state modeling, and clean separation between agent behavior and game logic.
