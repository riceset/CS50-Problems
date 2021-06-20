#include <stdio.h>
#include <cs50.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>


int main(void)
{
    //First Input:
    long cardNum = 0;

    do
    {
        cardNum = get_long("Number: ");
    }
    while (cardNum < 1);

    long cardNumCp = cardNum;
    long cardNumCp2 = cardNum;

    int even;
    int odd;

    int cardNumArray[16];
    int counter = 0;
    int total = 0;

    //Checksum:
    for (int i = 0; i < 16; i++)
    {
        //Gets the last digit:
        int singleNum = cardNum % 10;
        cardNum /= 10;

        //Assigns the single numbers to an array:
        cardNumArray[i] = singleNum;

        counter++;

        //Even:
        if (counter % 2 == 0)
        {
            //Assigns every even number from the cardNumArray to even.
            even = cardNumArray[i];

            even *= 2;

            //If there's a number greater than 10
            if (even >= 10)
            {
                //Get the decimal part
                int decimal = even / 10;
                //The remainder
                int remain = even % 10;
                //sum
                even = decimal + remain;
            }

            total += even;
        }
        else
        {
            //Assigns every odd number from the cardNumArray to odd.
            odd = cardNumArray[i];

            //Adds to the current total (13 -> 20)
            total += odd;
        }
    }

    //If the last digit of total is 0:
    if (total % 10 == 0)
    {
        //Calculates the number of digits in the card:
        int digits = 0;
        do
        {
            cardNumCp /= 10;
            digits++;
        }
        while (cardNumCp != 0);

        //Checks first digits:
        long n1 = cardNumCp2, firstTwo = cardNumCp2;
        while (cardNumCp2)
        {
            firstTwo = n1;
            n1 = cardNumCp2;
            cardNumCp2 /= 10;
        }

        //Turns 40~49 into 4 for checking Visa card:
        if (firstTwo >= 40 && firstTwo <= 49)
        {
            firstTwo /= 10;
        }


        //Checks the card brand:

        //American Express:
        if (digits == 15 && (firstTwo == 34 || firstTwo == 37))
        {
            printf("AMEX\n");
        }

        //Master Card:
        else if (digits == 16 && (firstTwo >= 51 && firstTwo <= 55))
        {
            printf("MASTERCARD\n");
        }

        //Visa
        else if ((digits == 13 || digits == 16) && firstTwo == 4)
        {
            printf("VISA\n");
        }

        else
        {
            printf("INVALID\n");
        }
    }
    //printf("total: %i\n", total);
}