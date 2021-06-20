# Gets a positive integer between 1 and 8 inclusive
while True:
    try:
        height = int(input("Height: "))
        if height >= 1 and height <= 8:
            break
    except ValueError:
        continue

hashes = 1
blank = height - hashes

for i in range(height):

    for j in range(blank):
        print(" ", end="")

    for j in range(hashes):
        print("#", end="")

    print("  ", end="")

    for j in range(hashes):
        print("#", end="")

    hashes = hashes + 1
    blank = blank - 1
    print()
