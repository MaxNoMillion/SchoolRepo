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
  /** Boundary buffer, for when checking borders */
  char[][] buffer_board = new char[board_size + 2][board_size + 2];
  /** String to keep track of who is playing. */
  char whos_turn = black;
  /** Boolean[] where the 0th index is the validity of move and 
   *  1-8 are the directions that need flipping.*/
  boolean[] move_state = new boolean[9];

  ////// OTHELLO CONTRUCTOR //////
  public Othello(){
    // Building main game board
    for (int i = 0; i < 8; i++)
      for (int j = 0; j < 8; j++)
        source_board[i][j] = empty;

    // Setting initial board configuration.
    // source_board[3][3] = white;
    // source_board[3][4] = black;
    // source_board[4][3] = black;
    // source_board[4][4] = white;
    source_board[3][3] = white;
    source_board[3][4] = black;
    source_board[4][3] = black;
    source_board[4][4] = white;
    source_board[5][5] = black;
    source_board[5][3] = black;
    //source_board[2][2] = black;
  }

  public void run(){
    // Getting coords of desired tile
    while (true){
      updateBufferBoard();
      int[] moveCoords = new int[2];
      // Checking if move is valid
      move_state[0] = false;
      while (move_state[0] == false){
        moveCoords = readCoords();
        isMoveValid(moveCoords);
        if (move_state[0]) break;
        System.out.println("Invalid input or move.");
      }
      calculateBoard();

      if (whos_turn == black){
        source_board[moveCoords[0]][moveCoords[1]] = black;
      }
      if (whos_turn == white){
        source_board[moveCoords[0]][moveCoords[1]] = white;
      }
      updateBoardVisuals();
      changeTurns();
    }
  }
  
  public void calculateBoard(){
    assert true;
  }

  public void changeTurns(){
    if (whos_turn == black)
      whos_turn = white;
    else if (whos_turn == white)
      whos_turn = black;
  }

  public void updateBoardVisuals(){
    printBoard();
  }

  public int[] readCoords(){
    int[] coords = new int[2];
    Scanner scan = new Scanner(System.in);
    System.out.print("Please enter row coord: ");
    coords[0] = scan.nextInt();
    System.out.print("Please enter column coord: ");
    coords[1] = scan.nextInt();

    return coords;
  }

  public void isMoveValid(int[] moveCoords){
    // Validating move //
    /** Detecting Out-of-Bounds */
    if (moveCoords[0] > 7 || moveCoords[1] > 7){
      move_state[0] = false;
      return;
    }
    /** Checking if tile is already taken */
    if ((source_board[moveCoords[0]][moveCoords[1]] != empty)){
      move_state[0] = false;
      return;
    }
    // Checking each direction for flanking and recording flanking direction in move_state
    for (int dir = 0; dir < 8; dir++){
      move_state[dir + 1] = isValidDirection(dir, moveCoords);
    }
    // Anding all directions to determine if move had valid direction
    for (int i = 1; i < 9; i++)
      move_state[0] = move_state[0] || move_state[i];
  }

  public boolean isValidDirection(int dir, int[] moveCoords){
    // Declaring vars
    int[] tempCoords = new int[2];
    tempCoords[0] = moveCoords[0];    // Hard copying moveCoords
    tempCoords[1] = moveCoords[1];
    int[] dirStep = new int[2];

    /** This is used to adjust the position of tempCoords in next step */
    if (dir == 0){        // Right
      dirStep[0] =  0;
      dirStep[1] =  1;
    }
    else if (dir == 1){   // Up-Right
      dirStep[0] = -1;
      dirStep[1] =  1;
    }
    else if (dir == 2){   // UP
      dirStep[0] = -1;
      dirStep[1] =  0;
    }
    else if (dir == 3){   // Up-Left
      dirStep[0] = -1;
      dirStep[1] = -1;
    }
    else if (dir == 4){   // Left
      dirStep[0] =  0;
      dirStep[1] = -1;
    }
    else if (dir == 5){   // Down-Left
      dirStep[0] =  1;
      dirStep[1] = -1;
    }
    else if (dir == 6){   // Down
      dirStep[0] =  1;
      dirStep[1] =  0;
    }
    else if (dir == 7){   // Down-Right
      dirStep[0] =  1;
      dirStep[1] =  1;
    }
    int counter = 0;
    // Determining is direction is valid for current direction if black's turn //
    if (whos_turn == black){
      while (buffer_board[tempCoords[0] + dirStep[0] + 1][tempCoords[1] + dirStep[1] + 1] == white){        // Steps through each tile in current direction         
        tempCoords[0] += dirStep[0];     // Steps tempCoord                                                           // as long as white
        tempCoords[1] += dirStep[1];       // Unique to each direction
        counter++;
      }
      if (buffer_board[tempCoords[0] + dirStep[0] + 1][tempCoords[1] + dirStep[1] + 1] == black && counter > 0){            // If black then flanked!
        return true;
      }
    }

    // Determining is direction is valid for current direction if white's turn //
    if (whos_turn == white){
      while (buffer_board[tempCoords[0] + dirStep[0] + 1][tempCoords[1] + dirStep[1] + 1] == black){        // Steps through each tile in current direction         
        tempCoords[0] += dirStep[0];     // Steps tempCoord                                                           // as long as black
        tempCoords[1] += dirStep[1];       // Unique to each direction
        counter++;
      }
      if (buffer_board[tempCoords[0] + dirStep[0] + 1][tempCoords[1] + dirStep[1] + 1] == white && counter > 0)            // If white then flanked!
        return true;
    }

    /** Returns false if there is no piece in current direction 
     *  or if not successful flank */
    return false;
  }

  public void updateBufferBoard(){
    for (int i = 0; i < 8; i++)
      for (int j = 0; j < 8; j++)
        buffer_board[i + 1][j + 1] = source_board[i][j];
  }

  // Quick n' Dirty print function.
  public void printBoard(){
    System.out.println("      0  1  2  3  4  5  6  7  ");
    System.out.println("      __ __ __ __ __ __ __ __ ");
    for (int i = 0; i < 8; i++){
      System.out.print("  " + i + "  ");
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
    othello.run();
  }
}