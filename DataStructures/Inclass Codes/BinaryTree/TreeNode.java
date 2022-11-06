class TreeNode 
{
    private TreeNode left;
    private TreeNode right;
    private int data;

    public TreeNode()
    {
        data = 0;
        left = right = null;
    }

    // accessor and mutator for data
    public int getData()
    {
        return data;
    }

    public void setData(int data)
    {
        this.data = data;
    }

    // accessor and mutator for left node
    public TreeNode getLeft()
    {
        return left;
    }

    public void setLeft(TreeNode left)
    {
        this.left = left;
    }

    // accessor and mutator for right node
    public TreeNode getRight()
    {
        return right;
    }

    public void setRight(TreeNode right)
    {
        this.right = right;
    }
    
}
