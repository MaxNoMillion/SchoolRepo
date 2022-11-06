/* ***************************************************************************
 * <Andrew Steen>
 * <11-01-21>
 * <Stack.java>
 *
 * <Stackin'>
 * **************************************************************************/
class Stack<john>
{
    List<john> list;

    // constructor
    public Stack()
    {
        list = new List<john>();
    }

    public Stack(Stack<john> other)
    {
        list = new List<john>(other.list);
    }

    public void Push(john data)
    {
        list.First();
        list.InsertBefore(data);
    }

    public john Pop()
    {
        list.First();
        john result = list.GetValue();
        list.Remove();
        return result;
    }

    public john Peek()
    {
        list.First();
        return list.GetValue();
    }

    public int Size()
    {   
        return list.GetSize();
    }

    public boolean IsEmpty()
    {
        return list.IsEmpty();
    }

    public boolean IsFull()
    {
        return list.IsFull();
    }

    public boolean Equals(Stack<john> other)
    {
        return this.list.Equals(other.list);
    }

    public Stack<john> Add(Stack<john> other)
    {
        Stack<john> newstack = new Stack<john>();

        newstack.list = this.list.Add(other.list);
        return newstack;
    }

    public String toString()
    {
        if (IsEmpty())
			return "NULL";
		else
		{
            list.First();
			String result = "";
			for (int i = 0; i < list.GetSize(); i++)
            {
                result += list.GetValue() + " ";
                list.Next();
            }
			return result;
		}
    }
}
