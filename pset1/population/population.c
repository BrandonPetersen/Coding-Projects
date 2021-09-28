#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO: Prompt for start size
    int start;
    do
    {
        start = get_int("Starting Size: ");
    }
    while (start < 9);
    

    // TODO: Prompt for end size
    int end;
    do
    {
        end = get_int("Ending Size: ");
    }
    while (end < start);

    // TODO: Calculate number of years until we reach threshold
    int population = start;
    int years = 0;
    while (population < end)
    {
        population += population / 3 - population / 4;
        years++;
    }

    // TODO: Print number of years
    printf("Years: %i\n", years);
}