import java.util.Scanner;

public class CShape {
    public double GetArea(double x,double y){
        double s;
        s=x*y;
        System.out.println(s);
        return 0;
    }

}


public class CRectangle extends CShape{
    public static void main(String arg[]){
        CRectangle i=new CRectangle();
        System.out.println("请输入长和宽");
        Scanner sc=new Scanner(System.in);
        double a=sc.nextDouble();
        double b=sc.nextDouble();
        i.GetArea(a, b);
    }

}

public class Teaa extends CShape{
    public double GetArea(double x){
        double s;
        s=3.14*x*x;
        System.out.println(s);
        return 0;
    }
    public static void main(String arg[]){
        System.out.println("请输入半径");
        Scanner cs=new Scanner(System.in);
        double r=cs.nextDouble();
        Teaa b=new Teaa();
        b.GetArea(r);
    }

}