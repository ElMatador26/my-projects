import java.util.*;
class Prime
{
        int check(int n)
        {
                for(int i=2; i<= n/2; i++)
                        if(n%i == 0)
                                return 0;
                return 1;
        }
        int ans(int n)
        {
                int s=0, c=0;
                for(int i = 2; s+i <= n; i++)
                {
                        if(check(i) == 1)
                        {
                                s=s+i;
                                
                                if(check(s) == 1 && s != 2)
                                        c++;
                        }
                }
                return c;
        }
}
class Test
{
        public static void main(String args[])
        {
                Scanner ob = new Scanner(System.in);
                int i = ob.nextInt();
                ob.close();
                Prime obj = new Prime();
                System.out.print("The number of primes are: "+ obj.ans(i));


       
        }


}
