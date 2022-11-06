class NodeTest
{
    public static void main(String[] args)
    {   
        int [] arr = {5, 10, 15, 20, 25};

        Node first, last, curr;

        first = curr = null;

        for (int i = 0; i < arr.length; i++)
        {
            curr = new Node();
            curr.setData(arr[i]);
            
            curr.setLink(first);    // make the new node point to head
            first = curr;   // make new node the head
        }

        print(first);
    }

    public static void print(Node n)
    {
        while (n != null)
        {
            System.out.print(n);
            n = n.getLink();
        }
        System.out.println();
    }
}