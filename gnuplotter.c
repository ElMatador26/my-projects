#include<stdio.h>
#include<stdlib.h>
#include<sys/time.h>
#define Time(a,b) ((a*1000000)+b)
typedef struct DATA
{
    int size;
    long long int bsort, msort;
}data;
void bsort(int *arr, int n)
{
    int i, j;
    for(i=n-2; i>0; i--)
        for(j=0; j<=i; j++)
            if(arr[j]>arr[j+1])
            {
                arr[j]=arr[j]+arr[j+1];
                arr[j+1]=arr[j]-arr[j+1];
                arr[j]=arr[j]-arr[j+1];
            }


}
void merge(int *arr, int low, int high)
{
    int *arr2, low2, high2, n, i;
    n=high-low+1;
    arr2=(int *)malloc(n*sizeof(int));
    low2=low;
    high2=(low+high)/2;
    high2++;
    i=0;
    while(low2<=(low+high)/2 || high2<=high)
    {

        if(arr[low2]<arr[high2])
        {
            if(low2<=(low+high)/2)
            {arr2[i]=arr[low2];
            low2++;}
            else
            {
                arr2[i]=arr[high2];
                high2++;
            }
        }
        else
        {
            if(high2<=high)
            {arr2[i]=arr[high2];
            high2++;}
            else
            {
                arr2[i]=arr[low2];
                low2++;
            }
        }
        i++;
    }
    for(i=0; i<n; i++)
    {
        arr[low]=arr2[i];
        low++;
    }
    free(arr2);
}

void divide(int *arr, int low, int high)
{
    int mid;
    if(low!=high)
    {

        mid=(low+high)/2;
        divide(arr, low, mid);
        divide(arr, mid+1, high);
        merge(arr, low, high);

    }
}

int digits(long long int i)
{
    int c=0;

    while(i!=0)
    {

               c++;
               i=i/10;

    }
    return c;
}
void print(data store, FILE *fp)
{
    int i, j;
    fprintf(fp, "%d", store.size);
    i=digits(store.size);
    for(j=0; j<19-i; j++)
        fprintf(fp, " ");
    fprintf(fp, "%lld", store.bsort);
    i=digits(store.bsort);
    for(j=0; j<14-i; j++)
        fprintf(fp, " ");
    fprintf(fp, "%lld\n", store.msort);
    printf("\n%d printing successful", store.size);

}
void main()
{
    srand(time(0));
    int i, n, *arr, *arr2;
    long long int t, t2, t3=0;
    data store, copy;
    struct timeval start, end;
    FILE *fp;
    fp=fopen("time.dat", "wb");
    fprintf(fp, "No. of elements    bsort_time    msort_time\n");
    for(n=10; n<=15000; n++)
    {

        arr=(int *)malloc(n*sizeof(int));
        arr2=(int *)malloc(n*sizeof(int));
        for(i=0; i<n; i++)
        {
            arr[i]=rand();
            arr2[i]=arr[i];
        }
        store.size=n;
        gettimeofday(&start, NULL);
        bsort(arr, n);
        gettimeofday(&end, NULL);
        t=(long long int)(end.tv_sec-start.tv_sec);
        t2=(long long int)(end.tv_usec-start.tv_usec);
        store.bsort=Time(t, t2);
        fflush(stdin);
        gettimeofday(&start, NULL);
        divide(arr2, 0, n-1);
        gettimeofday(&end, NULL);
        t=(long)(end.tv_sec-start.tv_sec);
        t2=(long)(end.tv_usec-start.tv_usec);
        store.msort=Time(t, t2);
        if(store.bsort>0 && store.msort>t3)
        print(store, fp);
        t3=store.msort;
        free(arr);
        free(arr2);
    }
    fclose(fp);

}
