//Game of Life but in Java
import java.io.*;
import java.util.concurrent.TimeUnit;

class Gol
{
	public static void main(String [] args)
	{
		boolean [][] board = readFile();
		printBoard(0, board);
		for (int gen = 1; gen < 10; gen++)
		{
			mySleep(100000);
			board = playGame(board);
			printBoard(gen, board);
		}
	}

	public static void mySleep(int msecs)
	{
		try
		{
			TimeUnit.MICROSECONDS.sleep(msecs);
		}catch (InterruptedException e){}
	}

	public static boolean [][] readFile()
	{
		boolean [][] board = null;
		int i = 0, size;

		try
		{
			BufferedReader br = new BufferedReader(
					new InputStreamReader(System.in));

			String line;
			while((line = br.readLine()) != null)
			{
				if (i == 0)
				{
					size = line.length();
					board = new boolean [size][size];
				}

				fillBoard(board, line, i);
				i++;
			}
			br.close();
		}catch (Exception e){}

		return board;
	}

	public static void fillBoard(boolean [][] board, 
			String line,int row)
	{
		for (int i = 0; i < line.length(); i++)
			board[row][i] =	(line.charAt(i) == '*') ? true : false;	// single line if else statement
	}

	public static void printBoard(int gen, boolean [][] board)
	{
		System.out.print("\033[H\033[2J");  
    	System.out.flush(); 

		System.out.println("Generation" + gen);
		for (int row = 0; row < board.length; row++)
		{
			for (int col = 0; col < board[row].length; col++)
				System.out.print(board[row][col] ? "*" : " ");
			System.out.println();
		}
	}

	public static boolean[][] playGame(boolean[][] board)
	{
		boolean [][] newboard = new boolean[board.length][board.length];

		for (int i = 1; i < board.length - 1; i++)
		{
			for (int j = 1; j < board.length - 1; j++)
			{
				int neighbors = countNeighbors(board, i, j);

				if (board[i][j])
					newboard[i][j] = (neighbors == 2 || neighbors == 3);
				else
					newboard[i][j] = (neighbors == 3);
			}
		}
		return newboard;
	}

	public static int countNeighbors(boolean[][] board, int row, int col)
	{
		int count = 0;

		for (int i = -1; i < 2; i++)
		{
			for (int j = -1; j < 2; j++)
			{
				if ((i != 0 || j != 0) && board[row + i][col + j])
					count++;
				//if (!(i = 0 && j == 0) && board[row+i][col+j])
				//	count++
			}
		}
		return count;
	}
}