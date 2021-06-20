// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

//Total words
unsigned int total = 0;

// Number of buckets in hash table
const unsigned int N = 10000;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int index = hash(word);

    for (node *cursor = table[index]; cursor != NULL; cursor = cursor->next)
        if (strcasecmp(cursor->word, word) == 0) return true;

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int sum = 0;

    for (int i = 0, n = strlen(word); i < n; sum += tolower(word[i]), i++);

    return sum % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *dict = fopen(dictionary, "r");
    if (!dict) return false;

    char *word = malloc(LENGTH + 1);

    while (fscanf(dict, "%s", word) != EOF)
    {
        node *new = malloc(sizeof(node));
        if (!new) return false;

        //Copies the new word into the new node
        strcpy(new->word, word);
        new->next = NULL;

        //Hashes the word
        int index = hash(word);

        //table[index] is a pointer to the head of a linked list
        //at index index

        if (!table[index])
            table[index] = new;

        else
        {
            new->next = table[index];
            table[index] = new;
        }

        total++;
    }

    free(word);
    fclose(dict);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return total;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        //tmp points to the head of the linked list at index index initially
        node *tmp = table[i];
        node *cursor = tmp;

        while (cursor)
        {
            cursor = cursor->next;
            free(tmp);
            tmp = cursor;
        }
    }

    return true;
}
