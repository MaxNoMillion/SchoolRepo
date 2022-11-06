import javax.lang.model.util.ElementScanner14;

class Tree2 
{
    public static void main(String [] args)
    {
        int [] arr = {72, 23, 84, 7 , 2, 22, 222};

        TreeNode root = null;
        for (int i = 0; i < arr.length; i++)
        {
            insert(arr[i], root);
        }

        inOrder(root);
        System.out.println();

        print(root, 1);
        System.out.println();
    }   

    public static TreeNode insert(int x, TreeNode root)
    {
        TreeNode current, trail, newNode;
        current = trail = newNode = null;

        // create the node
        newNode = new TreeNode();
        newNode.setData(x);

        if (root == null)
            root = newNode;
        else
        {
            current = root;
            while (current != null)
            {
                trail = current;

                if (current.getData() == x)
                {
                    System.out.println("Duplicate values");
                    return root;
                }
                else if (current.getData() > x)
                    current = current.getLeft();
                else 
                    current = current.getRight();
            }

            if (trail.getData() > x)
                trail.setLeft(newNode);
            else
                trail.setRight(newNode);
        }

        return root;
    }

    public static void inOrder(TreeNode t)
    {
        if (t != null)
        {
            inOrder(t.getLeft());
            System.out.print(t.getData() + ", ");
            inOrder(t.getRight());
        }
    }

    public static void print(TreeNode n, int lev)
    {
        if (n != null)
        {
            print(n.getRight(), lev+1);
            for (int i = 0; i < lev; i++);
                System.out.print("\t");
            System.out.println(n.getData());

            print(n.getLeft(), lev+1);
        }
    }
}
