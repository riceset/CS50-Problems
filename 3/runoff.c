#include <cs50.h>
#include <stdio.h>
#include <string.h>

typedef struct
{
    string name;
    int votes;
    bool eliminated;
} candidate;

// Defines the max number of voters and candidates
#define MAX_VOTERS 100
#define MAX_CANDIDATES 9

//The candidate preference "j" for voter i
int preferences[MAX_VOTERS][MAX_CANDIDATES];

// An array of candidates (can contain up to 9 candidates)
candidate candidates[MAX_CANDIDATES];

//Number of voters and candidates
int voter_count;
int candidate_count;

//Prototypes
bool vote(int voter, int rank, string name);
void tabulate(void);
bool print_winner(void);
int find_min(void);
bool is_tie(int min);
void eliminate(int min);

//We give the candidates on argv
int main(int argc, string argv[])
{
    //If the user didn't enter a candidate name
    if (argc < 2)
    {
        printf("Usage: runoff [candidate ...]\n");
        return 1;
    }

    //Assigns candidate_count the number of candidate names entered
    candidate_count = argc - 1;

    //If the user entered more than 9 candidate names
    if (candidate_count > MAX_CANDIDATES)
    {
        printf("Maximum number of candidates is %i\n", MAX_CANDIDATES);
        return 2;
    }

    //Populates the candidates array initializing the name instance
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
        candidates[i].eliminated = false;
    }

    //Prompts for the number of voters
    voter_count = get_int("Number of voters: ");

    //If the user entered a number greater than 100
    if (voter_count > MAX_VOTERS)
    {
        printf("Maximum number of voters is %i\n", MAX_VOTERS);
        return 3;
    }

    //Vertical list of all the voters
    for (int i = 0; i < voter_count; i++)
    {
        //Horizontal list of all the preferences for voter i
        for (int j = 0; j < candidate_count; j++)
        {
            //NOTE: + 1 is for displaying Rank 1 instead of Rank 0
            //when asking for the preference.

            //Query for each rank for candidate i (rank = preference)
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(i, j, name))
            {
                printf("Invalid vote.\n");
                return 4;
            }
        }
        //Prints a new line for visually separating each voter
        printf("\n");
    }

    // Keep holding runoffs until winner exists
    while (true)
    {
        // Calculate votes given remaining candidates
        tabulate();

        // Check if election has been won
        bool won = print_winner();
        if (won)
        {
            break;
        }

        // Eliminate last-place candidates
        int min = find_min();
        bool tie = is_tie(min);

        // If tie, everyone wins
        if (tie)
        {
            for (int i = 0; i < candidate_count; i++)
            {
                if (!candidates[i].eliminated)
                {
                    printf("%s\n", candidates[i].name);
                }
            }
            break;
        }

        // Eliminate anyone with minimum number of votes
        eliminate(min);

        // Reset vote counts back to zero
        for (int i = 0; i < candidate_count; i++)
        {
            candidates[i].votes = 0;
        }
    }

    return 0;
}

bool vote(int voter, int rank, string name)
{
    //For each candidate (entered on argv)
    for (int i = 0; i < candidate_count; i++)
    {
        //compare if this candidate's name is iqual to the voted candidate
        if (strcmp(name, candidates[i].name) == 0)
        {
            //If so, assign their position from the candidates vector to
            //the preference of voter i (inside the preferences matrix)
            preferences[voter][rank] = i;
            return true;
        }
    }

    return false;
}

void tabulate(void)
{
    //Updates the vote count for all non-eliminated candidates
    for (int i = 0; i < voter_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            //preference holds the candidate index so, candidates[preferences[i][j]]
            //would be, if Alice has index 0 on the candidates array and the voter
            //voted for Alice, candidates[0] will be Alice, adding 1 vote for her
            //and then breaking from the loop.
            if (!candidates[preferences[i][j]].eliminated)
            {
                candidates[preferences[i][j]].votes++;
                break;
            }
        }
    }
}

// Print the winner of the election, if there is one
bool print_winner(void)
{
    int majority = voter_count / 2;

    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].votes > majority)
        {
            printf("%s\n", candidates[i].name);
            return true;
        }
    }
    return false;
}

// Return the minimum number of votes any remaining candidate has
int find_min(void)
{
    int min = MAX_VOTERS;

    for (int i = 0; i < candidate_count; i++)
    {

        if (!candidates[i].eliminated && candidates[i].votes < min)
        {
            min = candidates[i].votes;
        }
    }
    return min;
}

// Return true if the election is tied between all candidates, false otherwise
bool is_tie(int min)
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (!candidates[i].eliminated && candidates[i].votes != min)
        {
            return false;
        }
    }
    return true;
}

// Eliminate the candidate (or candidates) in last place
void eliminate(int min)
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (!candidates[i].eliminated && candidates[i].votes == min)
        {
            candidates[i].eliminated = true;
        }
    }
    return;
}
