#include<stdio.h>
#include<stdlib.h>

typedef struct node
{
    int data,i;
    struct node *left, *right, *top;
}node;
node *makenode(int j)
{
    node *head=NULL;
    while(head==NULL)
        head=(node *)malloc(sizeof(node));
    head->left=head->right=NULL;
    head->top=NULL;
    head->data=j;
    head->i=0;
    return head;
}
node *add(node *head, node *head2)
{
    node *head3=head;
    if(head==NULL)
        return head2;

    while(head!=NULL)
    {
        if(head2==NULL)
        {
            head->i=(head->i)+1;
            head->i=(head->i)%2;
            if(head->i == 0)
                {
                    head=head->top;
                    continue;
                }
            break;
        }
        if(head->data > head2->data)
        {
            head->data=(head2->data)+(head->data);
            head2->data=(head->data)-(head2->data);
            head->data=(head->data)-(head2->data);
        }
        if(head->i == 0)
        {
            if(head->left!=NULL)
                head=head->left;
            else
                {
                    head->left=head2;
                    head2->top=head;
                    head2=NULL;
                }
        }
        else
        {
            if(head->right!=NULL)
                head=head->right;
            else
            {
                head->right=head2;
                head2->top=head;
                head2=NULL;
            }
        }

    }
    return head3;
}
void see(node *head, int i)
{
    if(head!=NULL)
    {printf("data=%d, i=%d number=%d\n", head->data, head->i, i);
    see(head->left, i*2);
    see(head->right, (i*2)+1);
    }
}
void merge(int *arr, int low, int mid, int high)
{
    int i=low, j=mid+1, *arr2, c=0;
    arr2=(int *)calloc((high-low+1), sizeof(int));
    while(i <= mid && j <=high)
    {
        if(arr[i] < arr[j])
        {
            arr2[c]=arr[i];
            i++;
        }
        else
        {
            arr2[c]=arr[j];
            j++;
        }
        c++;
    }
        while(i <= mid)
        {
            arr2[c]=arr[i];
            c++;
            i++;
        }

        while(j <= high)
        {
            arr2[c]=arr[j];
            c++;
            j++;
        }

    for(i=low; i< c+low; i++)
            arr[i]=arr2[i-low];
    free(arr2);
}
int sort(node *head, int *arr, int n)
{
    int i, j;
    if(head!=NULL)
    {
        arr[n]=head->data;
        i=sort(head->left, arr, n+1);
        j=sort(head->right, arr, i+1);
        merge(arr, n+1, i, j);
        return j;
    }
    return n-1;
}
void main()
{
    node *head=NULL;
    int i=1, arr[100], c=0;
    while(i!=0)
    {
        printf("Enter the number: ");
        scanf("%d", &i);
        head=add(head, makenode(i));
    }
    see(head, 1);
    i=sort(head, arr, 0);
    for(c=0; c<=i; c++)
        printf("%d ", arr[c]);
}
