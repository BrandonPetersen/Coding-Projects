#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i ++)
    {
        for (int k = 0; k < width; k++)
        {
            float red = image[i][k].rgbtRed;
            float green = image[i][k].rgbtGreen;
            float blue = image[i][k].rgbtBlue;
            
            float grey = (red + green + blue) / 3;
            int grey1 = round(grey);
        
            image[i][k].rgbtRed = grey1;
            image[i][k].rgbtBlue = grey1;
            image[i][k].rgbtGreen = grey1;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i ++)
    {
        for (int k = 0; k < (width / 2); k ++)
        {
            int red = image[i][k].rgbtRed;
            int green = image[i][k].rgbtGreen;
            int blue = image[i][k].rgbtBlue;
            
            image[i][k].rgbtRed = image[i][width - (k + 1)].rgbtRed;
            image[i][k].rgbtBlue = image[i][width - (k + 1)].rgbtBlue;
            image[i][k].rgbtGreen = image[i][width - (k + 1)].rgbtGreen;
            
            image[i][width - (k + 1)].rgbtRed = red;
            image[i][width - (k + 1)].rgbtBlue = blue;
            image[i][width - (k + 1)].rgbtGreen = green;
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
    float blue;
    float green;
    float red; 
    float pixels;
    for (int i = 0; i < height; i ++)
    {
        for (int k = 0; k < width; k++)
        {
            temp[i][k] = image[i][k];
        }
    }
    
    for (int i = 0; i < height; i ++)
    {
        for (int k = 0; k < width; k++)
        {
            blue = 0;
            green = 0;
            red = 0;
            pixels = 0.0;
            for (int j = -1; j < 2; j++)
            {
                if ((i + j) < 0 || (i + j) >= height)
                {
                    continue;
                }
                for (int v = -1; v < 2; v++)
                {
                    if ((k + v) < 0 || (k + v) >= width)
                    {
                        continue;
                    }
                    blue += temp[j + i][v + k].rgbtBlue;
                    red += temp[j + i][v + k].rgbtRed;
                    green += temp[j + i][v + k].rgbtGreen;
                    pixels++;
                }
            }
            image[i][k].rgbtBlue = round(blue / pixels);
            image[i][k].rgbtRed = round(red / pixels);
            image[i][k].rgbtGreen = round(green / pixels);
        
        }
    }
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
    float blue;
    float green;
    float red; 
    float pixels;
    int xEdge[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int yEdge[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};
    for (int i = 0; i < height; i ++)
    {
        for (int k = 0; k < width; k++)
        {
            temp[i][k] = image[i][k];
        }
    }
    
    for (int i = 0; i < height; i ++)
    {
        for (int k = 0; k < width; k++)
        {
            blue = 0;
            green = 0;
            red = 0;
            pixels = 0.0;
            
            int blueX = 0;
            int blueY = 0;
            int redX = 0;
            int redY = 0;
            int greenX = 0;
            int greenY = 0;
            
            for (int j = -1; j < 2; j++)
            {
                if ((i + j) < 0 || (i + j) >= height)
                {
                    continue;
                }
                for (int v = -1; v < 2; v++)
                {
                    if ((k + v) < 0 || (k + v) >= width)
                    {
                        continue;
                    }
                    blueX += temp[j + i][v + k].rgbtBlue * xEdge[j + 1][v + 1];
                    blueY += temp[j + i][v + k].rgbtBlue * yEdge[j + 1][v + 1];
                    redX += temp[j + i][v + k].rgbtRed * xEdge[j + 1][v + 1];
                    redY += temp[j + i][v + k].rgbtRed * yEdge[j + 1][v + 1];
                    greenX += temp[j + i][v + k].rgbtGreen * xEdge[j + 1][v + 1];
                    greenY += temp[j + i][v + k].rgbtGreen * yEdge[j + 1][v + 1];
                    pixels++;
                }
            }
            blue = round(sqrt((float)blueX * blueX  + (float)blueY * blueY));
            red = round(sqrt((float)redX * redX  + (float)redY * redY));
            green = round(sqrt((float)greenX * greenX  + (float)greenY * greenY));
            
            if (blue > 255)
            {
                blue = 255;
            }
            if (red > 255)
            {
                red = 255;
            }
            if (green > 255)
            {
                green = 255;
            }
            
            
            image[i][k].rgbtBlue = blue;
            image[i][k].rgbtRed = red;
            image[i][k].rgbtGreen = green;
        
        }
    }
}
