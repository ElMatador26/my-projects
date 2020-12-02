
import java.util.Scanner;

class alpha
{
    String[] sorting(String str[])
    {
        for (int i = str.length - 2; i >= 0; i--)
            for (int j = 0; j < i; j++)
            {
                if (j % 2 == 0)
                {
                    if (str[j].compareTo(str[j + 2]) > 0)
                    {
                        String str2 = str[j];
                        str[j] = str[j + 2];
                        str[j + 2] = str2;
                    }
                }
                 else 
                {
                    if (Integer.parseInt(str[j]) > Integer.parseInt(str[j + 2]))
                    {
                        String str2 = str[j];
                        str[j] = str[j + 2];
                        str[j + 2] = str2;
                    }
                }
            }
        return str;

    }
    void show(String str[])
    {
        for (int i = 0; i < str.length; i++)
            System.out.print(str[i] + " ");
    }
}
class Test
{public static void main(String args[])
    {
        Scanner ob = new Scanner(System.in);
        String str[] = ob.nextLine().toLowerCase().split(" ");
        ob.close();
        alpha obj = new alpha();
        str=obj.sorting(str);
        obj.show(str);

    }
}
