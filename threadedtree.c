#include<stdio.h>
#include<stdlib.h>

typedef struct node
{
    int data, i;
    struct node *left, *right;
}node;
node *add(node *head, int key)
{
    node *head2, *head3=head;
    head2=(node *)malloc(sizeof(node));
    head2->left=head2;
    head2->data=key;
    head2->i=1;
    head2->right=NULL;
    if(head==NULL)
        return head2;
    while(1)
    {
        if(head->data > head2->data)
        {
            if(head->left==head)
                {
                    head->left=head2;
                    head2->right=head;
                    head2->i=1;
                    return head3;
                }
                head=head->left;
        }
        else
        {
            if(head->i==1)
            {
                head2->right=head->right;
                head->right=head2;
                head->i=-1;
                head2->i=1;
                return head3;
            }
            head=head->right;

        }
    }
}
void see(node *head)
{
    while(head!=NULL)
    {
        head->i++;
        if(head->i%2==0)
            head=head->left;
        else
        {
            printf("%d ", head->data);
            head->i=head->i-2;
            head=head->right;
        }
    }
}
void main()
{
    node *head=NULL;
    int i=1;
    while(i!=0)
    {
        printf("Enter new element: ");
        scanf("%d", &i);
        head=add(head, i);
    }
    see(head);
}
