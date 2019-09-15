#include<stdio.h>
#include<stdlib.h>
typedef struct Node
{
    int i;
    struct Node *link;
}node;
node *add(node *tail, int j)
{
    if(tail==NULL)
        tail=(node *)malloc(sizeof(node));
    else
    {
        tail->link=(node *)malloc(sizeof(node));
        tail=tail->link;
    }
    tail->link=NULL;
    tail->i=j;
    return tail;

}
node *merge(int *arr, node *head1, node *head2)
{
    int c=0;
    node *head3=NULL, *tail=NULL;
    while(head1!=NULL && head2!=NULL)
    {
        if(head1->i < head2->i)
        {
            arr[c]=head1->i;
            head1=head1->link;
        }
        else
        {
            arr[c]=head2->i;
            head2=head2->link;
        }
        tail=add(tail, arr[c]);
        if(head3==NULL)
            head3=tail;
        c++;
    }
    if(head1==NULL)
    {
        while(head2!=NULL)
        {
            arr[c]=head2->i;
            tail=add(tail, arr[c]);
            if(head3==NULL)
                head3=tail;
            c++;
            head2=head2->link;
        }
    }
    if(head2==NULL)
    {
        while(head1!=NULL)
        {
            arr[c]=head1->i;
            tail=add(tail, arr[c]);
            if(head3==NULL)
                head3=tail;
            c++;
            head1=head1->link;
        }
    }
    return head3;

}
void neosort(int *arr, int n)
{
    int i, c=0;
    node *head1, *tail, *head2;
    head1=tail=NULL;
    head2=NULL;
    for(i=0; i<n; i++)
    {
        tail=add(tail, arr[i]);
            if(c==0 && head1==NULL)
                head1=tail;
             if(head2==NULL && c==1)
                head2=tail;
        if(arr[i] > arr[i+1] || i==n-1)
        {
            tail=NULL;
            c++;
            if(c==2)
            {
                head1=merge(arr, head1, head2);
                head2=NULL;
                c=1;
            }
        }

    }

}

void main()
{
    int *arr, n, i;
    printf("Enter the number of elements: ");
    scanf("%d", &n);
    arr=(int *)malloc(n*sizeof(int));
    for(i=0; i<n; i++)
    {
        printf("Enter the element: ");
        scanf("%d", &arr[i]);
    }
    neosort(arr, n);
    for(i=0; i<n; i++)
        printf("%d ", arr[i]);

}
