#include<stdio.h>
#include<stdlib.h>
typedef struct node
{
	int wt, i, j;
	struct node *link;
}node;

typedef struct set
{
	node *rear, *front;
	int s;
}set;
void kruskals(node *head, int n)
{
	set *arr=(set *)calloc(n, sizeof(set));
	int s=0;
	node *head2;
	while(head != NULL)
	{
		head2=head;
		if(arr[head->i].front != arr[head->j].front || arr[head->i].s == 0)	
		{
			if(arr[head->j].front != NULL)
			{
				arr[head->j].rear=(arr[head->j].rear)->link=head;
			}
			else
				arr[head->j].front=arr[head->j].rear=head;
			(arr[head->j].s)++;
			(arr[head->i].rear)->link=arr[head->j].front;
			arr[head->j].front=arr[head->i].front;
			arr[head->j].s=arr[head->j].s+arr[head->i].s;
			while(arr[head->i].front != NULL)
			{
				arr[(arr[head->i].front)->j]=arr[(arr[head->i].front)->i]=arr[head->j];
				arr[head->i].front=(arr[head->i].front)->link;
			}
			arr[head->i]=arr[head->j];
			head=head->link;
			head2->link=NULL;
		}
		else
		{
			head=head->link;
			free(head2);
		}
	}
	if(arr[0].s == n-1)
	{
		head2=arr[0].front;
		while(head2 != NULL)
		{
			printf("i=%d j=%d wt=%d\n", head2->i+1, head2->j+1, head2->wt);
			s=s+head2->wt;
			head2=head2->link;
		}
	}
	else
		printf("Multiple spanning forests are present\n");
	}

int main()
{
	node *head=NULL, *head2;
	int i=1, s=0;
	while(i != 0)
	{
		head2=(node *)calloc(1, sizeof(node));
		printf("Enter source vertex: ");
		scanf("%d", &(head2->i));
		printf("Enter destination vertex: ");
		scanf("%d", &(head2->j));
		printf("Enter the weight: ");
		scanf("%d", &(head2->wt));
		head2->link=head;
		head=head2;
		printf("Enter 0 to exit: ");
		scanf("%d", &i);
	}
	kruskals(head, 5);
	return 0;
}
			



