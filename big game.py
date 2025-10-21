# this is a test
import random
import time 
import os
import sys

def add_experience(amount):
    main_stats["Experience"] += amount
    while main_stats["Experience"] >= xp_to_next_level(main_stats["Level"]):
        main_stats["Experience"] -= xp_to_next_level(main_stats["Level"])
        main_stats["Level"] += 1
        main_stats["Stat_Points"] += 1
        print(f"Level up! You are now level {main_stats['Level']}!")
        print(f"You have {main_stats['Stat_Points']} unspent stat points")

def xp_to_next_level(level):
    # can change the amount of xp needed by changing the formula (player needs 100 xp if level 1 and 300 if level 3)
    return 100 * (level + 1)

def fight_enemy():
    canRun = True
    print(f"A {enemy['Name']} wants to fight you")
    enemy_defeated = False

    while enemy_defeated == False:
        if canRun == True:
            print("You can either Fight or Run. [fight, run]")
        else:
            print("You can no longer run, you must fight. [fight]")
        fight_option1 = input("> ").lower()

        if fight_option1 == "fight":
            print(f"\n Which skill do you want to use on the {enemy['Name']}?")

            for stat, value in player_skills.items():
                print(f"{stat}: dealing {value} damage")
            fight_option2 = input("> ").strip().lower()
            foundMove = False

            for stat in player_skills.keys():
                if stat.strip().lower() == fight_option2:
                    foundMove = True
                    break

            if foundMove:
                damageDealt = player_skills['Punch'] * player_controlled_stats["Strength"]
                print(damageDealt)
                enemy['Health'] -= damageDealt
                if enemy['Health'] <= 0:
                    enemy_defeated = True
                print(f"\nYou have dealt {damageDealt} damage to the {enemy['Name']} [{enemy['Health']}hp remaining]")

            else:
                print("You did not enter a valid skill")
        else:
            if canRun == True:
                if main_stats["Race"] == "Human":
                    print("W BUFF")
                else:
                    print("NOT HUMAN")
                chance_to_run = random.randint(1,2)
                if chance_to_run == 1:
                    print(f"You ran away from the {enemy['Name']}")
                    break
                else:
                    print("You failed to run away")


    if enemy_defeated:
        print(f"You defeated the {enemy['Name']} and gained {enemy['XP_reward']} XP!")
        add_experience(enemy["XP_reward"])
        add_items_to_inv(enemy['Drops'])


        if main_stats["Stat_Points"] > 0:
            spend_stat_points()

def spend_stat_points():
    while main_stats["Stat_Points"] > 0:
        print("\n Your stats:")
        for stat, value in player_controlled_stats.items():
            print(f"    {stat}: {value}")
        print(f"You have {main_stats['Stat_Points']} points to spend.")
        print("Choose a stat to upgrade: Health / Strength / Intellegence.")
        choice = input("> ").strip().lower()

        foundStat = None
        for stat in player_controlled_stats.keys():
            if stat.lower() == choice:
                foundStat = stat
                break
        
        if foundStat:
            player_controlled_stats[foundStat] += 1
            main_stats["Stat_Points"] -= 1
            print(f"{foundStat} has increased by 1!")
        else:
            print(f"Invalid stat name.")
    print("\nALL stat points spent!\n")    

def shop():
    clearOutput()
    print("🛍️  Welcome to the Shop!\n")

    shop_stock = generate_shop_stock()
    
    while True:
        print("Categories: Weapons / Armour / Potions / Misc / Exit")
        category = input("> ").strip().capitalize()
        clearOutput()

        if category.lower() == "exit":
            print("Leaving the shop...")
            break

        if category not in shop_stock:
            print("Invalid category.")
            continue

        print(f"=== {category} ===")
        for i, item in enumerate(shop_stock[category], start=1):
            print(f"{i}. {item['Name']}  |  Price: {item['Price']}  |  Level Req: {item['LevelReq']}")
        
        print("\nSelect item number to buy or type 'back' to return.")
        choice = input("> ").strip().lower()

        if choice == "back":
            clearOutput()
            continue

        if not choice.isdigit():
            print("Invalid choice.")
            continue

        choice = int(choice)
        if choice < 1 or choice > len(shop_stock[category]):
            print("That item doesn’t exist.")
            continue

        item = shop_stock[category][choice - 1]

        # Check requirements
        if main_stats["Level"] < item["LevelReq"]:
            print(f"You need to be level {item['LevelReq']} to buy this item.")
            press_to_continue()
            clearOutput()
            continue

        if main_stats["Money"] < item["Price"]:
            print("You don't have enough money!")
            press_to_continue()
            clearOutput()
            continue

        # Purchase
        main_stats["Money"] -= item["Price"]
        player_items[item["Name"]] = player_items.get(item["Name"], 0) + 1
        print(f"You bought {item['Name']} for {item['Price']} gold!")
        press_to_continue()
        clearOutput()

def add_items_to_inv(drops):
    for item, (min_amount, max_amount) in drops.items():
        amount = random.randint(min_amount, max_amount)
        if amount > 0:
            player_items[item] = player_items.get(item, 0) + amount
            print(f"    {item} - {amount}x item added to inventory")

def select_race():
    print("\nAs you are being reborn, fate decides what you will become...")
    time.sleep(1)

    choice = random.choice(list(races.keys()))
    race_data = races[choice]

    main_stats["Race"] = choice.capitalize()
    
    player_controlled_stats["Health"] += race_data['HealthBonus']
    player_controlled_stats['Intelligence'] += race_data['IntelligenceBonus']
    player_controlled_stats['Strength'] += race_data['StrengthBonus']
    player_controlled_stats['Speed'] += race_data['SpeedBonus']

    print(f"You have been reborn as {main_stats['Race']}\n")
    time.sleep(1.5)

def clearOutput():
    os.system('cls')

def options():
    print("This is a text based game, to play it you must type in the output.")

def orcOrigin():
    print("You were born as an orc")

def humanOrigin():
    print("You were reborn as a human")

def goblinOrigin():
    print("You were reborn as a goblin")

def press_to_continue():
    print("\nPress SPACE to continue")

    if os.name == 'nt':
        import msvcrt
        while True:
            key = msvcrt.getch()
            if key == b' ': # space bar
                break        

def generate_shop_stock():
    shop_stock = {}

    for category, items in item_DB.items():
        weighted_items = []
        for item in items:
            weighted_items.extend([item] * item['Rarity'])

        stock = random.sample(weighted_items, min(5, len(weighted_items)))
        shop_stock[category] = stock

    return shop_stock


races = {
    "Human": {
        "HealthBonus": 0, # can give better escape odds
        "StrengthBonus": 0,
        "IntelligenceBonus": 4,
        "SpeedBonus": 2
    },
    "Goblin": {
        "HealthBonus": 2,
        "StrengthBonus": 3,
        "IntelligenceBonus": -2,
        "SpeedBonus": 1
    },
    "Orc": {
        "HealthBonus": 4,
        "StrengthBonus": 3,
        "IntelligenceBonus": -4,
        "SpeedBonus": 0
    }
}

main_stats = {
    "Level": 1,
    "Experience": 0,
    "Health": 100,
    "Stat_Points": 0,
    "Money": 0,
    "Race": ""
}

player_items = {
}

player_skills = {
    "Punch": 50,
}

player_controlled_stats = {
    "Health": 1,
    "Strength": 1,
    "Intelligence": 1,
    "Speed": 1,
}

enemies = [
    {
        "Name": "Goblin",
        "Health": 30,
        "XP_reward": random.randint(100, 200),
        "Drops": {
            "Stick": (0, 2),
            "Lighter": (0, 1)
        }
    },
    {
        "Name": "Zombie",
        "Health": 30,
        "XP_reward": random.randint(100, 200),
        "Drops": {
            "Stick": (1, 3),
            "Lighter": (0, 1)
        }
    }
]

item_DB = {  # add more items in here (5 in each atleast) (the lower the rarity, the rarer it is)
    "Weapons": [
        {"Name": "Wooden Sword", "Price": 50, "LevelReq": 1, "Rarity": 10},
    ],
    "Armour": [
        {"Name": "Cloth", "Price": 50, "LevelReq": 1, "Rarity": 10}
    ],
    "Potions": [
        {"Name": "Small Health Potion", "Price": 50, "LevelReq": 1, "Rarity": 10}
    ],
    "Misc": [
        {"Name": "Torch", "Price": 50, "LevelReq": 1, "Rarity": 10}
    ]
}
enemy = random.choice(enemies)

print("#############")
print("# Main Menu #")
print("#############")
print("1. Start.")
print("2. Options.")
mainmenuinput = input("> ").strip().lower()

if mainmenuinput == "start":
    print("Starting...")
    # This is character creation
    time.sleep(1)
    clearOutput()
    select_race()
    press_to_continue()

elif mainmenuinput == "Options":
    print("Options...")
    options()

else:
    print("You did not select a valid option.")

# Main game
clearOutput()

fight_enemy()

# Work on either the combat (it still needs who ever has the fastest speed will go first and bag usage)
# maybe add quests to get more xp
# make actual progression as well