#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(void)
{
    int letters = 0;
    int words = 1;
    int sentences = 0;
    
    string text = get_string("Text: ");
    int length = strlen(text);
    
    for (int i = 0; i < length; i++)
    {
        if (((int)text[i] > 96 && (int)text[i] < 123) || ((int)text[i] > 64 && (int)text[i] < 91))
        {
            letters++;
        }
        else if ((int)text[i] == 32)
        {
            words++;
        }
        else if ((int)text[i] == 33 || (int)text[i] == 46 || (int)text[i] == 63)
        {
            sentences++;
        }
    }
    
    float L = (float)letters / ((float)words / 100);
    float S = (float) sentences / ((float)words / 100);
    
    float index = 0.0588 * L - 0.296 * S - 15.8;
    index = rint(index);
    
    if (1.0 <= index && index < 16.0)
    {
        printf("Grade %f", index);
    }
        
    else if (index < 1.0)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16.0)
    {
        printf("Grade 16+\n");
    }
}