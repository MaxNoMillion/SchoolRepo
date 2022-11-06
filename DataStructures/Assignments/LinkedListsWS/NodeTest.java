class NodeTest 
{
    public static void main(String[] args)
    {
        Node head, tail;
        head = tail = null;
        head = new Node();

        head.setData(5);
        print(head);

        head.setLink(new Node());
        tail = head.getLink();
        tail.setData(10);
        print(head);

        int[] arr = {15, 20, 25, 30, 35};
        Node temp;

        for (int i = 0; i < arr.length; i++)
        {
            temp = new Node();
            temp.setData(arr[i]);
            tail.setLink(temp);
            tail = temp;
        }
        print(head);

        temp = new Node();
        temp.setData(12);
        temp.setLink(head.getLink().getLink());
        head.getLink().setLink(temp);
        print(head);

        head = head.getLink();
        print(head);

        temp = head;
        while (temp != tail.getLink())
        {
            temp.setData(temp.getData()*temp.getData());
            temp = temp.getLink();
        }
        print(head);

        head.setLink(null);
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
}
