//////////////////////////////////////////////////////////////////////////
// Name: Andrew Steen                                                   //
// SWID: 102-68-080                                                     //
// Date: Nov 14 2022                                                    //
// Assignment #: 3                                                      //
// Program Discription: 2 player and 1 player Othello game.             //
//////////////////////////////////////////////////////////////////////////

// Imports
import java.util.Scanner;

// Main class
public class Othello{
  // Declaring Constants
  /** Board size constant */
  private static final int board_size = 8;
  /** Source board tile states for game logic. */
  private static final char white = '█';
  private static final char black = '░';
  private static final char empty = '_';
  

  // Declaring class variables.
  /** Creating a 2D array for game board. */
  char[][] source_board = new char[board_size][board_size];

  ////// OTHELLO CONTRUCTOR //////
  public Othello(){
    // Building main game board
    for (int i = 0; i < 8; i++)
      for (int j = 0; j < 8; j++)
        source_board[i][j] = empty;

    // Setting initial board configuration.
    source_board[3][3] = white;
    source_board[3][4] = black;
    source_board[4][3] = black;
    source_board[4][4] = white;
  }

  public void run(){
    System.out.print("Please type coords [#,#]: ");
    Scanner scan = new Scanner(System.in);
    String player_input = scan.nextLine();

    

  }

  public void updateBoardVisuals(){
    assert true;
  }

  public boolean isValidMove(){
    // Validity var that will be updated throughout fn
    boolean valid = false;





    return true;
  }


  // Quick n' Dirty print function.
  public void printBoard(){
    System.out.println("\t __ __ __ __ __ __ __ __ ");
    for (int i = 0; i < 8; i++){
      System.out.print("\t");
      for (int j = 0; j < 8; j++){
        System.out.print("|" + source_board[i][j] + source_board[i][j]);
      }
      System.out.print("|\n");
    }
  }

  /////// MAIN ///////
  public static void main(String[] args){
    Othello othello = new Othello();
    othello.printBoard();
  }
}