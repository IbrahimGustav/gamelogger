import json
from abc import ABC, abstractmethod

class GameEntry(ABC):
    platform_type = ""

    def __init__(self, title, platform, date_finished):
        self.title = title
        self.platform = platform
        self.date_finished = date_finished

    def get_summary(self):
        return f"[{self.platform_type}] {self.title} on {self.platform} - Finished on {self.date_finished}"

class PCGame(GameEntry):
    platform_type = "PC"

class ConsoleGame(GameEntry):
    platform_type = "Console"

class GameLogger:
    def __init__(self, filename='games.json'):
        self.filename = filename
        self.entries = self.load_data()

    def add_entry(self, game):
        self.entries.append(game)
        self.save_data()

    def edit_entry(self, index, new_game):
        if 0 <= index < len(self.entries):
            self.entries[index] = new_game
            self.save_data()
            print("Game updated successfully.")
        else:
            print("Invalid index.")

    def remove_entry(self, index):
        if 0 <= index < len(self.entries):
            removed = self.entries.pop(index)
            self.save_data()
            print(f"Removed: {removed.get_summary()}")
        else:
            print("Invalid index.")

    def display_entries(self):
        for i, game in enumerate(self.entries, 1):
            print(f"{i}. {game.get_summary()}")

    def save_data(self):
        with open(self.filename, 'w') as f:
            json.dump([game.__dict__ | {'type': game.__class__.__name__} for game in self.entries], f, indent=4)

    def load_data(self):
        class_map = {"PCGame": PCGame, "ConsoleGame": ConsoleGame}
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                return [class_map[item['type']](item['title'], item['platform'], item['date_finished']) for item in data]
        except FileNotFoundError:
            return []

def main():
    logger = GameLogger()

    while True:
        print("\nGame Logger Menu")
        print("1. Add PC Game")
        print("2. Add Console Game")
        print("3. View All Games")
        print("4. Edit Game")
        print("5. Remove Game")
        print("6. Exit")

        choice = input("Select an option: ")

        if choice in ('1', '2'):
            title = input("Game Title: ")
            platform = input("Platform (e.g., Steam, PS5): ")
            date = input("Date Finished (YYYY-MM-DD): ")
            game_class = PCGame if choice == '1' else ConsoleGame
            logger.add_entry(game_class(title, platform, date))

        elif choice == '3':
            logger.display_entries()

        elif choice == '4':
            logger.display_entries()
            index = int(input("Enter the number of the game to edit: ")) - 1
            if 0 <= index < len(logger.entries):
                old_game = logger.entries[index]
                title = input(f"Game Title [{old_game.title}]: ") or old_game.title
                platform = input(f"Platform [{old_game.platform}]: ") or old_game.platform
                date = input(f"Date Finished [{old_game.date_finished}]: ") or old_game.date_finished
                new_game = type(old_game)(title, platform, date)
                logger.edit_entry(index, new_game)
            else:
                print("Invalid selection.")

        elif choice == '5':
            logger.display_entries()
            index = int(input("Enter the number of the game to remove: ")) - 1
            logger.remove_entry(index)

        elif choice == '6':
            print("Goodbye!")
            break

        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()