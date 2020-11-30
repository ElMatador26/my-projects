
import java.util.Scanner;
class Test
{public static void main(String args[])
    {
        Scanner ob = new Scanner(System.in);
        String str[] = ob.nextLine().split(" ");
        ob.close();
        for(int i = str.length-2; i>= 0; i--)
            for(int j=0; j< i; j++)
            {
                if(j%2 == 0)
                {
                    if(str[j].toLowerCase().compareTo(str[j+2].toLowerCase()) > 0)
                    {
                        String str2 = str[j].toLowerCase();
                        str[j] = str[j+2].toLowerCase();
                        str[j+2]=str2;

                    }
                }
                else
                {
                    if(Integer.parseInt(str[j]) > Integer.parseInt(str[j+2]))
                    {
                        String str2 = str[j];
                        str[j] = str[j+2];
                        str[j+2]=str2;
                    }
                }
            }
        for(int i=0; i< str.length; i++)
            System.out.print(str[i]+ " ");

    }
}
