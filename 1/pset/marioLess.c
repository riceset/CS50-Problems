#include <stdio.h>
#include <cs50.h>

int main(void)
{
    //Block height and width:
    int height;
    int width = 1;

    //Prompts the user to enter a value between 1...8
    do
    {
        height = get_int("Height: ");
    }
    while (height > 8 || height < 1);

    //The number of spaces (previously dots) on the left side of the pyramid:
    int dots = height - 1;

    //Pyramid:

    for (int i = 0; i < height; i++)
    {
        //space on the left of the pyramid
        for (int a = 0; a < dots; a++)
        {
            printf(" ");
        }
        //Pyramid:
        for (int j = 0; j < width; j++)
        {
            printf("#");
        }

        //removes 1 dot per iteration:
        dots--;

        //Increases the width of the pyramids per interation:
        width++;

        //prints a new line from top to bottom:
        printf("\n");
    }
}
