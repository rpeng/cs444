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
        Object a = (Object)new B();
        ((A)a).hi();
        A.foo((int)'W');
        A.foo((int)'\n');
        return 0;
    }
}
