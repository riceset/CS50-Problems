#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

char ALPHABET[] = {'0', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'};

int POINTS[] = {0, 1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);

int main(void)
{
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    //Remove the comments to print the actual score on the program:
    // printf("Player 1: %i\n", score1);
    //printf("Player 2: %i\n", score2);

    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }

    else if (score2 > score1)
    {
        printf("Player 2 wins!\n");
    }

    else
    {
        printf("Tie!\n");
    }
}

int compute_score(string word)
{
    int total = 0;

    //Loops for each character inside the string given:
    for (int i = 0, n = strlen(word); i < n; i++)
    {
        char uppercased = toupper(word[i]);
        
        //if it's not a letter in the alphabet, 0 is given as the value:
        if (uppercased > 90 && uppercased < 65)
        {
            uppercased = '0';
        }

        //Tells the index of the current letter based on the ALPHABET array.
        const char *ptr = strchr(ALPHABET, uppercased);

        int index = 0;
        if (ptr)
        {
            index = ptr - ALPHABET;
        }
        
        //Assigns the letter itself to the point it is valid. (eg. B is 3)
        int letterPoint = POINTS[index];
        
        //The total sum of the points each letter inside the string is valid:
        total = total + letterPoint;
    }
    return total;
}
