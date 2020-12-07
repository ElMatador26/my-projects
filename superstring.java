import java.util.*;

class Sup
{
        int count(String str, char ch)
        {
                int c=0;
                for(int i=0; i<str.length(); i++)
                        if(str.charAt(i) == ch)
                                c++;
                return c;
        }
        short ans(String str)
        {
                int i= (int) 'a'-1;
                for(int j=0; j< str.length(); j++)
                {
                        int c = count(str, str.charAt(j));
                        int d = (int) str.charAt(j) - i;
                        if(c != d)
                                return 0;
                }
                return 1;
        }
}
class Test
{
        public static void main(String args[])
        {
                Scanner ob = new Scanner(System.in);
                String str = ob.nextLine();
                ob.close();
                Sup obj = new Sup();
                if(obj.ans(str) == 0)
                        System.out.print("No");
                else
                        System.out.print("Yes");
                

        }
}
