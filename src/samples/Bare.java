package org.example;

import org.one.One;
import org.two.Two;
import org.three.*;

public static class Bare extends org.one.One implements Two {
  public int anInt; 
  public boolean aBool = false; 
  public int someAddition = 1 + 3;
  static protected String[] aString;

  public void doNothing(){
  }

  protected Bare(int i, boolean j, Jane j) {
  }
}
