package P;

public class B extends A {
    public int c;
    public int d;
    public static int f = 4;

    public B() {
    }

    public void hi() {
        A.foo('b' + 0);
        A.foo('\n' + 0);
    }
}
