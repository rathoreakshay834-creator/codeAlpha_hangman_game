import random


WORDS = {
    "animals": {
        "easy": ["cat", "dog", "lion", "tiger", "elephant"],
        "medium": ["giraffe", "penguin", "dolphin", "rhino", "cheetah"],
        "hard": ["chameleon", "porcupine", "baboon", "narwhal", "lemur"],
    },
    "countries": {
        "easy": ["france", "india", "japan", "spain", "kenya"],
        "medium": ["canada", "brazil", "germany", "egypt", "argentina"],
        "hard": ["madagascar", "iceland", "mongolia", "venezuela", "uzbekistan"],
    },
    "programming": {
        "easy": ["python", "java", "html", "code", "loop"],
        "medium": ["function", "database", "compiler", "variable", "debugger"],
        "hard": ["recursion", "algorithm", "framework", "iteration", "inheritance"],
    },
    "fruits": {
        "easy": ["apple", "grape", "mango", "pear", "kiwi"],
        "medium": ["pineapple", "strawberry", "blueberry", "orange", "banana"],
        "hard": ["watermelon", "pomegranate", "coconut", "apricot", "dragonfruit"],
    },
}


def load_leaderboard(file_path="hangman_leaderboard.txt"):
    """Return leaderboard entries sorted by highest score first."""
    entries = []
    try:
        with open(file_path, "r", encoding="utf-8") as leaderboard_file:
            for line in leaderboard_file:
                line = line.strip()
                if not line:
                    continue
                parts = [part.strip() for part in line.split("|")]
                if len(parts) < 4:
                    continue
                name, score_text, category, difficulty = parts[:4]
                try:
                    score = int(score_text)
                except ValueError:
                    continue
                entries.append(
                    {
                        "name": name,
                        "score": score,
                        "category": category,
                        "difficulty": difficulty,
                    }
                )
    except FileNotFoundError:
        return []

    return sorted(entries, key=lambda item: item["score"], reverse=True)


def update_leaderboard(name, score, category, difficulty, file_path="hangman_leaderboard.txt"):
    """Append a score entry and save the leaderboard back to disk."""
    leaderboard = load_leaderboard(file_path=file_path)
    leaderboard.append(
        {
            "name": str(name),
            "score": int(score),
            "category": str(category),
            "difficulty": str(difficulty),
        }
    )
    leaderboard = sorted(leaderboard, key=lambda item: item["score"], reverse=True)

    with open(file_path, "w", encoding="utf-8") as leaderboard_file:
        for entry in leaderboard:
            leaderboard_file.write(
                f"{entry['name']}|{entry['score']}|{entry['category']}|{entry['difficulty']}\n"
            )

    return leaderboard


def show_leaderboard(file_path="hangman_leaderboard.txt", limit=10):
    """Print the highest-scoring entries in the leaderboard."""
    leaderboard = load_leaderboard(file_path=file_path)
    print("\n=== Leaderboard ===")
    if not leaderboard:
        print("No scores yet. Play a round to add the first score!")
        return

    for rank, entry in enumerate(leaderboard[:limit], start=1):
        print(
            f"{rank}. {entry['name']} - {entry['score']} points "
            f"({entry['category']}, {entry['difficulty']})"
        )


def evaluate_guess(secret_number, guessed_number):
    """Return a text-based result for comparing a guessed number against a target."""
    if guessed_number < secret_number:
        return "Too low"
    if guessed_number > secret_number:
        return "Too high"
    return "Correct"


def load_best_score(file_path="hangman_best_score.txt"):
    try:
        with open(file_path, "r", encoding="utf-8") as score_file:
            value = score_file.read().strip()
            return int(value) if value else 0
    except FileNotFoundError:
        return 0


def save_best_score(score, file_path="hangman_best_score.txt"):
    with open(file_path, "w", encoding="utf-8") as score_file:
        score_file.write(str(int(score)))
    return int(score)


def choose_word(category, difficulty):
    category_key = category.lower()
    difficulty_key = difficulty.lower()
    if category_key not in WORDS:
        raise ValueError(f"Unknown category: {category}")
    if difficulty_key not in WORDS[category_key]:
        raise ValueError(f"Unknown difficulty: {difficulty}")
    return random.choice(WORDS[category_key][difficulty_key])


def get_hint(word, guessed_letters):
    available = [letter for letter in word if letter not in guessed_letters]
    return random.choice(available) if available else "No hint available"


def display_hangman(mistakes):
    stages = [
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
    if mistakes >= len(stages):
        mistakes = len(stages) - 1
    print(stages[mistakes])


def format_word(word, guessed_letters):
    return " ".join(letter if letter in guessed_letters else "_" for letter in word)


def play_game(player_name="Player"):
    categories = list(WORDS.keys())
    print("Welcome to Hangman!")
    print("Available categories:", ", ".join(categories))

    while True:
        category_choice = input("Choose a category or type 'random': ").strip().lower()
        if category_choice == "random":
            category = random.choice(categories)
            print(f"Random category selected: {category.title()}")
            break
        if category_choice in WORDS:
            category = category_choice
            break
        print("Invalid category. Please try again.")

    difficulty_levels = ["easy", "medium", "hard"]
    while True:
        difficulty = input("Choose difficulty (easy/medium/hard): ").strip().lower()
        if difficulty in difficulty_levels:
            break
        print("Invalid difficulty. Please try again.")

    secret_word = choose_word(category, difficulty)
    guessed_letters = set()
    wrong_guesses = 0
    max_mistakes = 6
    best_score = load_best_score()
    score = 0

    print(f"\nYour word is: {format_word(secret_word, guessed_letters)}")

    while wrong_guesses < max_mistakes:
        display_hangman(wrong_guesses)
        print(f"Current word: {format_word(secret_word, guessed_letters)}")
        print(f"Incorrect guesses: {wrong_guesses}/{max_mistakes}")

        guess = input("Guess a letter or type 'hint': ").strip().lower()

        if guess == "hint":
            if secret_word:
                hint_letter = get_hint(secret_word, guessed_letters)
                print(f"Hint: the word contains '{hint_letter}'")
                guessed_letters.add(hint_letter)
            continue

        if not guess or not guess.isalpha():
            print("Please enter a valid letter.")
            continue

        if guess in guessed_letters:
            print("You already guessed that letter.")
            continue

        guessed_letters.add(guess)

        if guess in secret_word:
            print("Correct guess!")
            if set(secret_word) <= guessed_letters:
                score = (len(secret_word) * 10) + (max_mistakes - wrong_guesses) * 5
                print(f"You won! The word was '{secret_word}'.")
                print(f"Your score: {score}")
                if score > best_score:
                    best_score = score
                    save_best_score(best_score)
                update_leaderboard(player_name, score, category, difficulty)
                return score
        else:
            wrong_guesses += 1
            print("Wrong guess!")
            if wrong_guesses == max_mistakes:
                display_hangman(wrong_guesses)
                print(f"Game over! The word was '{secret_word}'.")
                update_leaderboard(player_name, 0, category, difficulty)
                return 0

    return 0


def main():
    player_name = input("Enter your name: ").strip() or "Player"
    while True:
        print("\n=== Hangman Menu ===")
        print("1. Play game")
        print("2. View leaderboard")
        print("3. Quit")
        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            play_game(player_name)
            show_leaderboard()
        elif choice == "2":
            show_leaderboard()
        elif choice == "3":
            print("Thanks for playing!")
            break
        else:
            print("Invalid option. Please choose 1, 2, or 3.")


if __name__ == "__main__":
    main()
