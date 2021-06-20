text = input("Text: ")

letters = 0
words = 1
sentences = 0

for letter in text:
    if letter.isalpha():
        letters += 1
    if letter == ' ':
        words += 1
    if letter == '.' or letter == '?' or letter == '!':
        sentences += 1

# Average number of letters / sentences per 100 words
letters = letters / words * 100
sentences = sentences / words * 100

index = round(0.0588 * letters - 0.296 * sentences - 15.8)

if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print(f"Grade {index}")
