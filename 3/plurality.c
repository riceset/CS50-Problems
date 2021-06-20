#include <cs50.h>
#include <stdio.h>
#include <string.h>

//const int MAX = 9;
#define MAX 9

typedef struct
{
    string name;
    int votes;
} candidate;

//Array of candidates:
candidate candidates[MAX];

//Number of candidates:
int candidate_count;

//Prototypes:
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    //Checks if the user entered less candidates than the required:
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    candidate_count = argc - 1; // Because the program name counts inside argc

    //Checks if the user entered more than 9 candidates:
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }

    //Assigns the entered name for each candidate inside the data structure:
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        if (!vote(name))
            printf("Invalid vote.\n");
    }
    print_winner();
}

bool vote(string name)
{
    //For each candidate entered, compare it to a candidate in the data structure,
    //if it's there add one to his/her votes.
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(name, candidates[i].name) == 0)
        {
            candidates[i].votes++;
            return true;
        }
    }
    return false;
}

void print_winner(void)
{
    int biggestVote = 0;

    //Linear searches through all the votes to get the biggest number:
    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].votes > biggestVote)
        {
            biggestVote = candidates[i].votes;
        }
    }

    //Searches again, but this time looking for any candidate with the
    //number of votes iqual to the highest vote.
    for (int j = 0; j < candidate_count; j++)
    {
        if (candidates[j].votes == biggestVote)
        {
            printf("%s\n", candidates[j].name);
        }
    }
}