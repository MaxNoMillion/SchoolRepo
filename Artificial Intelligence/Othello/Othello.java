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
  boolean[] move_state = new boolean[8];

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
    // Getting coords of desired tile
    while (true){
      updateBufferBoard();
      //checkForPossibleMove();

      int[] moveCoords = new int[2];
      // Checking if move is valid
      while (!isMoveValid(moveCoords)){
        moveCoords = readCoords();
        if (isMoveValid(moveCoords)) 
          break;
        System.out.println("Invalid input or move.");
      }
      calculateBoard(moveCoords);
      updateBoardVisuals();
      changeTurns();
    }
  }
  
  public void calculateBoard(int[] moveCoords){
    /** Places piece down on selected tile. */
    if (whos_turn == black)
      source_board[moveCoords[0]][moveCoords[1]] = black;
    if (whos_turn == white)
      source_board[moveCoords[0]][moveCoords[1]] = white;

    for (int i = 0; i < move_state.length; i++)
      if (move_state[i])
        flipFlankDirection(i, moveCoords);
  }

  public void flipFlankDirection(int dir, int[] moveCoords){
    // Declaring vars
    int[] tempCoords = new int[2];
    tempCoords[0] = moveCoords[0];    // Hard copying moveCoords
    tempCoords[1] = moveCoords[1];
    // Getting current direction Off-set
    int[] dirStep = new int[2];
    dirStep = getDirectionOffSet(dir);

    if (whos_turn == black){
      while (buffer_board[tempCoords[0] + dirStep[0] + 1][tempCoords[1] + dirStep[1] + 1] == white){
        /** Stepping to next flanked piece */
        tempCoords[0] += dirStep[0];
        tempCoords[1] += dirStep[1];
        /** Flipping flanked white pieces to black */
        source_board[tempCoords[0]][tempCoords[1]] = black;
      }
    }
    if (whos_turn == white){
      while (buffer_board[tempCoords[0] + dirStep[0] + 1][tempCoords[1] + dirStep[1] + 1] == black){
        /** Stepping to next flanked piece */
        tempCoords[0] += dirStep[0];
        tempCoords[1] += dirStep[1];
        /** Flipping flanked black pieces to white */
        source_board[tempCoords[0]][tempCoords[1]] = white;
      }
    }
  }

  public boolean checkForPossibleMove(){
    int[] scanCoords = new int[2];
    boolean valid = false;
    for (int i = 0; i < source_board.length; i++){
      for (int j = 0; j < source_board[0].length; j++){
        scanCoords[0] = i;
        scanCoords[1] = j;
        valid = valid || isMoveValid(scanCoords);
      }
    }
    return valid;
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

    if (whos_turn == black)
      System.out.println("        ** Black's Turn **\n");
    if (whos_turn == white)
      System.out.println("        ** White's Turn **\n");

    int[] coords = new int[2];
    Scanner scan = new Scanner(System.in);
    System.out.print("Please enter row coord: ");
    coords[0] = scan.nextInt();
    System.out.print("Please enter column coord: ");
    coords[1] = scan.nextInt();

    return coords;
  }

  public boolean isMoveValid(int[] moveCoords){
    boolean valid = false;
    // Validating move //
    /** Detecting Out-of-Bounds */
    if (moveCoords[0] > 7 || moveCoords[1] > 7)
      return valid;
    /** Checking if tile is already taken */
    if ((source_board[moveCoords[0]][moveCoords[1]] != empty))
      return valid;

    // Checking each direction for flanking and recording flanking direction in move_state
    for (int dir = 0; dir < 8; dir++){
      move_state[dir] = isValidDirection(dir, moveCoords);
    }
    // Anding all directions to determine if move had valid direction
    for (int i = 0; i < 8; i++)
      valid = valid || move_state[i];

    return valid;
  }

  public boolean isValidDirection(int dir, int[] moveCoords){
    // Declaring vars
    int[] tempCoords = new int[2];
    tempCoords[0] = moveCoords[0];    // Hard copying moveCoords
    tempCoords[1] = moveCoords[1];
    // Getting current direction Off-set
    int[] dirStep = new int[2];
    dirStep = getDirectionOffSet(dir);
    
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

  public int[] getDirectionOffSet(int dir){
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
    return dirStep;
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