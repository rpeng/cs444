package P;

public class A {
    public int a;
    public static int b = 3;
    public A next;

    public A() {

    }

    public A(int i) {
        this.a = i;
    }

    public A(A other, int plus) {
        this.a = other.a + plus;
    }

    public static native int foo(int bar);

    public void f() {
        A.foo('a' + 0);
        A.foo('f' + 0);
        A.foo('\n' + 0);
    }

    public void hi() {
        A.foo(a + '0');
        A.foo('\n' + 0);
    }

    public static int test() {
    /*
        new A(new A(4), 3).hi();
        new B().hi(); */
        int[] j = new int[4];
        j[0] = 1;
        j[1] = 2;
        new A(j.length).hi();
        return 0;
    }
}
