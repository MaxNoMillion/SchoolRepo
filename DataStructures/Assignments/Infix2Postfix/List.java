import javax.lang.model.util.ElementScanner14;

/* ***************************************************
 * <Andrew Steen>
 * <10-15-21>
 * <list.java>
 *
 * <Various Fuctions to Help Munipulate Linked Lists>
 *************************************************** */

// the Node class
class Node<john>
{
	private john data;
	private Node<john> link;

	// constructor
	public Node()
	{
		this.data = null;
		this.link = null;
	}

	// accessor and mutator for the data component
	public john getData()
	{
		return this.data;
	}

	public void setData(john data)
	{
		this.data = data;
	}

	// accessor and mutator for the link component
	public Node getLink()
	{
		return this.link;
	}

	public void setLink(Node link)
	{
		this.link = link;
	}
}

// the List class
public class List<john>
{
	public static final int MAX_SIZE = 1024;

	private Node<john> head;
	private Node<john> tail;
	private Node<john> curr;
	private int num_items;

	// constructor
	// remember that an empty list has a "size" of 0 and its "position" is at -1
	public List()
	{
		head = tail = curr = null;
		num_items = 0;
	}

	// copy constructor
	// clones the list l and sets the last element as the current
	public List(List<john> l)
	{	
		if (l.head != null)
		{
			Node<john> inc;
			this.head = new Node();
			this.head.setData(l.head.getData());
			this.tail = this.head;
			inc = l.head;

			while (inc != l.tail)
			{
				this.tail.setLink(new Node());
				this.tail = this.tail.getLink();
				inc = inc.getLink();
				this.tail.setData(inc.getData());
			}
			this.curr = this.tail;
			this.num_items = l.num_items;
		}
		else if (l.head == null)
		{
			this.head = this.curr = this.tail = null;
			this.num_items = 0;
		}
	}

	// navigates to the beginning of the list
	public void First()
	{
		this.curr = this.head;
	}

	// navigates to the end of the list
	// the end of the list is at the last valid item in the list
	public void Last()
	{
		this.curr = this.tail;
	}

	// navigates to the specified element (0-index)
	// this should not be possible for an empty list
	// this should not be possible for invalid positions
	public void SetPos(int pos)
	{
		if (!IsEmpty() && pos >= 0 && pos < GetSize())
		{
			this.curr = this.head;
			for (int i = 0; i < pos; i++)
				this.curr = this.curr.getLink();
		}
	}

	// navigates to the previous element
	// this should not be possible for an empty list
	// there should be no wrap-around
	public void Prev()
	{
		if (!IsEmpty() && this.curr != this.head)
		{
			Node<john> inc;
			inc = this.head;
			while (inc.getLink() != this.curr)
				inc = inc.getLink();
			this.curr = inc;
		}
	}

	// navigates to the next element
	// this should not be possible for an empty list
	// there should be no wrap-around
	public void Next()
	{
		if (!IsEmpty() && this.curr != this.tail)
		{
			this.curr = this.curr.getLink();
		}
	}

	// returns the location of the current element (or -1)
	public int GetPos()
	{
		if (IsEmpty())
			return -1;
		else
		{
			Node<john> temp;
			int pos = -1;
			temp = this.head;
			while (temp != this.curr.getLink())
			{
				temp = temp.getLink();
				pos++;
			}
			return pos;
		}
	}

	// returns the value of the current element (or -1)
	public john GetValue()
	{
		if (IsEmpty())
			return null;
		else
			return curr.getData();
	}

	// returns the size of the list
	// size does not imply capacity
	public int GetSize()
	{
		if (IsEmpty())
			return 0;
		else
			return this.num_items;
	}

	// inserts an item before the current element
	// the new element becomes the current
	// this should not be possible for a full list
	public void InsertBefore(john data)
	{
		if (IsEmpty() || IsFull())
			InsertAfter(data);
		else if (this.head == this.curr)
		{
			Node<john> temp;
			temp = new Node();
			temp.setData(data);
			temp.setLink(this.head);
			this.head = this.curr = temp;
			this.num_items++;
		}
		else
		{
			Node<john> inc;
			Node<john> temp;
			inc = this.head;
			temp = new Node();
			temp.setData(data);
			while(inc.getLink() != this.curr)
				inc = inc.getLink();
			inc.setLink(temp);
			temp.setLink(this.curr);
			this.curr = temp;
			this.num_items++;
		}
	}

	// inserts an item after the current element
	// the new element becomes the current
	// this should not be possible for a full list
	public void InsertAfter(john data)
	{
		Node<john> temp;
		temp = new Node();
		temp.setData(data);

		if (!IsFull())
		{
			if (IsEmpty())
			{
				this.head = new Node();
				this.head.setData(data);
				this.curr = this.tail = this.head;
			}
			else if (this.curr == this.tail)
			{	
				temp = new Node();
				temp.setData(data);
				this.curr.setLink(temp);
				this.tail = this.curr = temp;
			}
			else
			{
				temp = new Node();
				temp.setData(data);
				temp.setLink(this.curr.getLink());
				this.curr.setLink(temp);
				this.curr = temp;
			}
			this.num_items++;
		}
	}

	// removes the current element (collapsing the list)
	// this should not be possible for an empty list. If possible,
	// following element becomes new current element.
	public void Remove()
	{
		if (!IsEmpty())
		{
			if (this.curr == this.tail && GetSize() != 1)
			{
				Prev();
				this.tail = this.curr;
				this.curr.setLink(null);
			}
			else if (this.curr == this.head)
			{
				this.head = this.head.getLink();
				this.curr = this.head;
			}
			else
			{
				Prev();
				this.curr.setLink(this.curr.getLink().getLink());
				this.curr = this.curr.getLink();
			}
			this.num_items--;
		}
	}

	// replaces the value of the current element with the specified value
	// this should not be possible for an empty list
	public void Replace(john data)
	{
		if (!IsEmpty())
			this.curr.setData(data);
	}

	// returns if the list is empty
	public boolean IsEmpty()
	{
		return (this.head == null);
	}

	// returns if the list is full
	public boolean IsFull()
	{
		return (GetSize() == MAX_SIZE);
	}

	// returns if two lists are equal (by value)
	public boolean Equals(List l)
	{
		if (GetSize() != l.GetSize())
			return false;
		
		Node<john> l_inc;
		Node<john> this_inc;
		l_inc = l.head;
		this_inc = this.head;

		while (l_inc != l.tail)
		{
			if (l_inc.getData() != this_inc.getData())
				return false;
			l_inc = l_inc.getLink();
			this_inc = this_inc.getLink();
		}
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

		if (l.head != null && this.head != null)
		{
			sum.tail.setLink(l.head);
			sum.tail = sum.curr = l.tail;
		}
		else if (l.head == null  && this.head != null)
		{
			sum.head = this.head;
			sum.tail = sum.curr = this.tail;
		}
		else if (l.head != null  && this.head == null)
		{	
			sum.head = l.head;
			sum.tail = sum.curr = l.tail;
		}
		else
		{
			sum.head = sum.curr = sum.tail = null;
		}
		sum.num_items = this.num_items + l.num_items;

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
			Node<john> temp;
			temp = this.head;
			String result = "";
			while (temp != this.tail.getLink())
			{
				result += temp.getData() + "";
				temp = temp.getLink();
			}
			return result;
		}
	}
}
