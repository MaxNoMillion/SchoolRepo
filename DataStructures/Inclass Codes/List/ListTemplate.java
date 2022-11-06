/* ***************************************************
 * <Andrew Steen>
 * <the date>
 * <the file name>
 *
 * <a simple, short program/class description>
 *************************************************** */

// the EasyList class
public class List
{
	public static final int MAX_SIZE = 50;

	private int end;	// the index of the last valid item in the list
	private int curr;	// the index of the current item in the list
	private char[] list;	// the list

	// constructor
	// remember that an empty list has a "size" of -1 and its "position" is at -1
	public List()
	{
	}

	// copy constructor
	// clones the list l and sets the last element as the current
	public List(List l)
	{
	}

	// navigates to the beginning of the list
	public void First()
	{
	}

	// navigates to the end of the list
	// the end of the list is at the last valid item in the list
	public void Last()
	{
	}

	// navigates to the specified element (0-index)
	// this should not be possible for an empty list
	// this should not be possible for invalid positions
	public void SetPos(int pos)
	{
	}

	// navigates to the previous element
	// this should not be possible for an empty list
	// there should be no wrap-around
	public void Prev()
	{
	}

	// navigates to the next element
	// this should not be possible for an empty list
	// there should be no wrap-around
	public void Next()
	{
	}

	// returns the location of the current element (or -1)
	public int GetPos()
	{
	}

	// returns the value of the current element (or -1)
	public char GetValue()
	{
	}

	// returns the size of the list
	// size does not imply capacity
	public int GetSize()
	{
	}

	// inserts an item before the current element
	// the new element becomes the current
	// this should not be possible for a full list
	public void InsertBefore(char data)
	{
	}

	// inserts an item after the current element
	// the new element becomes the current
	// this should not be possible for a full list
	public void InsertAfter(char data)
	{
	}

	// removes the current element (collapsing the list)
	// this should not be possible for an empty list
	public void Remove()
	{
	}

	// replaces the value of the current element with the specified value
	// this should not be possible for an empty list
	public void Replace(char data)
	{
	}

	// returns if the list is empty
	public boolean IsEmpty()
	{
	}

	// returns if the list is full
	public boolean IsFull()
	{
	}

	// returns if two lists are equal (by value)
	public boolean Equals(List l)
	{
	}

	// returns the concatenation of two lists
	// l should not be modified
	// l should be concatenated to the end of *this
	// the returned list should not exceed MAX_SIZE elements
	// the last element of the new list is the current
	public List Add(List l)
	{
	}

	// returns a string representation of the entire list (e.g., 1 2 3 4 5)
	// the string "NULL" should be returned for an empty list
	public String toString()
	{
	}
}
