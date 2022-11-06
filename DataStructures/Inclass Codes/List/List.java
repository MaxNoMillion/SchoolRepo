import javax.lang.model.util.ElementScanner14;

/* ***************************************************
 * <your name>
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
		list = new char[MAX_SIZE];
		end = curr = -1;
	}

	// copy constructor
	// clones the list l and sets the last element as the current
	public List(List l)
	{
		list = new char[MAX_SIZE];
		end = curr = -1;
		for (int i = 0; i < l.GetSize(); i++)
			this.InsertAfter(l.list[i]);
	}

	// navigates to the beginning of the list
	public void First()
	{
		if (!IsEmpty())
			curr = 0;
	}

	// navigates to the end of the list
	// the end of the list is at the last valid item in the list
	public void Last()
	{
		curr = end;
	}

	// navigates to the specified element (0-index)
	// this should not be possible for an empty list
	// this should not be possible for invalid positions
	public void SetPos(int pos)
	{
		if (!IsEmpty() && pos >= 0 && pos <= end)
			curr = pos;
	}

	// navigates to the previous element
	// this should not be possible for an empty list
	// there should be no wrap-around
	public void Prev()
	{
		if (curr > 0)
			curr--;
	}

	// navigates to the next element
	// this should not be possible for an empty list
	// there should be no wrap-around
	public void Next()
	{
		if (!IsEmpty() && curr < end)
			curr++;
	}

	// returns the location of the current element (or -1)
	public int GetPos()
	{
		return curr;
	}

	// returns the value of the current element (or -1)
	public char GetValue()
	{
		if(IsEmpty())
			return (char)32;
		else
			return list[curr];
	}

	// returns the size of the list
	// size does not imply capacity
	public int GetSize()
	{
		return (end + 1);
	}

	// inserts an item before the current element
	// the new element becomes the current
	// this should not be possible for a full list
	public void InsertBefore(char data)
	{
		if (IsEmpty() || IsFull())
			InsertAfter(data);
		else 
		{
			curr--;
			InsertAfter(data);
		}
	}

	// inserts an item after the current element
	// the new element becomes the current
	// this should not be possible for a full list
	public void InsertAfter(char data)
	{
		if (!IsFull())
		{
			if (IsEmpty())
			{
				end = curr = 0;
				list[curr] = data;
			}
			else if (end == curr)
			{
				end += 1;
				curr += 1;
				list[curr] = data;
			}
			else
			{
				// move everything over
				for (int i = end; i > curr; i--)
				{
					list[i+1] = list[i];
				}

				list[curr+1] = data;
				curr++;
				end++;
			}
		}
	}

	// removes the current element (collapsing the list)
	// this should not be possible for an empty list
	public void Remove()
	{
		if (!IsEmpty())
		{
			if (end == curr)
			{
				end--;
				curr--;
			}
			else
			{	
				for (int i = curr; i < end; i++)
					list[i] = list[i+1];
				end--;
			}
		}
	}

	// replaces the value of the current element with the specified value
	// this should not be possible for an empty list
	public void Replace(char data)
	{
		if (!IsEmpty())
		{
			list[curr] = data;
		}
	}

	// returns if the list is empty
	public boolean IsEmpty()
	{
		return (end == -1);
	}

	// returns if the list is full
	public boolean IsFull()
	{
		return (end >= MAX_SIZE - 1);
	}

	// returns if two lists are equal (by value)
	public boolean Equals(List l)
	{
		if (GetSize() != l.GetSize())
			return false;

		for (int i = 0; i <= end; i++)
			if (this.list[i] != l.list[i])
				return false;
		return true;
	}

	// returns the concatenation of two lists
	// l should not be modified
	// l should be concatenated to the end of *this
	// the returned list should not exceed MAX_SIZE elements
	// the last element of the new list is the current
	public List Add(List l)
	{
		List sum = new List(this);

		for (int i = 0; i < l.GetSize(); i++)
			sum.InsertAfter(l.list[i]);
		return sum;
	}

	// returns a string representation of the entire list (e.g., 1 2 3 4 5)
	// the string "NULL" should be returned for an empty list
	public String toString()
	{
		if (IsEmpty())
			return "NULL";
		else
		{
			String result = "";
			for (int i = 0; i <= end; i++)
				result += list[i] + " ";
			return result;
		}
	}
}
