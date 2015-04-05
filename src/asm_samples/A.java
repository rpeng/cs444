package P;

public class A {
    public int a;
    public int b;
    public static int i = A.foo(2);

    public A() {
    }

    public static int foo(int bar) {
        return bar;
    }

    public static int test() {
        return 0;
    }
}
