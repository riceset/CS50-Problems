#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    //Gets input from the user:
    float dollar;

    do
    {
        dollar = get_float("Change Owed: ");
    }
    while (dollar < 0);

    //converting user input in float to integers:
    int cents = round(dollar * 100);

    //How many coins you used. (counter to print)
    int coins = 0;

    //Coin values:
    float quarter = 25;
    float dime = 10;
    float nickel = 5;
    float penny = 1;

    //checks if the value entered by the user is greater or equal than 25. If so, you add 1 to the
    //coin counter and make the value entered the value itself minus 25. (eg: 40 = 40 - 25) that is
    //15. so now 40 is 15.

    while (cents >= quarter)
    {
        coins++;
        cents = cents - quarter;
    }

    while (cents >= dime)
    {
        coins++;
        cents = cents - dime;
    }

    while (cents >= nickel)
    {
        coins++;
        cents = cents - nickel;
    }

    while (cents >= penny)
    {
        coins++;
        cents = cents - penny;
    }

    printf("%i\n", coins);
}