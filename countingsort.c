#include<stdio.h>
#include<stdlib.h>

void csort(int *arr, int n)
{
    int j=0, i, s, *arr2;
    for(i=0; i<n; i++)
    {
        if(i==0 || s<arr[i])
            s=arr[i];
    }
    printf("s=%d\n", s);
    arr2=(int *)calloc(s+1, sizeof(int));
    for(i=0; i<n; i++)
        arr2[arr[i]]++;
    for(i=0; i<=s; i++)
        printf("%d ", arr2[i]);
    for(i=0; i<=s; i++)
    {
        if(arr2[i] > 0)
        {
            arr2[i]--;
            arr[j]=i;
            i--;
            j++;
        }
    }
}


int main()
{
    int arr[100], n, i;
    printf("Enter the number of elements: ");
    scanf("%d", &n);
    for(i=0; i<n; i++)
    {
        printf("Enter the element number %d: ", i);
        scanf("%d", &arr[i]);

    }
    csort(arr, n);
    printf("The sorted array is:\n");
    for(i=0; i<n; i++)
        printf("%d ", arr[i]);
}
