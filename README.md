# CodeAlpha Hangman Game

A fun text-based Hangman game built using Python. This version includes a game menu, multiple categories, difficulty levels, hints, score tracking, and a persistent leaderboard.

## Features

- Multiple word categories
  - Animals
  - Countries
  - Programming
  - Fruits
- Difficulty levels: easy, medium, hard
- Random word selection
- Random category option
- Hint system
- Score tracking
- Best score saving
- Persistent leaderboard
- Hangman drawing progress
- Main menu with Play, View Leaderboard, and Quit options
- Console-based gameplay

## Technologies Used

- Python
- Random module
- Lists and dictionaries
- Loops and conditionals
- String operations
- File handling

## How to Run

1. Install Python 3 on your system.
2. Open the project folder in VS Code.
3. Open a terminal in that folder.
4. Run the following command:

```bash
python hangman.py
```

## Gameplay

- Enter your name when the game starts
- Choose `1` to play, `2` to view the leaderboard, or `3` to quit
- Choose a category or use the random category option
- Select a difficulty level
- Guess letters one at a time
- Type `hint` if you need a clue
- The leaderboard is shown after each round
- Try to complete the word before the hangman is fully drawn

## Notes

This project is a beginner-friendly Python game and already includes a leaderboard, a random category option, and a simple game menu. It can still be extended with more features like:

- sound effects
- GUI version using Tkinter
- more word categories
- difficulty presets by theme