class Tree 
{
    public static void main(String [] args)
    {
        TreeNode root = new TreeNode();
        root.setData(37);

        // One way of adding a node to a tree
        TreeNode a = new TreeNode();
        a.setData(48);

        root.setLeft(a);

        // Another way of adding a node to a tree
        root.setRight(new TreeNode());
        root.getRight().setData(16);

        a.setLeft(new TreeNode());
        a = a.getLeft();
        a.setData(2);

        a.setLeft(new TreeNode());
        a.getLeft().setData(7);
        a.setRight(new TreeNode());
        a.getRight().setData(50);

        inOrder(root);
    }

    public static void inOrder(TreeNode t)
    {
        if (t != null)
        {
            inOrder(t.getLeft());
            // do processing
            System.out.print(t.getData() + " ");
            inOrder(t.getRight());
        }
    }

    public static void preOrder(TreeNode t)
    {
        if (t != null)
        {
            // do processing
            System.out.print(t.getData() + " ");
            preOrder(t.getLeft());
            preOrder(t.getRight());
        }
    }

    public static void postOrder(TreeNode t)
    {
        if (t != null)
        {
            postOrder(t.getLeft());
            postOrder(t.getRight());
            // do processing
            System.out.print(t.getData() + " ");
        }
    }
}
