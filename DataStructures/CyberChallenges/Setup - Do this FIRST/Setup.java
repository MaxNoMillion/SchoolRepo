public class Setup {
  public static final int BLACK  = 30;
  public static final int RED    = 31;
  public static final int GREEN  = 32;
  public static final int YELLOW = 33;
  public static final int BLUE   = 34;
  public static final int MAGENTA= 35;
  public static final int CYAN   = 36;
  public static final int LTGRAY = 37;

  public static void main(String[] args) {
    String hello = c(CYAN, "Hello ");
    String world = c(MAGENTA, "World");
    String bang = c(GREEN, "!!!");
    System.out.print(hello + world + bang);
  }
  
  public static String c(int num, String msg) {
    return "\033[" + num + "m" + msg + "\033[39m";
  }
}
