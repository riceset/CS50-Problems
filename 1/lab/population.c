#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int start_population = 0, end_population = 0, years = 0, gain = 0, lose = 0;

    //Minimum size allowed is 9
    do
        start_population = get_int("Start size: ");

    while (start_population < 9);

    do
        end_population = get_int("End size: ");

    while (end_population < start_population);
    
    int population = start_population;

    while (population < end_population)
    {
        gain = population / 3, lose = population / 4;
        population = population + gain - lose;
        years++;
    }

    printf("Years: %d\n", years);
}
