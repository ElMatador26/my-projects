#include<stdio.h>
#include<stdlib.h>

//merge sort with loops

typedef struct node
{
	int high, low, mid, *arr, i;
	struct node *link;
}node;

node *merge(node *head)
{
	node *head2;
	int high2=(head->mid)+1, low2=head->low, *arr2;
	arr2=(int *)calloc((head->high)-(head->low)+1, sizeof(int));
	head->i=0;
	while(low2 <= head->mid && high2 <= head->high)
	{
		if(head->arr[low2] < head->arr[high2])
			arr2[(head->i)++]=head->arr[low2++];
		else
			arr2[(head->i)++]=head->arr[high2++];
	}
	while(low2 <= head->mid)
		arr2[(head->i)++]=head->arr[low2++];
	while(high2 <= head->high)
		arr2[(head->i)++]=head->arr[high2++];
	for(low2 = head->low; low2 <= head->high; low2++)
		head->arr[low2]=arr2[low2-(head->low)];
	free(arr2);
	head2=head;
	head=head->link;
	free(head2);
	return head;
}

void divide(int *arr, int n)
{
	
	node *head=NULL, *head2;
	head=(node *)calloc(1, sizeof(node));
	head->arr=arr;
	head->low=0;
	head->high=n-1;
	head->mid=(n-1)/2;
	
	while(head != NULL)
	{
		if(head->high == head->low)
		{
			head2=head;
			head=head->link;
			free(head2);
			continue;
		}
		(head->i)++;
		if(head->i == 1)
		{
			head2=(node *)calloc(1, sizeof(node));
			head2->link=head;
			head2->low=head->low;
			head2->high=head->mid;
			head2->mid=(head2->low+head2->high)/2;
			head2->arr=arr;
			head=head2;
		}
		if(head->i == 2)
		{
			head2=(node *)calloc(1, sizeof(node));
			head2->link=head;
			head2->low=head->mid+1;
			head2->high=head->high;
			head2->mid=(head2->low+head2->high)/2;
			head2->arr=arr;
			head=head2;
		}
		if(head->i == 3)
			head=merge(head);
	}
}

int main()
{
	int n, i, *arr;
	printf("Enter the number of elements: ");
	scanf("%d", &n);
	arr=(int *)malloc(n*sizeof(int));
	printf("Enter the elements: ");
	for(i=0; i<n; i++)
		scanf("%d", &arr[i]);
	divide(arr, n);
	for(i=0; i<n; i++)
		printf("%d ", arr[i]);
	printf("\n");
	return 0;
}

