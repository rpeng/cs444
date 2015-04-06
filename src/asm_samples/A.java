package P;

public class A {
    public int a = 1;
    public int b = 2;
    public int c = 3;
    public int d = 4;

    // public static int i = A.sub(3,1);
    // public static int j = A.i;

    public A() {
    }

    public static native int foo(int bar);

    /*
    public static int add(int a, int b) {
        return a + b;
    }

    public static int sub(int a, int b) {
        return a - b;
    }
    */

    public static int test() {
        A a = new A();
        return 0;
    }
}
