class Node<john>
{
    private john data;
    private Node link;

    public Node()
    {
        data = null;
        link = null;
    }

    public void setData(john data)
    {
        this.data = data;
    }
    public void setLink(Node link)
    {
        this.link = link;
    }

    public john getData()
    {
        return this.data;
    }
    public Node getLink()
    {
        return this.link;
    }

    public String toString()
    {
        return "" + this.data;
    }
}

class NodeTest
{
    public static void main(String [] args)
    {
        Node<Integer> a = new Node<Integer>();
        a.setData(23);
        System.out.println(a);
        Node<Character> b = new Node<Character>();
        b.setData('b');
        System.out.println(b);
    }
}