#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<omp.h>

#define N 1024
#define LIMIT 1000000

void print_domain(double domain[N+1][N+1]) {
    int step = floor(N/8), i, j;
    printf("*******************************************************\n");
    for (i = 1; i <= N; i+=step) {
        for (j = 1; j <= N; j+=step)
            printf("%f ", domain[i][j]);
        printf("\n");
    }
    printf("*******************************************************\n\n\n");
}