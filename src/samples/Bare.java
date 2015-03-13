package org.example;

public class Bare extends Bare2 {
    public static int cool = 4; // nok
    public static int here = cool; // ok
    public static int test_bar = bar; // should not be ok

    public void doSomething() {
        Bare2 b = new Bare2();
        b = here;
        here = false;

        /*
        org.doSomething.Bare.cool();
        org.doSomething.Bare.cool = 4;
        cool = 4;
        cool();*/
    }
}
