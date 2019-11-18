#include<stdio.h>
#define MAX 5

typedef struct queue
{
    int arr[MAX], front, rear, n;
}queue;

queue add(queue q, int i)
{
    if(q.n==MAX)
    {
        printf("Queue is full:\n");
        return q;
    }
    q.front=(q.front+1)%MAX;
    q.arr[q.front]=i;
    q.n=q.n+1;
    return q;
}
queue delete(queue q)
{
    if(q.n==0)
    {
        printf("Queue is empty:\n");
        return q;
    }
    q.n=q.n-1;
    printf("The deleted element is %d\n", q.arr[q.rear]);
    q.rear=(q.rear+1)%MAX;
    return q;
}
void see(queue q)
{
    if(q.n==0)
    {
        printf("Queue is empty:\n");
        return;
    }
    while(1)
    {
        printf("%d ", q.arr[q.rear]);
        if(q.rear==q.front)
            break;
        q.rear=(q.rear+1)%MAX;
    }
    printf("\n");
}
int main()
{
    int i=1;
    queue q;
    q.n=0;
    q.front=-1;
    q.rear=0;
    while(i!=0)
    {
        printf("Enter \n0 to exit, \n1 to add, \n2 to delete and \n3 to see the queue: ");
        scanf("%d", &i);
        if(i==1)
        {
            printf("Enter the number: ");
            scanf("%d", &i);
            q=add(q, i);
            i=1;
            continue;
        }
        if(i==2)
        {
            q=delete(q);
            continue;
        }
        if(i==3)
        {
            see(q);
            continue;
        }
        if(i!=0)
            printf("Wrong input, try again:\n");
    }

    return 0;
}
