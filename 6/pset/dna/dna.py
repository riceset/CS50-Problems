import csv
import sys
import os
import re


def main():
    """Checks for correct number of arguments"""

    if len(sys.argv) != 3:
        sys.exit("Incorrect number of arguments.\nUsage: python dna.py database.csv sequence.txt")

    """checks for correct file extensions"""

    if os.path.splitext(sys.argv[1])[1] != '.csv':
        sys.exit("File extension is wrong. Expected '.csv' as first argument.\nUsage: python dna.py database.csv sequence.txt")
    elif os.path.splitext(sys.argv[2])[1] != '.txt':
        sys.exit("File extension is wrong. Expected '.txt' as second argument.\nUsage: python dna.py database.csv sequence.txt")

    """checks if the file exists"""
    if not os.path.isfile(sys.argv[1]) and not os.path.isfile(sys.argv[2]):
        sys.exit("The file provided does not exist.\nUsage: python dna.py database.csv sequence.txt")

    """Opening the files"""
    with open(sys.argv[1]) as database_file:
        with open(sys.argv[2]) as sequence_file:

            sequence = sequence_file.read()

            # A list with all the sequence names
            sequence_names = ["AGTC", "AGATC", "AATG", "TCTAG", "GATA", "TATC", "GAAA", "TCTG", "TTTTTTCT"]

            # Counter is a dictionary with a sequence as a key and the number
            # of times it repeats in a sequence as a value
            counters = dict.fromkeys(sequence_names, 0)
 
            for key in counters:

                # Matches contains the longest sequence of the current pattern but may
                # contain duplicates
                matches = re.findall(fr"(?:{key})+", sequence)

                # Maximum doesn't contain duplicates, but if a list is empty
                # it will fill it with zero
                maximum = max(matches, key=len, default=0)
                
                # Filters and removes all the 0s
                if isinstance(maximum, str):

                    # Assigns how many time the current pattern repeated in a row as a value
                    # in the counters dict
                    counters[key] = maximum.count(key)

            database = csv.DictReader(database_file)

            # Creates a list with all the people on the CSV file
            people = []
            
            # Converts all the integer values to integers and appends each dict to the people list
            for person in database:
                temp = {}
                for key in person:
                    temp[key] = int(person[key]) if person[key].isdigit() else person[key]
                people.append(temp)

            # Creates a new field called compatible
            for person in people:
                person["Compatible"] = 0

            # Adds 1 to compatible if it matches the number
            for person in people:
                for key in person:
                    for key2 in counters:
                        if key2 == key:
                            if counters[key2] == person[key]:
                                person["Compatible"] += 1

            # If compatible is equal to the number of keys - 1 (name)
            # print the person's name
            for person in people:
                if person["Compatible"] == 8 or person["Compatible"] == 3:
                    print(person["name"])
                    sys.exit()
                    break

            print("No match")
            

if __name__ == "__main__":
    main()
