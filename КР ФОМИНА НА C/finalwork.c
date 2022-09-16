#define _CRT_SECURE_NO_WARNINGS
#include <stdlib.h>
#include <stdio.h>
#include <virtdisp.h>


int main()
{
    const int w = 1000;
    const int h = 1000;
    int count = 0;
    int x = 0;
    int y = 0;
    int layer = 0;
    double newx = 0;
    double newy = 0;
    double drawx = 0;
    double drawy = 0;

    while (layer < 5)
    {
        char filename[23];
        char filename_number[10];

        unsigned char image[1000 * 1000];
        sprintf(filename, "layers/layer-%d-a.raw", layer);

        cn_connect(NULL, 0);
        sprintf(filename_number, "layer%d", layer);
        cn_auth("g01-egorov", "QKRnTE");
        cn_select(filename_number);
        cn_size(500, 500);
        cn_clear();
        stroke(0, 0, 0, 255);
        draw_line(0, 0, 0, 500); //-линия
        draw_line(0, 500, 500, 500); //-линия
        draw_line(500, 500, 500, 0); //-линия
        draw_line(500, 0, 0, 0); //-линия
        stroke(0, 0, 255, 255);
        draw_line(250, 0, 250, 375); //-линия
        stroke(255, 0, 0, 255);
        draw_line(500 - 375, 250, 500, 250); //-линия
        

        FILE* f;
        f = fopen(filename, "rb");
        fread(image, sizeof(unsigned char), w * h, f);
        for (int i = 0; i < (w * h); i++)
        {
            if (image[i] < 127)
            {
                y = i / 1000;
                x = (500 - (i - (y * 1000)));
                newx = (double)x;
                newx /= 1000;
                newy = (double)y;
                newy = (500 - newy) / 1000;
                newx = -newx;
                newy = -newy;
                printf("%d %d  %.2f  %.2f\n", layer, count, newx, newy);
                
                //drawing
                drawx = (newx * 500) + 250;
                drawy = (newy * 500) + 250;
                stroke(255, 0, 255, 255);
                draw_line(drawx - 8, drawy - 8, drawx + 8, drawy + 8); //-линия
                draw_line(drawx + 8, drawy - 8, drawx - 8, drawy + 8); //-линия
                count++;
            }

            //printf("%d\n", image[i]);
        }
        fclose(f);
        layer++;
        count = 0;
        cn_sync();
        cn_disconnect();
    }




    return 0;
}