import random
import time

def randomNumber():
    pickedNumber = random.randint(1, base)
    return pickedNumber

started = False

while True:
    start = input("Do you want start? ")
    if start == "yes":
        started = True
        base = 2
        stage = 0

    while started == True:
        stage += 1
        number = randomNumber() 
        if number == base:
            print("You got to stage", stage)
            started = False
        if stage > 100:
            print("You maxed out on stage", stage)
            started = False
        base += 1
