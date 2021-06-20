#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

typedef uint8_t BYTE;
#define BLOCK_SIZE 512

bool is_jpeg(BYTE block[]);

int main(int argc, char *argv[])
{
    //Checks for command line arguments
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }
    
    //Opens the memory card
    FILE *card = fopen(argv[1], "r");
    if (!card)
    {
        printf("Could not open file.\n");
        return 1;
    }

    BYTE block[BLOCK_SIZE];
    int jpeg_counter = 0;
    char filename[8];
    FILE *image;
    bool first_jpeg = false;

    while (fread(block, sizeof(BYTE), BLOCK_SIZE, card))
    {

        if (is_jpeg(block))
        {
            first_jpeg = true;

            //Close the last jpeg (if not the first)
            if (jpeg_counter != 0)
            {
                fclose(image);
            }
            
            //Creates a new jpeg
            sprintf(filename, "%03i.jpg", jpeg_counter);
            image = fopen(filename, "w");
            jpeg_counter++;
            fwrite(block, sizeof(BYTE), BLOCK_SIZE, image);
        }

        else if (!first_jpeg)
        {
            continue;
        }

        else
        {
            fwrite(block, sizeof(BYTE), BLOCK_SIZE, image);
        }
    }

    fclose(card);
    fclose(image);

    return 0;
}

bool is_jpeg(BYTE block[])
{
    return
        block[0] == 0xff &&
        block[1] == 0xd8 &&
        block[2] == 0xff &&
        (block[3] & 0xf0) == 0xe0;
}
