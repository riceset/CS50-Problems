#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(void)
{
    string sentence = get_string("Text: ");

    float letters = 0;
    float words = 1;
    float sentences = 0;

    for (int i = 0, n = strlen(sentence); i < n; i++)
    {
        //Uppercases the input:
        char uppercased = toupper(sentence[i]);

        //Increase the letters counter for each letter in the sentence:
        if (uppercased >= 65 && uppercased <= 90)
        {
            letters++;
        }

        //32 is a space in ascii
        if (uppercased == 32)
        {
            words++;
        }

        if (uppercased == 46 || uppercased == 63 || uppercased == 33)
        {
            sentences++;
        }
    }

    //Average of letters per 100 words:
    float averLetters = letters / words * 100;

    //Average of sentences per 100 words:
    float averSentences = sentences / words * 100;

    //Coleman-Liau Index Calculation:
    float index = 0.0588 * averLetters - 0.296 * averSentences - 15.8;
    int grade = round(index);

    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }
}
