package P;

public class B extends A {
    public int c;
    public int d = 4;
    public int f;

    public B() {
    }

    public void hi() {
        A.foo('b' + 0);
        A.foo('\n' + 0);
    }
}
