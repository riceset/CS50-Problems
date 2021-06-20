#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <stdlib.h>


int main(int argc, string argv[])
{
    char keyChar;
    
    //Error types:
    bool invalidKey = false;
    bool numbers = false;
    bool tooShort = false;
    bool duplicates = false;

    //Checks if the user entered 1 key:
    if (argc == 1 || argc > 2)
    {
        invalidKey = true;
    }

    //If the user entered a key:
    else if (argv[1] != NULL)
    {
        for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            //Uppercases each character inside the key:
            keyChar = toupper(argv[1][i]);

            //Checks if the key contains 26 characters:
            if (strlen(argv[1]) != 26)
            {
                tooShort = true;
            }

            //Triggers an error if there's a non-alphabetical character inside the key:
            else if (!isalpha(keyChar))
            {
                numbers = true;
            }
        }
        
        //Checks for duplicate characters:
        int count;
        for (int j = 0; j < strlen(argv[1]); j++)
        {  
            count = 1;
            for (int k = j + 1; k < strlen(argv[1]); k++)
            {  
                if (argv[1][j] == argv[1][k] && argv[1][j] != ' ')
                {  
                    count++;  
                    argv[1][k] = '0';
                }
            }
        
            if (count > 1 && argv[1][j] != '0')
            {
                duplicates = true;
            }
        }
    }
    
    if (numbers)
    {
        printf("Key must only contain alphabetic characters.\n");
        return 1;
    }

    else if (tooShort)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    else if (duplicates)
    {
        printf("Key must not contain repeated characters.\n");
        return 1;
    }
    
    else if (invalidKey)
    {
        printf("Usage: ./substitution KEY\n");
        return 1;
    }
    
    else
    {
        //Gets input:
        string plaintext = get_string("plaintext: ");
        
        //Prompt:
        printf("ciphertext: ");
        for (int i = 0, n = strlen(plaintext); i < n; i++)
        {
            char alphabet[] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'};
            
            //Backup of the text entered:
            char lowercase = plaintext[i];
            
            //Uppercased version of the text entered:
            char letter = toupper(plaintext[i]);
            
            //Gives the index of each item on the alphabet array:
            const char *ptr = strchr(alphabet, letter);
            int index = 0;
            if (ptr)
            {
                index = ptr - alphabet;
            }
            
            //Capitalizing the key:
            char cipher;
            for (int j = 0, m = strlen(argv[1]); j < m; j++)
            {
                cipher = toupper(argv[1][index]);
            }
            
            //If the char was originally lowercased, make it lowercased again:
            if (islower(lowercase))
            {
                cipher = tolower(cipher);
            }
            
            //If the char is not alphabetical, keep it as it is:
            else if (!isalpha(plaintext[i]))
            {
                cipher = plaintext[i];
            }
            
            printf("%c", cipher);
        }
        printf("\n");
    }
    
}