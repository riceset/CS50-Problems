import sys


def main():
    num = int(input("Number: "))
    if checksum(num) == False:
        print("INVALID")
        sys.exit(1)

    else:
        if len(str(num)) == 15 and (int(str(num)[:2]) == 34 or int(str(num)[:2]) == 37):
            print("AMEX")
        elif len(str(num)) == 16 and (int(str(num)[:2]) == 51 or int(str(num)[:2]) == 52 or int(str(num)[:2]) == 53 or int(str(num)[:2]) == 54 or int(str(num)[:2]) == 55):
            print("MASTERCARD")
        elif len(str(num)) == 13 or len(str(num)) == 16 and int(str(num)[:1]) == 4:
            print("VISA")
        else:
            print("INVALID")


def split(word):
    return [char for char in word]


def checksum(num):
    # Turns the credit card number into a list of digits
    num = list = [int(x) for x in str(num)]

    tmp = []

    secondHalf = 0

    # Iterates over all the numbers
    for number in range(len(list)):
        # Checks for every other number
        if not (number + 1) % 2 == 0:
            # Adds the current number multiplied by to to tmp and splits it if the number has more
            # than 1 digit
            tmp.append(split(str(list[number] * 2)))
        else:
            secondHalf += list[number]

    # Converts the 2D list into a flat list
    tmp = sum(tmp, [])

    # Converts the list of strings into a list of integers
    tmp = [int(i) for i in tmp]

    # Gets the sum of the list
    listSum = sum(tmp)
    checksum = secondHalf + listSum

    # If the last digit of the checksum is 0, then the cc num is valid
    if checksum % 10 == 0:
        return True
    else:
        return False
    return False

main()
