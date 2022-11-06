class NodeTest
{
    public static void main(String[] args)
    {   
        int [] arr = {5, 10, 15, 20, 25};

        Node first, last, curr;

        first = last = curr = null;

        for (int i = 0; i < arr.length; i++)
        {
            curr = new Node();
            curr.setData(arr[i]);
            
            if (first == null) // if there is no node in my list
            {
                first = last = curr;    // then make curr the only node
            }
            else
            {
                last.setLink(curr);
                last = curr;
            }
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