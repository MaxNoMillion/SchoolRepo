//////////////////////////////////////////////////////////////////////////
// Name: Andrew Steen                                                   //
// SWID: 102-68-080                                                     //
// Date: Nov 14 2022                                                    //
// Assignment #: 3                                                      //
// Program Discription: 2 player and 1 player /w computer Othello game. //
//////////////////////////////////////////////////////////////////////////

// Imports
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

// Main class
public class Othello {
  // Declaring Constants
  /** Board size constant */
  private static final int board_size = 8;
  /** Source board tile states for game logic. */
  private static final char white = '█';
  private static final char black = '░';
  private static final char empty = '_';

  // Declaring class variables.
  /** Creating a 2D array for game board. */
  char[][] source_board = new char[board_size + 2][board_size + 2];

   /** What game mode */
   boolean isComputerPlayer = false;
   /** Players' color (used when playing computer) */
   char comColor = white;
   char playerColor = white;


  ////// OTHELLO CONTRUCTOR //////
  public Othello(){
    // Building main game board
    for (int i = 0; i < board_size + 2; i++)
      for (int j = 0; j < board_size + 2; j++)
        source_board[i][j] = empty;

    // Setting initial board configuration.
    source_board[3 + 1][3 + 1] = white;
    source_board[3 + 1][4 + 1] = black;
    source_board[4 + 1][3 + 1] = black;
    source_board[4 + 1][4 + 1] = white;
  }


  public void run(){
    char whos_turn = black;
    boolean forfeit_black = false;
    boolean forfeit_white = false;

    // Main Game Loop //
    while (true){
      int[] moveCoords = new int[2];
      // Move Validity Check //
      /** The first check is to determine if a valid move exsists
      *  This is checked first to reduce total calculations */
      //System.out.println(getPossibleMove(source_board, whos_turn).size());
      if (getPossibleMove(source_board, whos_turn).size() > 0){
        /** For end-of-game detection 
        *  (resets forfeit boolean for current player) */
        if (whos_turn == black)
          forfeit_black = false;
        else forfeit_white = false;

        /** Is computer or player */
        if (isComputerPlayer && comColor == whos_turn){
          moveCoords = computerMove(whos_turn);
        } else {
          moveCoords = playerCoords(whos_turn);
        }

      } else {
        /** Else current player forfeits turn */
        System.out.println("\n    No possible move. Forfeit turn.\n");
        /** End game trigger */
        if (isGameOver(forfeit_black, forfeit_white)){
          endGame();
          return;
        }
        /** Saves forfeit boolean */
        if (whos_turn == black)
        forfeit_black = true;
        else forfeit_white = true;
      }

      /** Where flanked peices are flipped */
      source_board = calculateBoard(source_board, moveCoords, whos_turn);
      /** Where turn toggles */
      if (whos_turn == black)
        whos_turn = white;
      else if (whos_turn == white)
        whos_turn = black;
      /** Where the board display is updated */
      update(source_board, whos_turn);
      
    }
  }

  public int[] computerMove(char whos_turn){
    int[] temp = new int[2];
    return temp;
  }

  public char[][] calculateBoard(char[][] board, int[] moveCoords, char whos_turn){
    /** Places piece down on selected tile. */
    if (whos_turn == black)
      board[moveCoords[0] + 1][moveCoords[1] + 1] = black;
    else
      board[moveCoords[0] + 1][moveCoords[1] + 1] = white;

    boolean[] flank_dir = getFlankDirections(board, moveCoords, whos_turn);
    char[][] updated_board = flipFlankDirection(board, flank_dir, moveCoords, whos_turn);

    return updated_board;
  }

  public char[][] flipFlankDirection(char[][] board, boolean[] flank_dir, int[] moveCoords, char whos_turn){
    char[][] updated_board = copyBoard(board);
    for (int dir = 0; dir < flank_dir.length; dir++){
      int[] dirStep = new int[2];
      dirStep = getDirectionOffSet(dir);

      if (whos_turn == black){
        while (board[moveCoords[0] + dirStep[0] + 1][moveCoords[1] + dirStep[1] + 1] == white){
          /** Stepping to next flanked piece */
          moveCoords[0] += dirStep[0];
          moveCoords[1] += dirStep[1];
          /** Flipping flanked white pieces to black */
          updated_board[moveCoords[0] + 1][moveCoords[1] + 1] = black;
        }
      }
      if (whos_turn == white){
        while (board[moveCoords[0] + dirStep[0] + 1][moveCoords[1] + dirStep[1] + 1] == black){
          /** Stepping to next flanked piece */
          moveCoords[0] += dirStep[0];
          moveCoords[1] += dirStep[1];
          /** Flipping flanked black pieces to white */
          updated_board[moveCoords[0] + 1][moveCoords[1] + 1] = white;
        }
      }
    }
    return updated_board;
  }

  public char[][] copyBoard(char[][] ori){
    char[][] copy = new char[board_size + 2][board_size + 2];
     /** Makes hard copies of same size boards */
     for (int i = 1; i < board_size + 1; i++)
       for (int j = 1; j < board_size + 1; j++)
         copy[i][j] = ori[i][j];
     return copy;
   }

  public int[] playerCoords(char whos_turn){
    int[] moveCoords = new int[2];
    /** Checks if inputted move if valid until valid move is inputted */
    while (!isMoveValid(source_board, moveCoords, whos_turn)){
      moveCoords = readCoords();      // Updates moveCoords by reading inputted coords
      /** Determines move validity. If move is valid, then while loop is broken */
      if (isMoveValid(source_board, moveCoords, whos_turn)) 
        return moveCoords;
      /** Reprint board */
      update(source_board, whos_turn);
      System.out.println("**** Invalid input or move ****\n");
    } 
    return moveCoords;
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
    scan.close();
    return coords;
  }

  public List<int[]> getPossibleMove(char[][] board, char whos_turn){
    /** Creating array list of possible move coords */
    List<int[]> possMoves = new ArrayList<int[]>();
    for (int i = 1; i < board_size + 1; i++){
      for (int j = 1; j < board_size + 1; j++){
        int[] coords = {i, j};
        /** Finding valid moves */
        //System.out.println(isMoveValid(board, coords, whos_turn));
        if (isMoveValid(board, coords, whos_turn))
          /** Adding moves to array list */
          possMoves.add(coords);
      }
    }
    return possMoves;
  }

  public boolean isMoveValid(char[][] board, int[] moveCoords, char whos_turn){
    boolean valid = false;
    // Validating move //
    /** Detecting Out-of-Bounds */
    if (moveCoords[0] > board_size - 1 || moveCoords[1] > board_size - 1)
      return valid;
    /** Checking if tile is already taken */
    if ((source_board[moveCoords[0] + 1][moveCoords[1] + 1] != empty))
      return valid;

    // Checking each direction for flanking and recording flanking direction in move_state
    boolean[] flank_dir = getFlankDirections(board, moveCoords, whos_turn);

    // Anding all directions to determine if move had valid direction
    for (int i = 0; i < 8; i++){
      //System.out.print(flank_dir[i]);
      valid = valid || flank_dir[i];
    }
    return valid;
  }

  public boolean[] getFlankDirections(char[][] board, int[] moveCoords, char whos_turn){
    boolean[] flank_dir = new boolean[8];

    for (int dir = 0; dir < 8; dir++){
      // Getting current direction Off-set
      int[] dirStep = getDirectionOffSet(dir);

      int counter = 0;
      // Determining is direction is valid for current direction if black's turn //
      if (whos_turn == black){
        System.out.println(moveCoords[0] + " " + moveCoords[1]);
        while (board[moveCoords[0] + dirStep[0] + 1][moveCoords[1] + dirStep[1] + 1] == white){        // Steps through each tile in current direction         
          moveCoords[0] += dirStep[0];     // Steps tempCoord                                                           // as long as white
          moveCoords[1] += dirStep[1];       // Unique to each direction
        }
        if (board[moveCoords[0] + dirStep[0] + 1][moveCoords[1] + dirStep[1] + 1] == black && counter > 0){           // If black then flanked!
          System.out.println("frof");
          flank_dir[dir] = true;}
        else
          flank_dir[dir] = false;
      }
  
      // Determining is direction is valid for current direction if white's turn //
      if (whos_turn == white){
        while (board[moveCoords[0] + dirStep[0] + 1][moveCoords[1] + dirStep[1] + 1] == black){        // Steps through each tile in current direction         
          moveCoords[0] += dirStep[0];     // Steps tempCoord                                                           // as long as black
          moveCoords[1] += dirStep[1];       // Unique to each direction
          counter++;
        }
        if (board[moveCoords[0] + dirStep[0] + 1][moveCoords[1] + dirStep[1] + 1] == white && counter > 0)            // If white then flanked!
          flank_dir[dir] = true;
        else
          flank_dir[dir] = false;
      }
    }
    return flank_dir;
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

  public int countPieces(char[][] board, char player){
    int white_counter = 0;
    int black_counter = 0;
    for (int i = 1; i < board_size + 1; i++){
      for (int j = 1; j < board_size + 1; j++){
        if (board[i][j] == white)
          white_counter++;
        if (board[i][j] == black)
          black_counter++;
      }
    }
    if (player == 'w')
      return white_counter;
    else
      return black_counter;
  }

  public void update(char[][] board, char whos_turn){
    System.out.println("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n");
    System.out.println("    ▓▓▓ ▓▓▓ ▓ ▓ ▓▓▓ ▓   ▓   ▓▓▓");
    System.out.println("    ▓ ▓  ▓  ▓▓▓ ▓▓  ▓   ▓   ▓ ▓");
    System.out.println("    ▓▓▓  ▓  ▓ ▓ ▓▓▓ ▓▓▓ ▓▓▓ ▓▓▓");
    System.out.println();
    System.out.print("      White: " + countPieces(board, 'w'));
    System.out.println("\t    Black: " + countPieces(board, 'b'));
    //System.out.println();

    printBoard(board);

    /** Prints the current turn */
    if (whos_turn == black)
      System.out.println("        ** Black's Turn **");
    else
      System.out.println("        ** White's Turn **");

    // Pauses to show computer players move
    if (isComputerPlayer && whos_turn == comColor){
      System.out.print("\nPress [ENTER] to continue.");
      Scanner scan = new Scanner(System.in);
      scan.nextLine();
      scan.close();
    } else {
      System.out.println();
    }
  }

  public void printBoard(char[][] board){
    /** Prints colomn coord */
    System.out.print("      ");
    for (int i = 1; i < board_size + 1; i++)
      System.out.print((i - 1) + "  ");
    System.out.println();
    /** Prints top of board */
    System.out.print("      ");
    for (int i = 1; i < board_size + 1; i++)
      System.out.print("__" + " ");
    System.out.println();

    for (int i = 1; i < board_size + 1; i++){
      System.out.print("  " + (i - 1) + "  ");
      for (int j = 1; j < board_size + 1; j++){
        System.out.print("|" + board[i][j] + board[i][j]);
      }
      System.out.print("|\n");
    }
  }

  public void startUp(){
    System.out.println("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n");
    System.out.println("                  ▓ ▓ ▓▓▓ ▓   ▓▓▓ ▓▓▓ ▓▓▓ ▓▓▓");
    System.out.println("                  ▓▓▓ ▓▓  ▓   ▓   ▓ ▓ ▓▓▓ ▓▓ ");
    System.out.println("                  ▓▓▓ ▓▓▓ ▓▓▓ ▓▓▓ ▓▓▓ ▓ ▓ ▓▓▓");
    System.out.println();     
    System.out.println("                            ▓▓▓ ▓▓▓          ");
    System.out.println("                             ▓  ▓ ▓          ");
    System.out.println("                             ▓  ▓▓▓          ");
    System.out.println();     
    System.out.println("                  ▓▓▓ ▓▓▓ ▓ ▓ ▓▓▓ ▓   ▓   ▓▓▓");
    System.out.println("                  ▓ ▓  ▓  ▓▓▓ ▓▓  ▓   ▓   ▓ ▓");
    System.out.println("                  ▓▓▓  ▓  ▓ ▓ ▓▓▓ ▓▓▓ ▓▓▓ ▓▓▓");
    System.out.println("\n\n\n");
    while (true){
      System.out.print("\nAre you playing 1 player (agaist computer) or 2 player [1/2]: ");
      /** Scanning input */
      try {
        Scanner scan = new Scanner(System.in);
        int input = scan.nextInt();

        if (input == 1){
          isComputerPlayer = true;
          break;
        }
        else if (input == 2){
          isComputerPlayer = false;
          break;
        }
        scan.close();
      } catch (Exception e){}

      System.out.println("\n   ** Please type only '1' or '2' **");
    }
    if (isComputerPlayer){
      System.out.println("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n");
      while (true){
        System.out.print("\nWould you like to be black or white (NOTE: Black goes first) [b/w]? ");
        /** Scanning input */
        try {
          Scanner scan = new Scanner(System.in);
          String input = scan.nextLine();
          System.out.println(input);
          if (input.equalsIgnoreCase("w")){
            comColor = black;
            playerColor = white;
            break;
          }
          else if (input.equalsIgnoreCase("b")){
            comColor = white;
            playerColor = black;
            break;
          }
          scan.close();
        } catch (Exception e){}

        System.out.println("\n   ** Please type only 'b' or 'w' **");
      }
    }

    update(source_board, black);
  }

  public boolean isGameOver(boolean fb, boolean fw){
    if (fb && fw)
      return true;
    return false;
  }

  public void endGame(){
    System.out.println("Game has ended!!!");

    if (countPieces(source_board, 'w') > countPieces(source_board, 'b'))
      System.out.println("\n\n\n\nWhite WON!!!\n\n\n\n");
    else if (countPieces(source_board, 'b') > countPieces(source_board, 'w'))
      System.out.println("\n\n\n\nBlack WON!!!\n\n\n\n");
    else 
      System.out.println("\n\n\n\n It's a TIE!!!\n\n\n\n");
  }

  public static void main(String[] args){
    Othello othello = new Othello();
    othello.startUp();
    othello.run();
  }
}

