#include<stdio.h>
#include<stdlib.h>
//updated
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
	arr=(set *)calloc(n, sizeof(set));
	printf("s=%d\n", arr[head->i].s);
	while(head!=NULL)
	{
		if(arr[head->i].s == 0 )
			printf("Hi");
		if(arr[head->i].s == 0 )//|| arr[head->i].front != arr[head->j].front)
		{	
			printf("Hello");
			if(arr[head->i].front == NULL)
				arr[head->i].front=arr[head->i].rear=head;
			else
				arr[head->i].rear=(arr[head->i].rear)->link=head;
			arr[head->i].rear->link=arr[head->j].front;
			arr[head->i].rear=arr[head->j].rear;
			arr[head->i].s=1+arr[head->i].s+arr[head->j].s;
			head2=arr[head->i].front;
			while(1)
			{
				arr[head2->i]=arr[head2->j]=arr[head->i];
				if(head2 == arr[head->i].rear)
					break;
				head2=head2->link;
			}
		}
		head=head->link;
	}
	if(arr[0].s == n)
		printf("Spanning tree is formed");
	else
		printf("Spanning forests detected");
}
int main()
{
	node *head=NULL, *head2;
	int i=1, s=-1;
	while(i != 0)
	{
		head2=(node *)malloc(sizeof(node));
		head2->link=head;
		head=head2;
		printf("Enter the initial vertex: ");
		scanf("%d", &(head->i));
		printf("Enter the end vertex: ");
		scanf("%d", &(head->j));
		printf("Enter the weight: ");
		scanf("%d", &(head->wt));
		printf("Enter 0 to stop: ");
		scanf("%d", &i);
		s=(s >= head->i)?s:head->i;
		s=(s >= head->j)?s:head->j;
	}
	kruskals(head, s+1);
	return 0;
}			
