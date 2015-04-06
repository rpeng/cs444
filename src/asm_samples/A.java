package P;

public class A {
    public int a;
    public static int b = 3;
    public A next;

    public A() {

    }

    public A(int i) {
        a = i;
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
        A b = new B();
        b.hi();
        b.f();

        return 0;
    }
}
