//////////////////////////////////////////////////////////////////////////
// Name: Andrew Steen                                                   //
// SWID: 102-68-080                                                     //
// Date: Nov 14 2022                                                    //
// Assignment #: 3                                                      //
// Program Discription: 2 player and 1 player /w computer Othello game. //
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
  /** Forfeit turn boolean
   *  (If both players forfeited their turn, the game is over.) */
  boolean forfeit_black = false;
  boolean forfeit_white = false;
  /** Declaring moveCoords */
  int[] moveCoords = new int[2];

  ////// OTHELLO CONTRUCTOR //////
  public Othello(){
    // Building main game board
    for (int i = 0; i < board_size; i++)
      for (int j = 0; j < board_size; j++)
        source_board[i][j] = empty;

    // Setting initial board configuration.
    source_board[3][3] = white;
    source_board[3][4] = black;
    source_board[4][3] = black;
    source_board[4][4] = white;
  }

  public void run(){
    // Main Game Loop //
    while (true){
      /** Updates buffer_board before any calculations */
      updateBufferBoard();
      // Move Validity Check //
      /** The first check is to determine if a valid move exsists
       *  This is checked first to reduce total calculations */
      if (isPossibleMove()){
        /** For end-of-game detection 
         *  (resets forfeit boolean for current player) */
        if (whos_turn == black)
          forfeit_black = false;
        else forfeit_white = false;

        /** Checks if inputted move if valid until valid move is inputted */
        while (!isMoveValid(moveCoords)){
          moveCoords = readCoords();      // Updates moveCoords by reading inputted coords
          /** Determines move validity. If move is valid, then while loop is broken */
          if (isMoveValid(moveCoords)) 
            break;
          /** Reprint board */
          updateBoardVisuals();
          System.out.println("**** Invalid input or move ****\n");
        } 
      /** If no possible move, then current player forfeits turn
       *  If both players forfeit turn, then game is over */
      } else{
        System.out.println("\n    No possible move. Forfeit turn.\n");

        /** End game trigger */
        if (forfeit_black && forfeit_white){
          endGame();
          return;
        }

        /** Saves forfeit boolean */
        if (whos_turn == black)
          forfeit_black = true;
        else forfeit_white = true;
      }
      /** Where flanked peices are flipped */
      calculateBoard(moveCoords);
      /** Where the board display is updated */
      updateBoardVisuals();
      /** Where turn toggles */
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

  public boolean isPossibleMove(){
    int[] scanCoords = new int[2];
    boolean valid = false;
    for (int i = 0; i < board_size; i++){
      for (int j = 0; j < board_size; j++){
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
    /** Prints the current turn */
    if (whos_turn == black)
      System.out.println("        ** Black's Turn **\n");
    if (whos_turn == white)
      System.out.println("        ** White's Turn **\n");
  }

  public int[] readCoords(){

    /** Simple Coord Input with input validation */
    int[] coords = new int[2];
    Scanner scan = new Scanner(System.in);
    try {
      System.out.print("Please enter row coord: ");
      coords[0] = scan.nextInt();
      System.out.print("Please enter column coord: ");
      coords[1] = scan.nextInt();
    } catch(Exception e){}
    
    return coords;
  }

  public boolean isMoveValid(int[] moveCoords){
    boolean valid = false;
    // Validating move //
    /** Detecting Out-of-Bounds */
    if (moveCoords[0] > board_size - 1 || moveCoords[1] > board_size - 1)
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
    for (int i = 0; i < board_size; i++)
      for (int j = 0; j < board_size; j++)
        buffer_board[i + 1][j + 1] = source_board[i][j];
  }

  public void endGame(){
    System.out.println("Game has ended!!!");

    if (getScore('w') > getScore('b'))
      System.out.println("\n\n\n\nWhite WON!!!\n\n\n\n");
    else if (getScore('b') > getScore('w'))
      System.out.println("\n\n\n\nBlack WON!!!\n\n\n\n");
    else 
      System.out.println("\n\n\n\n It's a TIE!!!\n\n\n\n");
  }
  
  public int getScore(char player){
    int white_counter = 0;
    int black_counter = 0;
    for (int i = 0; i < board_size; i++){
      for (int j = 0; j < board_size; j++){
        if (source_board[i][j] == white)
          white_counter++;
        if (source_board[i][j] == black)
          black_counter++;
      }
    }
    if (player == 'w')
      return white_counter;
    else
      return black_counter;
  }

  public void printBoard(){
    System.out.println("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n");
    System.out.println("    ▓▓▓ ▓▓▓ ▓ ▓ ▓▓▓ ▓   ▓   ▓▓▓");
    System.out.println("    ▓ ▓  ▓  ▓▓▓ ▓▓  ▓   ▓   ▓ ▓");
    System.out.println("    ▓▓▓  ▓  ▓ ▓ ▓▓▓ ▓▓▓ ▓▓▓ ▓▓▓");
    System.out.println();
    System.out.print("      White: " + getScore('w'));
    System.out.println("\t    Black: " + getScore('b'));
    //System.out.println();

    /** Prints colomn coord */
    System.out.print("      ");
    for (int i = 0; i < board_size; i++)
      System.out.print(i + "  ");
    System.out.println();
    /** Prints top of board */
    System.out.print("      ");
    for (int i = 0; i < board_size; i++)
      System.out.print("__" + " ");
    System.out.println();

    for (int i = 0; i < board_size; i++){
      System.out.print("  " + i + "  ");
      for (int j = 0; j < board_size; j++){
        System.out.print("|" + source_board[i][j] + source_board[i][j]);
      }
      System.out.print("|\n");
    }
  }

  /////// MAIN ///////
  public static void main(String[] args){
    Othello othello = new Othello();
    othello.printBoard();
    System.out.println("        ** Black's Turn **\n");
    othello.run();
  }
}