class Node
{
    private int data;
    private Node link;

    public Node()
    {
        this.data = 0;
        this.link = null;
    }

    // Accessor and Mutator for the data component
    public int getData()
    {
        return this.data;
    }

    public void setData(int data)
    {
        this.data = data;
    }

    // Accessor and Mutator for the link component
    public Node getLink()
    {
        return this.link;
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