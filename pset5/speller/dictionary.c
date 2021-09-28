// Implements a dictionary's functionality

#include <stdbool.h>
#include "dictionary.h"
#include <cs50.h>
#include <stdio.h>
#include <math.h>
#include <ctype.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 100;

unsigned int wc = 0;
// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int value = hash(word);
    
    node *p = table[value];
    
    while (p != NULL)
    {
        if (strcasecmp(word, p->word) == 0)
        {
            return true;
        }
        p = p->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned int hashvalue = 0;
    int k = 0;
    while (word[k] != '\0')
    {
        hashvalue += tolower(word[k]);
        k++;
    }
    return hashvalue % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *read = fopen(dictionary, "r");
    if (read == NULL)
    {
        return false;
    }
    
    char buffer[LENGTH + 1];
    while (fscanf(read, "%s", buffer) != EOF)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }
        
        strcpy(n->word, buffer);
        int hashvalue = hash(n->word);
        n->next = table[hashvalue];
        table[hashvalue] = n;
        wc++;
    }    
    fclose(read);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return wc;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *tmp = table[i];
        while (tmp != NULL)
        {
            node *p = tmp;
            tmp = tmp->next;
            free(p);
        }
    }
    return true;
}
