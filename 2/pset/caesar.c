#include <cs50.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include "../cs50.h"


int main(int argc, string argv[])
{
    bool valid;

    //Checks if the user entered 1 key:
    if (argc == 1 || argc > 2)
    {
        valid = false;
    }

    else
    {
        //Iteracts over the key:
        for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            //If it's not a digit, it's not valid:
            if (isdigit(argv[1][i]) == false)
            {
                valid = false;
                break;
            }

            //If it's a digit, it's valid:
            else if (isdigit(argv[1][i]))
            {
                valid = true;
            }
        }
    }

    if (valid == false)
    {
        printf("Usage: ./caesar arguments\n");
        return 1;
    }

    if (valid)
    {
        //converts the key into an int:
        int key = atoi(argv[1]);

        //Gets input:
        string plaintext = get_string("plaintext: ");

        //Cypher text:
        char cipher;
        
        //Prompt:
        printf("ciphertext: ");

        //Iteracts over the input:
        for (int i = 0, n = strlen(plaintext); i < n; i++)
        {
            //Handles cases that the chipertext goes over Z:
            if (plaintext[i] + key >= 'Z' || plaintext[i] + key >= 'z')
            {
                char alphabet[] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'};
                
                //Creates a backup of the plaintext word preserving the original case:
                char lowercase = plaintext[i];
                
                //Creates a copy of the plaintext word uppercasing everything:
                char letter = toupper(plaintext[i]);
                
                //Gives us the index of char letter on the alphabet array:
                const char *ptr = strchr(alphabet, letter);
                int index = 0;
                if (ptr)
                {
                    index = ptr - alphabet;
                }

                //ci is the new index if the letter surpasses Z/z (eg. z + 2 = b) because
                //the new index (ci) is now 1.
                int ci = (index + key) % 26;
                
                //Assigns the letter to the uppercased alphabet correspondent:
                letter = alphabet[ci];
                
                //If the letter was originally lowercased, it's converted back again:
                if (islower(lowercase))
                {
                    letter = tolower(letter);
                }
                
                cipher = letter;
            }

            //If the letter isn't alphabetical, keep it as it is.
            else if (!isalpha(plaintext[i]))
            {
                cipher = plaintext[i];
            }

            else
            {
                //Shifts the letters by the key provided:
                cipher = plaintext[i] + key;
            }
            
            printf("%c", cipher);
        }
        printf("\n");
    }
}
