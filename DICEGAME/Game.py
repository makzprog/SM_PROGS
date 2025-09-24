import random

class DiceGame:
    def __init__(self, sides=6):
        self.sides = sides
    
    # Ask user for how many dices they want to roll
    def amount_dices(self):
        num_dices = input("How many dices do you want to roll? ")
        
        if num_dices.isdigit() and int(num_dices) > 0:
            num_dices = int(num_dices)
            return num_dices
        else:
            print("Please enter a valid number.")
            return self.amount_dices()
    
    # Roll the dices and display the result     
    def roll_dices(self, num_dices):
        count = 0
        sum_totals = 0
        isActive = True
        while isActive:
            ask_user = input("Roll the dices? (y/n): ")
            if ask_user == 'y' or ask_user == 'Y':
                self.roll = tuple(random.randint(1, self.sides) for _ in range(num_dices))
                count += 1
                sum_totals += sum(self.roll)
                print("You rolled:", self.roll, " | Total:", sum_totals, " | Times Rolled:", count)
                sum_totals = 0
            elif ask_user == 'n' or ask_user == 'N':
                isActive = False
                print("Game Over")
                print("Total rolls:", count)
                break
            else:
                if ask_user != 'y' and ask_user != 'Y':
                    print("Invalid input. Please enter 'y' or 'n'.")
        return self.roll

# start the program
if __name__ == "__main__":
    start_game = DiceGame()
    specify_dices = start_game.amount_dices()
    rolling_dices = start_game.roll_dices(specify_dices)
