class Node
{
    private int data;
    private Node link;

    public Node()
    {
        data = 0;
        link = null;
    }

    // accessors and mutators
    public int getData()
    {
        return data;
    }
    public void setData(int data)
    {
        this.data = data;
    }

    public Node getLink()
    {
        return link;
    }
    public void setLink(Node link)
    {
        this.link = link;
    }
    
    public String toString()
    {
        return "" + getData() + "->";
    }
}