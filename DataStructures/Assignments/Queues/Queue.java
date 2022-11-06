/* ***************************************************************************
 * <Andrew Steen>
 * <11-01-21>
 * <Queue.java>
 *
 * <Queuein'>
 * **************************************************************************/
class Queue<john>
{

    List<john> list;

    // constructor
    public Queue()
    {
        list = new List<john>();
    }

    public Queue(Queue<john> other)
    {
        list = new List<john>(other.list);
    }

    public void Enqueue(john data)
    {
        list.Last();
        list.InsertAfter(data);
    }

    public john Dequeue()
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

    public boolean Equals(Queue<john> other)
    {
        return this.list.Equals(other.list);
    }

    public Queue<john> Add(Queue<john> other)
    {
        Queue<john> newQueue = new Queue<john>();

        newQueue.list = this.list.Add(other.list);
        return newQueue;
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
