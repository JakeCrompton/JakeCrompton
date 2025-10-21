
print("Welcome to the casino! ")
age = int(input("How old are you\n"))
if age < 18:
    print("You are not old enough to gamble")
    welcome = False
else:
    print("You are old enough to gamble")
    welcome = True

while welcome == True:
    print("Lag")
    break