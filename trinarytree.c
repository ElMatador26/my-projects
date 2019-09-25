#include <stdio.h>
#include<stdlib.h>
typedef struct node
{
    int data, i;
    struct node *left, *right, *top;
}node;

node *add(node *head, int i)
{
    if(head==NULL)
    {
        head=(node *)malloc(sizeof(node));
        head->top=head->left=head->right=NULL;
        head->data=i;
        head->i=0;
        return head;
    }
    if(head->data > i)
    {
        head->left=add(head->left, i);
        (head->left)->top=head;
        return head;
    }
    else
    {
        head->right=add(head->right, i);
        (head->right)->top=head;
        return head;
    }

}

void see(node *head, int j)
{
    while(head!=NULL)
    {
        head->i=(head->i)+1;
        if(head->i==j)
            printf("%d ", head->data);
       if(head->i == 1)
       {
           if(head->left!=NULL)
                head=head->left;
           else
            continue;
       }
       if(head->i == 2)
       {
           if(head->right!=NULL)
            head=head->right;
           else
            continue;
       }
       if(head->i == 3)
        {
            head->i=0;
            head=head->top;
        }
    }
}
void main(void)
{
    node*head=NULL;
    int i=1;
    while(i!=0)
    {
        printf("Enter the number: ");
        scanf("%d", &i);
        head=add(head, i);
    }
    printf("Preorder\n");
    see(head, 1);
    printf("\nInorder:\n");
    see(head, 2);
    printf("\nPostorder:\n");
    see(head, 3);
}
