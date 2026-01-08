import os
import random
from typing import Literal
from google import genai
from google.genai import types

#ADK
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "GOOGLE_API_KEY not found."
    )

client = genai.Client(api_key=API_KEY)

# Global Game State 
game_state = {
    "round": 0,
    "user_score": 0,
    "bot_score": 0,
    "user_bomb_used": False,
    "bot_bomb_used": False,
    "game_over": False
}

# Game Logic
def validate_move(move: str, player: Literal["user", "bot"]) -> dict:
    """Validate move and enforce bomb constraints."""
    move = move.lower().strip()
    valid_moves = ["rock", "paper", "scissors", "bomb"]

    if move not in valid_moves:
        return {"valid": False, "reason": "Invalid move"}

    if move == "bomb":
        if player == "user" and game_state["user_bomb_used"]:
            return {"valid": False, "reason": "User bomb already used"}
        if player == "bot" and game_state["bot_bomb_used"]:
            return {"valid": False, "reason": "Bot bomb already used"}

    return {"valid": True, "move": move}


def resolve_round(user_move: str, bot_move: str) -> dict:
    """Determine winner of a round."""
    if user_move == bot_move:
        return {"winner": "draw", "reason": "Same move"}

    if user_move == "bomb" and bot_move == "bomb":
        return {"winner": "draw", "reason": "Bomb vs Bomb"}

    if user_move == "bomb":
        return {"winner": "user", "reason": "Bomb beats everything"}

    if bot_move == "bomb":
        return {"winner": "bot", "reason": "Bomb beats everything"}

    wins = {
        "rock": "scissors",
        "scissors": "paper",
        "paper": "rock"
    }

    if wins[user_move] == bot_move:
        return {"winner": "user", "reason": f"{user_move} beats {bot_move}"}

    return {"winner": "bot", "reason": f"{bot_move} beats {user_move}"}


def update_game_state(result: dict, user_move: str, bot_move: str) -> dict:
    """Update persistent game state."""
    game_state["round"] += 1

    if user_move == "bomb":
        game_state["user_bomb_used"] = True
    if bot_move == "bomb":
        game_state["bot_bomb_used"] = True

    if result["winner"] == "user":
        game_state["user_score"] += 1
    elif result["winner"] == "bot":
        game_state["bot_score"] += 1

    if game_state["round"] >= 3:
        game_state["game_over"] = True

    return game_state

# Agent System Prompt
SYSTEM_PROMPT = """
You are an AI referee for Rock–Paper–Scissors–Plus.

Responsibilities:
- Explain rules briefly (≤ 5 lines)
- Prompt the user for a move
- Interpret user intent
- Call tools to validate moves and resolve rounds
- Clearly explain outcomes
- End the game automatically after 3 rounds

Rules:
- Moves: rock, paper, scissors, bomb (once per player)
- Bomb beats all
- Bomb vs bomb is a draw
- Invalid input wastes the round

Do NOT invent state.
Always rely on tool outputs.
"""

def generate_narration(round_no, user_move, bot_move, result):
    prompt = f"""
Round {round_no} just ended.

User move: {user_move}
Bot move: {bot_move}
Result: {result['winner']}
Reason: {result['reason']}

Explain this round briefly in simple, friendly language.
"""

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    return response.text.strip()


# Game Loop 
def play_game():
    print("Rock–Paper–Scissors")
    print("• Game is best of 3 rounds")
    print("• Moves: rock, paper, scissors, bomb: once per game")
    print("• Bomb beats all; bomb vs bomb is a draw\n")

    while not game_state["game_over"]:
        user_input = input(f"Round {game_state['round'] + 1} — Your move: ")
        user_validation = validate_move(user_input, "user")

        bot_move = random.choice(["rock", "paper", "scissors", "bomb"])
        bot_validation = validate_move(bot_move, "bot")
        if not bot_validation["valid"]:
            bot_move = random.choice(["rock", "paper", "scissors"])

        if not user_validation["valid"]:
            print("Invalid move. Round wasted.\n")
            update_game_state({"winner": "draw"}, None, None)
            continue

        result = resolve_round(user_validation["move"], bot_move)
        update_game_state(result, user_validation["move"], bot_move)

        narration = generate_narration(
            game_state["round"],
            user_validation["move"],
            bot_move,
            result
        )

        print(narration)
        print(f"Score → You {game_state['user_score']} : Bot {game_state['bot_score']}\n")



    print("GAME OVER ")
    if game_state["user_score"] > game_state["bot_score"]:
        print("Final Result: You win ")
    elif game_state["bot_score"] > game_state["user_score"]:
        print("Final Result: Bot wins ")
    else:
        print("Final Result: Draw ")

if __name__ == "__main__":
    play_game()
