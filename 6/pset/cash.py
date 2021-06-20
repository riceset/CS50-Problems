# Coins
quarter = 25
dime = 10
nickel = 5
penny = 1

# Initial value owed
while True:
    try:
        initial = float(input("Change owed: ")) * 100
        if initial > 0:
            break
    except ValueError:
        continue

# change owed
owed = round(int(initial))

# Total coins used
total = 0

while not owed == 0:
    if owed >= quarter:
        owed = owed - quarter
        total = total + 1

    elif owed >= dime:
        owed = owed - dime
        total = total + 1

    elif owed >= nickel:
        owed = owed - nickel
        total = total + 1

    elif owed >= penny:
        owed = owed - penny
        total = total + 1

print(total)
