#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);
    

    for (int i = 0; i < height; i++)
    {
        int k = height - i;
        k--;
        while (k > 0)
        {
            printf(" ");
            k--;
        }
        int t = i;
        while (t >= 0)
        {
            printf("#");
            t--;
        }
        printf("  ");
        t = i;
        while (t >= 0)
        {
            printf("#");
            t--;
        }
        printf("\n");
        
        
    }

}