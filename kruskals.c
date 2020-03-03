#include<stdio.h>
#include<stdlib.h>
//final
typedef struct node
{
	int i, j, wt;
	struct node *link;
}node;
typedef struct set
{
	node *front, *rear;
	int s;
}set;
void kruskals(node *head, int n)
{
	set *arr;
	node *head2=NULL;
	int s;
	arr=(set *)calloc(n, sizeof(set));
	while(head != NULL)
	{
		head2=head;
		head=head->link;
		s=head2->i;
		if(arr[head2->i].s == 0 || arr[head2->i].front != arr[head2->j].front)
		{	
			if(arr[s].front == NULL)
				arr[s].front=arr[s].rear=head2;
			else
				arr[s].rear=(arr[s].rear)->link=head2;
			arr[s].rear->link=arr[head2->j].front;
			if(arr[head2->j].rear != NULL)
				arr[s].rear=arr[head2->j].rear;
			arr[s].s=arr[s].s+1+arr[head2->j].s;
			head2=arr[s].front;
			arr[s].rear->link=NULL;
			while(head2 != NULL)
			{
				arr[head2->i]=arr[head2->j]=arr[s];
				head2=head2->link;
			}
		}
		else
			free(head2);
	}
	if(arr[0].s == n-1)
	{
		printf("Spanning tree detected: \n");
		s=0;
		head2=arr[0].front;
		while(head2 != NULL)
		{
			printf("i=%d, wt=%d, j=%d\n", head2->i, head2->wt, head2->j);
			s=s+(head2->wt);
			head2=head2->link;
		}
		printf("The total weight is: %d\n", s);
	}
	else
		printf("Spanning forests detected\n");
	printf("\n");

}
node *insert(node *head, node *head2)
{
	node *head3;
	if(head==NULL || head->wt > head2->wt)
	{
		head2->link=head;
		return head2;
	}
	head3=head;
	while(head3 != NULL)
	{
		if(head3->link == NULL || (head3->link)->wt > head2->wt)
		{
			head2->link=head3->link;
			head3->link=head2;
			return head;
		}
		head3=head3->link;
	}
}

int main()
{
	node *head=NULL, *head2;
	int i=1, s=-1;
	while(i != 0)
	{
		head2=(node *)malloc(sizeof(node));
		printf("Enter the initial vertex: ");
		scanf("%d", &(head2->i));
		printf("Enter the end vertex: ");
		scanf("%d", &(head2->j));
		printf("Enter the weight: ");
		scanf("%d", &(head2->wt));
		printf("Enter 0 to stop: ");
		scanf("%d", &i);
		head=insert(head, head2);
		s=(s >= head2->i)?s:head2->i;
		s=(s >= head2->j)?s:head2->j;
	}
	kruskals(head, s+1);
	return 0;
}			
