#include<stdio.h>
#include<stdlib.h>
typedef struct node
{
    struct node *link;
    int data;
}queue;

queue *add(queue *front, int i)
{
    queue *head;
    head=(queue *)malloc(sizeof(queue));
    head->data=i;
    head->link=head;
    if(front==NULL)
        return head;
    head->link=front->link;
    front->link=head;
    return head;
}
queue *delete(queue *front)
{
    queue *head;
    if(front==NULL)
    {
        printf("Empty queue\n");
        return NULL;
    }
    if(front->link==front)
    {
        free(front);
        return NULL;
    }
    head=front->link;
    front->link=head->link;
    free(head);
    return front;
}
void see(queue *front)
{
    queue *head;
    if(front==NULL)
        printf("Empty queue\n");
    else
    {
        head=front->link;
        while(1)
        {
            printf("%d ", head->data);
            if(head==front)
                break;
            head=head->link;
        }
        printf("\n");
    }
}
int main()
{
    queue *front=NULL;
    int i=1;
    while(i!=0)
    {
        printf("Enter\n0 to exit,\n1 to add,\n2 to delete and\n3 to view the list: ");
        scanf("%d", &i);
        if(i==1)
        {
            printf("Enter the number to add: ");
            scanf("%d", &i);
            front=add(front, i);
            i=1;
            continue;
        }
        if(i==2)
        {
            front=delete(front);
            continue;
        }
        if(i==3)
        {
            see(front);
            continue;
        }
        if(i!=0)
            printf("Wrong input, try again:\n");
    }
    return 0;
}
