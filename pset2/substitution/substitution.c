#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

bool validKey(string key);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Error: Missing or Incompatible Command Line Argument\n");
        return 1;
    }

    string key = argv[1];
    if (validKey(key) == true)
    {
        string plaintext = get_string("plaintext: ");
        int length = strlen(plaintext);
        printf("ciphertext: ");
        
        for (int i = 0; i < length; i ++)
        {
            if ((int)plaintext[i] > 96 && (int)plaintext[i] < 123)
            {
                
                printf("%c", tolower(key[(int)plaintext[i] - 97]));
            }
            else if ((int)plaintext[i] > 64 && (int)plaintext[i] < 91)
            {
                
                printf("%c", toupper(key[(int)plaintext[i] - 65]));
            }
            else 
            {
                printf("%c", plaintext[i]);
            }
        }
        printf("\n");

    }
    else
    {
        printf("Invalid Key\n");
        return 1;
    }
}
bool validKey(string key)
{
    int inalphabet = 0;
    if (strlen(key) == 26)
    {
        for (char i = 'a'; i <= 'z'; i++)
        {
            for (int k = 0; k < 26; k++)
            {
                if (tolower(key[k]) == i)
                {
                    inalphabet ++;
                    break;
                }
            }
        }
        if (inalphabet == 26)
        {
            return true;
        }
        else
        {
            return false;
        }
    }
    else
    {
        return false;
    }
}