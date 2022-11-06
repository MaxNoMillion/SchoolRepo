class NodeTestTest
{
    public static void main(String[] args)
    {
        Node head = new Node();

        int[] myArray = createAscendingArray(30);

        nodeArray(head, myArray);
        print(head);
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

    public static void nodeArray(Node n, int[] arr)
    {
        Node curr = n;
        Node temp;
        // sets the head node data
        // the head node has a default value of 0
        curr.setData(arr[0]);
        for (int i = 1; i < arr.length; i++)
        {
            temp = new Node();
            temp.setData(arr[i]);
            curr.setLink(temp);
            curr = temp;
        }
    }

    public static int[] createAscendingArray(int size)
    {      
        int[] arr = new int[size];
        for(int i = 0; i < size; i++)
        {
            arr[i] += i + 1;
        }
        return arr;
    }
}