
import java.util.Scanner;
class Mult{
    int[][] ans(int[][] mat1, int[][] mat2)
    {
        int row1=mat1.length, col1=mat2.length, col2=mat2[0].length;
        int mat[][] = new int[row1][col2];
        for(int i=0; i< row1; i++)
            for(int j=0; j < col2; j++)
                for(int k=0; k < col1; k++)
                    mat[i][j] = mat[i][j]+mat1[i][k]*mat2[k][j];
        return mat;
    }
    int[][] takein(int x, int y, Scanner ob)
    {
        int mat1[][] = new int[x][y];
        for (int i = 0; i < x; i++)
            for (int j = 0; j < y; j++) 
            {
                System.out.println("Enter the value of index " + i + " " + j);
                mat1[i][j] = ob.nextInt();
            }
        return mat1;
    }
    void show(int mat1[][])
    {
        for (int i = 0; i < mat1.length; i++) {
            for (int j = 0; j < mat1[0].length; j++)
                System.out.print(mat1[i][j] + " ");
            System.out.println(" ");
        }
    }
}
class Test{
    public static void main(String args[])
    {
        System.out.println("Enter the values of the 3 dimensions");
        Scanner ob = new Scanner(System.in);
        String str[] = ob.nextLine().split(" ");
        
        Mult obj = new Mult();
        System.out.println("Enter the values of first matrix");
        int mat1[][] = obj.takein(Integer.parseInt(str[0]), Integer.parseInt(str[1]), ob);
        System.out.println("Enter the values of Second matrix");
        int mat2[][] = obj.takein(Integer.parseInt(str[1]), Integer.parseInt(str[2]), ob);
        ob.close();
        System.out.println("First matrix:");
        obj.show(mat1);
        System.out.println("Second matrix");
        obj.show(mat2);
        int mat[][] = obj.ans(mat1, mat2);
        System.out.println("Product: ");
        obj.show(mat);   
    }
}
