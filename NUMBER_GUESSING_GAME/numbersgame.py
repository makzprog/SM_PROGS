import random

class NumberGuessingGame:
    def __init__(self, lower = 1, upper = 100):
        self.lower = lower
        self.upper = upper
        
    def start_game(self):
        self.number_to_guess = tuple(random.randint(self.lower, self.upper) for _ in range(self.upper))
        self.attempts = 0
        self.isActive = True
        while self.isActive:
            user_guess = input(f"Guess the number between {self.lower} and {self.upper}: ")
            if user_guess in self.number_to_guess:
                self.attempts += 1
                print(f"Congratulations! You've guessed the number in {self.attempts} attempts.")
                self.isActive = False
            else:
                if user_guess <  