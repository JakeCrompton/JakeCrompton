import os
import platform
import time

# Function to clear the console output
def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")
# View Inventory function
def viewInventory():
    seehands = input("Do you want to see inventory? ")
    if seehands.lower() == "yes":
        if len(hands) == 0:
            print("You have nothing in your hands")
        else:
            print("Hands:", hands)
    seebackpack = input("Do you want to see what's in your backpack? ")
    if seebackpack.lower() == "yes":
        if len(backpack) == 0:
            print("You have nothing in your backpack")
        else:
            print("Backpack:", backpack)

def swapItems():
    ask = input("Do you want to swap items you are holding? ")
    if ask.lower() == "yes":
        print("What items would you like to swap?")
        print("You currently have:", hands)

def shop():
    print("What do you want from the store?")

# Weapons: Quantity, Weight, Damage
Weapons = {
    "Sword": [1 ,2, 4],
    "Gun": [1, 1, 2],
}

# Armour: Quantity, Weight, Protection
Armour = {
    "Shirt": [1 ,2, 5],
    "Pants": [1, 2, 2],
}

# Stats: Value
Stats = {
    "Strength": 1,
    "Endurance": 1,
}

maxhands = 2
hands = []
backpack = []
maxHealth = 100
ArmourEquipped = 0
health = 100
game = False

startLoop = True
while startLoop:
    clear_screen()  # 👈 Clears screen before showing menu
    print("------------------")
    print("-----Main Menu-----")
    print("------------------")
    print("1: Start")
    print("2: How to play")
    print("3: Credits\n")
    StartPrompt = input("Type in the number of the option you would like to pick: ")

    if not StartPrompt.isdigit():
        print("Please type a valid number.")
        time.sleep(2)
        continue

    StartPrompt = int(StartPrompt)

    if StartPrompt > 3:
        print("You did not pick a valid option")
        time.sleep(2)

    elif StartPrompt == 1:
        game = True
        # Start game
        print("Game starting...")
        time.sleep(2)
        clear_screen()
    elif StartPrompt == 2:
        # How to play
        clear_screen()
        print("You read the prompts and whatever is in brackets is the choices you can make\n")
        input("Press Enter to return to menu...")
    elif StartPrompt == 3:
        # Credits
        clear_screen()
        print("Credits:\n why tf you looking in here")
        input("Press Enter to return to menu...")

    while game:
        print("You wake up in a room...")
        s1e1 = input("What do you want to do? [Look around] [Stand up] [Go back to sleep] ")

        if s1e1.lower() == "look around":
            clear_screen()
            print("You stand up and look around")
            input("Press Enter to continue...")
        elif s1e1.lower() == "stand up":
            clear_screen()
            print("You stand up.")
            input("Press Enter to continue...")
        elif s1e1.lower() == "go back to sleep":
            clear_screen()
            print("You fall back asleep... Game Over!")
            input("Press Enter to return to menu...")
            game = False
