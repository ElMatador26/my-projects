#include<stdio.h>
#include<stdlib.h>
typedef struct Node
{
    int data, h;
    struct Node *left, *right;
}node;
node *insert(node *head, node *head2)
{
    int l, r;
    if(head==NULL)
    {
         if(head2->h<=1)
        return head2;
        else
        {
            head2->h=0;
            if(head->left==NULL)
            {
                head=head2->right;
                head2->right=NULL;
            }
            else
            {
                head=head2->left;
                head2->left=NULL;
            }
                return insert(head, head2);


        }
    }
    if(head->data > head2->data)
        head->left=insert(head->left, head2);

    else
            head->right=insert(head->right, head2);


        if(head->left==NULL)
            l=0;
        else
            l=(head->left)->h+1;
        if(head->right==NULL)
            r=0;
        else
            r=(head->right)->h+1;
            if(l-r >-2 && l-r < 2)
            {
                head->h=(l>=r)?l:r;
                return head;
            }
        if(l-r > 1)
            {
                head2=head->left;
                head->left=NULL;
                head->h=r;

            }
        if(l-r<-1)
        {
            head2=head->right;
            head->right=NULL;
            head->h=l;
        }
        return insert(head2, head);

}
node *add(node *head, int i)
{
    node *head2=(node *)malloc(sizeof(node));
    head2->data=i;
    head2->h=0;
    head2->left=NULL;
    head2->right=NULL;
    if(head==NULL)
        return head2;
        return insert(head, head2);



}

void see(node *head)
{
    int l, r;
    if(head!=NULL)
    {
        see(head->left);
        if(head->left==NULL)
            l=0;
        else
            l=(head->left)->h+1;
        if(head->right==NULL)
            r=0;
        else
            r=(head->right)->h+1;

        printf("data=%d balance=%d\n", head->data, l-r);
        see(head->right);
    }
}

void main()
{
    node *head=NULL;
    int i;
    while(i!=0)
    {printf("Enter the number: ");
    scanf("%d", &i);
    head=add(head, i);
    }
    see(head);
}
