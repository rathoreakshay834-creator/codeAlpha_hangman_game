import os
import random

WORDS = {
    "animals": [
        ("cat", "A pet that likes to sleep"),
        ("tiger", "A big striped wild cat"),
        ("elephant", "The largest land animal"),
        ("giraffe", "A tall animal with a long neck"),
        ("dolphin", "A smart sea mammal"),
        ("rabbit", "A small animal that hops"),
        ("parrot", "A colorful bird that can mimic sounds"),
    ],
    "countries": [
        ("india", "A country in South Asia"),
        ("france", "Known for the Eiffel Tower"),
        ("japan", "An island country in Asia"),
        ("brazil", "A country in South America"),
        ("canada", "Known for maple leaves and snow"),
        ("germany", "Home to many famous cars"),
        ("egypt", "A country with the pyramids"),
    ],
    "programming": [
        ("python", "A beginner-friendly programming language"),
        ("java", "A popular object-oriented language"),
        ("html", "Used to build webpage structure"),
        ("css", "Used for styling web pages"),
        ("github", "A platform for storing code"),
        ("developer", "A person who builds software"),
        ("computer", "An electronic machine for processing data"),
    ],
    "fruits": [
        ("apple", "A red or green fruit"),
        ("banana", "A yellow curved fruit"),
        ("mango", "A sweet tropical fruit"),
        ("grape", "Small fruits usually found in bunches"),
        ("orange", "A citrus fruit with a peel"),
        ("papaya", "A tropical fruit with black seeds"),
        ("peach", "A fuzzy fruit with a pit"),
    ],
}

HANGMAN_STAGES = [
    """
      +---+
      |   |
          |
          |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
          |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
      |   |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|\\  |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|\\  |
     /    |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|\\  |
     / \\ |
          |
    =========
    """,
]


def choose_word(category, difficulty):
    category = category.lower()
    if category not in WORDS:
        category = random.choice(list(WORDS.keys()))

    options = []
    for word, hint in WORDS[category]:
        if difficulty == "easy" and len(word) <= 5:
            options.append((word, hint))
        elif difficulty == "medium" and 5 < len(word) <= 8:
            options.append((word, hint))
        elif difficulty == "hard" and len(word) > 8:
            options.append((word, hint))

    if not options:
        options = WORDS[category]

    return random.choice(options)


def load_best_score():
    file_path = os.path.join(os.path.dirname(__file__), "hangman_best_score.txt")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            value = file.read().strip()
            return int(value) if value else 0
    except (FileNotFoundError, ValueError):
        return 0


def save_best_score(score):
    file_path = os.path.join(os.path.dirname(__file__), "hangman_best_score.txt")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(str(score))


def display_word(word, guessed_letters):
    displayed = ""
    for letter in word:
        if letter in guessed_letters:
            displayed += letter + " "
        else:
            displayed += "_ "
    return displayed.strip()


def play_game(best_score):
    print("\n================================")
    print("       HANGMAN GAME")
    print("================================")
    print("Choose a category and difficulty level.")

    print("\nAvailable categories:")
    for category_name in WORDS:
        print(f"- {category_name}")

    category = input("Enter category: ").strip().lower()
    while category not in WORDS:
        print("Invalid category. Please choose one of the available options.")
        category = input("Enter category: ").strip().lower()

    difficulty = input("Choose difficulty (easy/medium/hard): ").strip().lower()
    while difficulty not in {"easy", "medium", "hard"}:
        print("Invalid difficulty. Choose easy, medium, or hard.")
        difficulty = input("Choose difficulty (easy/medium/hard): ").strip().lower()

    word, hint = choose_word(category, difficulty)
    guessed_letters = []
    wrong_guesses = 0
    max_wrong_guesses = 6
    score = 0
    hint_used = False

    print(f"\nCategory: {category.title()}")
    print(f"Difficulty: {difficulty.title()}")
    print("Type 'hint' anytime to reveal a clue.")

    while wrong_guesses < max_wrong_guesses:
        print("\n" + HANGMAN_STAGES[wrong_guesses])
        print("Word:", display_word(word, guessed_letters))
        print("Used letters:", ", ".join(sorted(guessed_letters)) if guessed_letters else "None")
        print("Score:", score)

        if all(letter in guessed_letters for letter in word):
            score += 50
            if score > best_score:
                best_score = score
                save_best_score(best_score)
            print("\n🎉 Congratulations! You guessed the word!")
            print("Word:", word)
            print("Your final score:", score)
            print("Best score:", best_score)
            return best_score

        guess = input("Enter a letter or type 'hint': ").strip().lower()

        if guess == "hint":
            if not hint_used:
                print(f"Hint: {hint}")
                score = max(0, score - 10)
                hint_used = True
            else:
                print("You already used the hint.")
            continue

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter only one valid letter.")
            continue

        if guess in guessed_letters:
            print("You already guessed that letter.")
            continue

        guessed_letters.append(guess)

        if guess in word:
            score += 10
            print("✅ Correct guess!")
        else:
            score = max(0, score - 5)
            wrong_guesses += 1
            print("❌ Wrong guess!")
            print(f"Wrong guesses: {wrong_guesses}/{max_wrong_guesses}")

    print("\n" + HANGMAN_STAGES[max_wrong_guesses])
    print("\n😢 Game Over!")
    print("The correct word was:", word)
    print("Final score:", score)
    print("Best score:", best_score)
    return best_score


def main():
    best_score = load_best_score()
    print("================================")
    print("      WELCOME TO HANGMAN")
    print("================================")
    print(f"Best Score: {best_score}")

    while True:
        best_score = play_game(best_score)
        choice = input("\nDo you want to play again? (y/n): ").strip().lower()
        if choice not in {"y", "yes"}:
            print("Thanks for playing! Goodbye!")
            break


if __name__ == "__main__":
    main()