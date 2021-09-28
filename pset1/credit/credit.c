#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    long number;
    long digits;
    int count = 0;
    
    do
    {
        number = get_long("Number: ");
    }
    while (number < 0);
    
    digits = number;
    
    while (digits > 0)
    {
        digits = digits / 10;
        count++;
    }
    if (count != 13 && count != 15 && count != 16)
    {
        printf("INVALID\n");
        return 0;
    }
    
    long card = number;
    int sum = 0;
    int product = 0;
    
    do
    {
        if (count == 16 || count == 13 || count == 15)
        {
            sum += card % 10;
            card = card / 10;
            product += card % 10;
            product += card % 10;
            sum += product % 10;
            product = product / 10;
            sum += product % 10;
            card = card / 10;
            product = 0;
        }
        
    }
    while (card > 0);
         
    if (sum % 10 != 0)
    {
        printf("INVALID\n");
        return 0;
    }
    
   
    
    long f2d = number;
    do
    {
        f2d = f2d / 10;
    }
    while (f2d > 100);
    
    if ((f2d / 10 == 5) && (0 < f2d % 10 && f2d % 10 < 6))
    {
        printf("MASTERCARD\n");
    }
    else if ((f2d / 10 == 3) && (f2d % 10 == 4 || f2d % 10 == 7))
    {
        printf("AMEX\n");
    }
    else if (f2d / 10 == 4)
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }
    
}