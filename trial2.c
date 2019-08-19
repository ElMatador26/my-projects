#include<stdio.h>
#include<stdlib.h>
typedef struct f
{
    int x, y;

}xy;
void print(int *arr, int n)
{
    int i, j;
    for(i=0; i<n; i++)
    {
        for(j=0; j<n; j++)
            {
                if(arr[i*n+j]!=-1)
                printf("%d ", arr[i*n+j]);
                else
                    printf("s ");
            }
        printf("\n");
    }
}
void search(int *mat, int n ,int i, xy s, xy ob)
{
    if(mat[(s.y)*n+s.x]!=-1)
            {

                mat[(s.y)*n+s.x]=i;

            }
        if(ob.x!=s.x || ob.y!=s.y)
    {
        if(s.x<n-1)
           {
               if(mat[s.x+1+(s.y)*n]>i+1 || mat[s.x+1+(s.y)*n]==0)
               {
                   s.x=s.x+1;
                   search(mat, n, i+1, s, ob);
                   s.x=s.x-1;
                }
           }
            if(s.x>0)
            {

             if(mat[s.x-1+(s.y)*n]>i+1 || mat[s.x-1+(s.y)*n]==0)
             {
                 s.x=s.x-1;
                 search(mat, n, i+1, s, ob);
                 s.x=s.x+1;
             }
         }
         if(s.y<n-1)
           {
               if(mat[s.x+(s.y+1)*n]>(i+1) || mat[s.x+(s.y+1)*n]==0)
               {
                   s.y=s.y+1;
                   search(mat, n, i+1, s, ob);
                   s.y=s.y-1;

                }
           }
           if(s.y>0)
           {
             if(mat[s.x+(s.y-1)*n]>i+1 || mat[s.x+(s.y-1)*n]==0)
             {
                 s.y=s.y-1;
                 search(mat, n, i+1, s, ob);
                 s.y=s.y+1;

             }
         }


    }


}

void main()
{
    int*arr, n, k, j;
    xy s, ob, obs;
    printf("Enter the value of n: ");
    scanf("%d", &n);
    arr=calloc(n*n, sizeof(int));
    printf("Enter x-coordinate of object: ");
    scanf("%d", &(ob.x));
    printf("Enter y-coordinate of object: ");
    scanf("%d", &(ob.y));
    printf("Enter x-coordinate ofsource: ");
    scanf("%d", &(s.x));
    printf("Enter y-coordinate ofsource: ");
    scanf("%d", &(s.y));

            arr[(s.y)*n+s.x]=-1;
    printf("Enter the number of obstacles: ");
    scanf("%d",&k);
    for(j=1; j<=k; j++)
    {
        printf("Enter x-coordinate of obstacle %d: ", j);
        scanf("%d",&(obs.x));
        printf("Enter y-coordinate of obstacle %d: ", j);
        scanf("%d",&(obs.y));
        arr[(obs.y)*n+obs.x]=-1;

    }
    search(arr, n, 0, s, ob);

    printf("The shortest number of steps: %d", arr[(ob.y)*n+ob.x]);
}
