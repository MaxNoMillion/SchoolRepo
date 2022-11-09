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
  char[][] source_board = new char[board_size + 2][board_size + 2];
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
  /** What game mode */
  boolean isComputerPlayer = false;
  /** Players' color (used when playing computer) */
  char comColor = white;
  char playerColor = white;
  /** Depth of search */
  int ply_depth = 7;
  /** Alpah/Beta Pruning toggle */
  boolean isAlphaBeta = false;

  // Scoreboard heuristic
  static final private int[][] score_board = {
		{1000, -100,  150,  100,  100,  150, -100, 1000},
		{-100, -200,   20,   20,   20,   20, -200, -100},
		{ 150,   20,   15,   15,   15,   15,   20,  150},
		{ 100,   20,   15,   10,   10,   15,   20,  100},
		{ 100,   20,   15,   10,   10,   15,   20,  100},
		{ 150,   20,   15,   15,   15,   15,   20,  150},
		{-100, -200,   20,   20,   20,   20, -200, -100},
		{1000, -100,  150,  100,  100,  150, -100, 1000}};

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
    // Main Game Loop //
    while (true){
      // Move Validity Check //
      /** The first check is to determine if a valid move exsists
      *  This is checked first to reduce total calculations */
      if (isPossibleMove()){
        /** For end-of-game detection 
        *  (resets forfeit boolean for current player) */
        if (whos_turn == black)
          forfeit_black = false;
        else forfeit_white = false;

        /** Is computer or player */
        if (isComputerPlayer && comColor == whos_turn){
          computerMove();
        }
        else
          playerMove();

      } else {
        /** Else current player forfeits turn */
        System.out.println("\n    No possible move. Forfeit turn.\n");
        /** End game trigger */
        if (isGameOver()){
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
      /** Where turn toggles */
      changeTurns();
      /** Where the board display is updated */
      updateBoardVisuals();
    }
  }

  public void computerMove(){
    if (isAlphaBeta)
      minimax(source_board, whos_turn);
    else
      minimax(source_board, whos_turn);
  }

  public void playerMove(){
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
  }

  public char[][] copyBoard(char[][] ori){
   char[][] copy = new char[board_size + 2][board_size + 2];
    /** Makes hard copies of same size boards */
    for (int i = 1; i < board_size + 1; i++)
      for (int j = 1; j < board_size + 1; j++)
        copy[i][j] = ori[i][j];
    return copy;
  }

  public int heuristic(char[][] board, char current_turn){
    /** Assigning who's who */
    char opponent = white;
    if (current_turn == white)
      opponent = black;
    /** Getting both scores */
    int ourScore = getScore(board, current_turn);
    int opponentScore = getScore(board, opponent);

    return ourScore - opponentScore;
  }

  public int[][] getPossibleMoves(char[][] board){
    int[][] possMoves = new int[64][2];
    int moveCounter = 0;
    for (int i = 1; i < board_size + 1; i++){
      for (int j = 1; j < board_size + 1; j++){
        int[] coords = {i, j};
        if (isMoveValid(coords)){
          possMoves[moveCounter + 1][0] = i;
          possMoves[moveCounter + 1][1] = j;
          moveCounter++;
        }
      }
    }
    possMoves[0][0] = moveCounter;
    return possMoves;
  }

  public int minimaxValue(char[][] board, int depth, char oriTurn, char currentTurn){
    /** Exit condition */
    if (depth == ply_depth || isGameOver()){
      return heuristic(board, oriTurn);
    }

    /** Assigns currentTurn as this will be what deturmines min or max */
    char otherTurn = black;
    if (currentTurn == black)
      otherTurn = white;

    /** Gets all possible moves for current turn. */
    int[][] possibleMoves = getPossibleMoves(board);

    /** If no possible move, then forfeit turn and load other's possible moves */
    if (possibleMoves[0][0] == 0){
      return minimaxValue(board, depth + 1, oriTurn, otherTurn);
    }
    else {
      /** Combining min and max default values */
      int bestEval = Integer.MIN_VALUE;
      if (oriTurn != currentTurn)
        bestEval = Integer.MAX_VALUE;

      //System.out.println(bestEval);

      // Runs through possible moves
      for (int i = 1; i < possibleMoves[0][0] + 1; i++){
        /** Hard copying current board to create branch */
        char[][] temp_board = copyBoard(board);

        /** Possible move of tempBoard */
        temp_board[possibleMoves[i][0]][possibleMoves[i][1]] = currentTurn;

        /** Recursively calling minimax fn to create more branches */
        int eval = minimaxValue(temp_board, depth + 1, oriTurn, otherTurn);

        /** Setting max and min values depending on if currentTurn 
         *  in a maximizing turn or minimizing turn */
        if (oriTurn == currentTurn){
          if (eval > bestEval)
            bestEval = eval;
        } else {
          if (eval < bestEval)
            bestEval = eval;
        }
      }
      return bestEval;
    }
  }

  public void minimax(char[][] board, char currentTurn){

    int[] best_coords = new int[2];

    /** Assigns currentTurn as this will be what deturmines min or max */
    char otherTurn = black;
    if (currentTurn == black)
      otherTurn = white;

    /** Gets all possible moves for current turn. */
    int[][] possibleMoves = getPossibleMoves(board);

    int bestEval = Integer.MIN_VALUE;

    for (int i = 1; i < possibleMoves[0][0] + 1; i++){

      /** Hard copying current board to create branch */
      char[][] temp_board = copyBoard(board);

      /** Possible move of tempBoard */
      temp_board[possibleMoves[i][0]][possibleMoves[i][1]] = currentTurn;

      int eval = minimaxValue(temp_board, 1, currentTurn, otherTurn);

      if (eval > bestEval){
        bestEval = eval;
        best_coords[0] = possibleMoves[i][0];
        best_coords[1] = possibleMoves[i][1];
      }  
    }
    moveCoords = best_coords;  
    // Forming movestate (Not great way, but don't have time to refactor)
    for (int dir = 0; dir < 8; dir++)
      move_state[dir] = isValidDirection(dir, moveCoords);
  }

  public int minimax(int pos, int depth, boolean maxiPlayer, int alpha, int beta){
    return 0;
  }
  
  public void calculateBoard(int[] moveCoords){
    /** Places piece down on selected tile. */
    if (whos_turn == black)
      source_board[moveCoords[0] + 1][moveCoords[1] + 1] = black;
    else
      source_board[moveCoords[0] + 1][moveCoords[1] + 1] = white;

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
      while (source_board[tempCoords[0] + dirStep[0] + 1][tempCoords[1] + dirStep[1] + 1] == white){
        /** Stepping to next flanked piece */
        tempCoords[0] += dirStep[0];
        tempCoords[1] += dirStep[1];
        /** Flipping flanked white pieces to black */
        source_board[tempCoords[0] + 1][tempCoords[1] + 1] = black;
      }
    }
    if (whos_turn == white){
      while (source_board[tempCoords[0] + dirStep[0] + 1][tempCoords[1] + dirStep[1] + 1] == black){
        /** Stepping to next flanked piece */
        tempCoords[0] += dirStep[0];
        tempCoords[1] += dirStep[1];
        /** Flipping flanked black pieces to white */
        source_board[tempCoords[0] + 1][tempCoords[1] + 1] = white;
      }
    }
  }

  public boolean isPossibleMove(){
    int[] scanCoords = new int[2];
    boolean valid = false;
    for (int i = 1; i < board_size + 1; i++){
      for (int j = 1; j < board_size + 1; j++){
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
    update();
  }

  public int getScore(char[][] board, char currentTurn){
    int score = 0;
    if (currentTurn == comColor){
      for (int i = 0; i < board_size; i++)
        for (int j = 0; j < board_size; j++)
          if (board[i + 1][j + 1] == comColor)
            score += score_board[i][j];
    } else {
      for (int i = 0; i < board_size; i++)
        for (int j = 0; j < board_size; j++)
          if (board[i + 1][j + 1] == playerColor)
            score += score_board[i][j];
    }
    return score;
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
    if ((source_board[moveCoords[0] + 1][moveCoords[1] + 1] != empty))
      return valid;

    // Checking each direction for flanking and recording flanking direction in move_state
    for (int dir = 0; dir < 8; dir++)
      move_state[dir] = isValidDirection(dir, moveCoords);
    
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
      while (source_board[tempCoords[0] + dirStep[0] + 1][tempCoords[1] + dirStep[1] + 1] == white){        // Steps through each tile in current direction         
        tempCoords[0] += dirStep[0];     // Steps tempCoord                                                           // as long as white
        tempCoords[1] += dirStep[1];       // Unique to each direction
        counter++;
      }
      if (source_board[tempCoords[0] + dirStep[0] + 1][tempCoords[1] + dirStep[1] + 1] == black && counter > 0){            // If black then flanked!
        return true;
      }
    }

    // Determining is direction is valid for current direction if white's turn //
    if (whos_turn == white){
      while (source_board[tempCoords[0] + dirStep[0] + 1][tempCoords[1] + dirStep[1] + 1] == black){        // Steps through each tile in current direction         
        tempCoords[0] += dirStep[0];     // Steps tempCoord                                                           // as long as black
        tempCoords[1] += dirStep[1];       // Unique to each direction
        counter++;
      }
      if (source_board[tempCoords[0] + dirStep[0] + 1][tempCoords[1] + dirStep[1] + 1] == white && counter > 0)            // If white then flanked!
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

  public boolean isGameOver(){
    if (forfeit_black && forfeit_white)
      return true;
    return false;
  }

  public void endGame(){
    System.out.println("Game has ended!!!");

    if (counterPieces('w') > counterPieces('b'))
      System.out.println("\n\n\n\nWhite WON!!!\n\n\n\n");
    else if (counterPieces('b') > counterPieces('w'))
      System.out.println("\n\n\n\nBlack WON!!!\n\n\n\n");
    else 
      System.out.println("\n\n\n\n It's a TIE!!!\n\n\n\n");
  }
  
  public int counterPieces(char player){
    int white_counter = 0;
    int black_counter = 0;
    for (int i = 1; i < board_size + 1; i++){
      for (int j = 1; j < board_size + 1; j++){
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

  public void update(){
    System.out.println("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n");
    System.out.println("    ▓▓▓ ▓▓▓ ▓ ▓ ▓▓▓ ▓   ▓   ▓▓▓");
    System.out.println("    ▓ ▓  ▓  ▓▓▓ ▓▓  ▓   ▓   ▓ ▓");
    System.out.println("    ▓▓▓  ▓  ▓ ▓ ▓▓▓ ▓▓▓ ▓▓▓ ▓▓▓");
    System.out.println();
    System.out.print("      White: " + counterPieces('w'));
    System.out.println("\t    Black: " + counterPieces('b'));
    //System.out.println();

    printBoard(source_board);

    /** Prints the current turn */
    if (whos_turn == black)
      System.out.println("        ** Black's Turn **");
    else
      System.out.println("        ** White's Turn **");

    // Pauses to show computer players move
    if (isComputerPlayer && whos_turn == comColor){
      System.out.print("\nPress [ENTER] to continue.");
      Scanner scan = new Scanner(System.in);
      String input = scan.nextLine();
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
        } catch (Exception e){}

        System.out.println("\n   ** Please type only 'b' or 'w' **");
      }
    }

    update();
  }
  /////// MAIN ///////
  public static void main(String[] args){
    Othello othello = new Othello();
    othello.startUp();
    othello.run();
  }
}