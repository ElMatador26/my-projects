#include<stdio.h>
#include<stdlib.h>

typedef struct node
{
    char c;
    int pref;
    struct node *link;
}node;

node *push(node *head, char c, int pref)
{
    node *head2=(node *)malloc(sizeof(node));
    head2->link=head;
    head2->c=c;
    head2->pref=pref;
    return head2;
}
node *pop(node *head)
{
    node *head2=head;
    if(head != NULL)
    {
        head=head->link;
        if(head2->c != '(')
            printf("%c", head2->c);
        free(head2);
    }
    return head;
}
void postfix(char *str)
{
    int i, brk=0;
    node *head=NULL;
    for(i=0; str[i]!='\0'; i++)
    {
        if(str[i]=='(')
        {
            brk++;
            head=push(head, str[i], brk*4);
            continue;
        }
        if(str[i]==')')
        {
            brk--;
            while(head!=NULL && head->c != '(')
                head=pop(head);
            continue;
        }
        if(str[i]== '+' || str[i]=='-')
        {
            while(head!=NULL && head->pref >= (brk*4)+1)
                head=pop(head);
            head=push(head, str[i], (brk*4)+1);
            continue;
        }
        if(str[i]=='*' || str[i]=='/' || str[i]=='%')
        {
            while(head!=NULL && head->pref >= (brk*4)+2)
                head=pop(head);
            head=push(head, str[i], (brk*4)+2);
            continue;
        }
        if(str[i]=='^')
        {
            while(head!=NULL && head->pref >= (brk*4)+3)
                head=pop(head);
            head=push(head, str[i], (brk*4)+3);
            continue;
        }
        printf("%c", str[i]);
    }
    while(head!=NULL)
        head=pop(head);
}
void main()
{
    char str[100];
    printf("Enter the string: ");
    scanf("%s", str);
    postfix(str);
}
