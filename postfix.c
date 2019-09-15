#include<stdio.h>
#include<stdlib.h>

typedef struct node
{
    int data, j;
    struct node *left, *right;
}node;

node *merge(node *head1, node *head2)
{
    if(head2->j <= head1->j && head1->j!=0)
    {
        head2->left=head1;
        return head2;
    }
    if(head1->j==0)
        return head2;
    head1->right=merge(head1->right, head2);
    return head1;
}
node *postfix(char *str)
{
    node *head1, *head2, *head3;
    int i, pref=0, brk=0;
    head1=head2=NULL;
    for(i=0; str[i]!='\0'; i++)
    {
        if(str[i]=='(')
        {
            brk++;
            continue;
        }
        if(str[i]==')')
        {
            brk--;
            continue;
        }
        if(str[i]=='+' || str[i]=='-')
            pref=(brk*3)+1;
        if(str[i]=='/' || str[i]=='*')
            pref=(brk*3)+2;
        if(str[i]=='^')
            pref=(brk*3)+3;
        if(pref!=0)
        {

                head3=(node *)malloc(sizeof(node));
                head3->data=str[i];
                head3->j=pref;
                head3->left=(node *)malloc(sizeof(node));
                head3->right=(node *)malloc(sizeof(node));
                head3->left->data=str[i-1];
                head3->left->j=0;
                (head3->left)->left=(head3->left)->right=NULL;
                head3->right->data=str[i+1];
                head3->right->j=0;
                (head3->right)->left=(head3->right)->right=NULL;
                if(head1==NULL)
                    head1=head3;
                else
                {
                    head2=head3;
                    head1=merge(head1, head2);
                }
                pref=0;
        }
    }
    if(brk!=0)
    {
        printf("Syntax error.");
        return NULL;
    }
    return head1;
}

void see(node *head)
{
    if(head!=NULL)
    {
        see(head->left);
        see(head->right);
        printf("%c", head->data);
    }
}

void main()
{
    char str[100];
    node *head;
    printf("Enter the string: ");
    scanf("%s", str);
    head=postfix(str);
    see(head);

}
