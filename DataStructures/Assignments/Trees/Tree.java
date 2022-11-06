import javax.lang.model.util.ElementScanner14;

/* ***************************************************************************
 * <Andrew Steen>
 * <11-05-21>
 * <Tree.java>
 *
 * <Treein'>
 * **************************************************************************/
class Tree
{
    private Node root;
    private int size;
    public static final int MAX_SIZE = 30;

    // Constructor. An empty tree has a size of 0.
    public Tree()
    {
        this.root = null;
        size = 0;
    }

    // Copy constructor. Clones Tree t (i.e. its nodes, and its size)
    public Tree(Tree t)
    {
        this.root = mycopy(t.root);
        this.size = t.size;
    }

    // Private copy function that recursively copies Node a (along with
    // all its links, and returns that copy.
    private Node mycopy(Node a)
    {
        if (a == null)
            return null;
        else
        {
            Node newNode = new Node(a.getData());
            newNode.setLeft(mycopy(a.getLeft()));
            newNode.setRight(mycopy(a.getRight()));
            return newNode;
        }
    }

    // function that takes the key and calls the deleteKey function.
    // Should only work if the tree is not empty.
    public void Delete(int key)
    {
        if (!IsEmpty())
        {
            this.root = DeleteKey(this.root, key); 
        }
    }

    // private recursive function that takes a node, and the key to delete from
    // the subtrees attached to that node. It returns a copy of the tree
    // with the required node having been removed from the appropriate subtrees.
    private Node DeleteKey(Node a, int key)
    {
        if (a == null)
            return a;
        if (key < a.getData())
            a.setLeft(DeleteKey(a.getLeft(), key));
        else if (key > a.getData())
            a.setRight(DeleteKey(a.getRight(), key));
        else
        {
            if (a.getLeft() == null)
            {
                this.size--;
                return a.getRight();
            }
            else if (a.getRight() == null)
            {
                this.size--;
                return a.getLeft();
            }
            a.setData(Successor(a).getData());
            a.setRight(DeleteKey(a.getRight(), a.getData()));
        }
        return a;
    }

    // Private function to find the successor to a node. The successor
    // of a node in a binary tree is the node immediately larger than
    // the required node.
    private Node Successor(Node a)
    {
        a = a.getRight();
        while (a.getLeft() != null)
            a = a.getLeft();
        return a;
    }


    // Function to insert data into the tree in its appropriate location
    // by using the Add() recursive function. This should not be
    // possible for a tree that is already full. If the tree is empty,
    // then it does the insertion itself.
    public void Insert(int data)
    {
        if (IsFull())
            return;
        else if (IsEmpty())
        {
            this.root = new Node();
            this.root.setData(data);
            this.size++;
        }
        else
        {
            Add(data, this.root);
            this.size++;
        }
    }

    // Private recursive function that takes a Node attached to its own 
    // subtrees, and attaches the data to the tree in the proper location.
    private void Add(int data, Node a)
    {
        if (data < a.getData())
            if (a.getLeft() != null)
                Add(data, a.getLeft());
            else
            {
                a.setLeft(new Node());
                a.getLeft().setData(data);
            }
        else
            if (a.getRight() != null)
                Add(data, a.getRight());
            else
            {
                a.setRight(new Node());
                a.getRight().setData(data);
            }
    }

    // function to return the size of the tree (i.e. the number of nodes
    // in the tree).
    public int Size()
    {
        return this.size;
    }

    // Function to tell whether the tree is empty or not.
    public boolean IsEmpty()
    {
        return Size() == 0;
    }

    // Function to tell whether the tree is full or not.
    public boolean IsFull()
    {
        return Size() == this.MAX_SIZE;
    }

    // Function to return the InOrder traversal of the tree. It takes a
    // string as its argument, updates the string with the node
    // information, and then returns the updated string that should 
    // contain the inorder traversal of the tree.
    private String InOrder(Node a, String s)
    {
        //LNR
        if (a == null)
            return s;
        return InOrder(a.getLeft(), s) + a.getData() + " " + InOrder(a.getRight(), s);
    }

    // Function to return the PreOrder traversal of the tree. It takes a
    // string as its argument, updates the string with the node
    // information, and then returns the updated string that should 
    // contain the preorder traversal of the tree.
    private String PreOrder(Node a, String s)
    {
        //NLR
        if (a == null)
            return s;
        return a.getData() + " " + PreOrder(a.getLeft(), s) + PreOrder(a.getRight(), s);
    }

    // Function to return the PostOrder traversal of the tree. It takes a
    // string as its argument, updates the string with the node
    // information, and then returns the updated string that should 
    // contain the postorder traversal of the tree.
    private String PostOrder(Node a, String s)
    {
        if (a == null)
            return s;
        return PostOrder(a.getLeft(), s) + PostOrder(a.getRight(), s) + a.getData() + " ";
    }

    // A function that returns the maximum value in the tree. That value
    // is -1 for an empty tree.
    public int getMax()
    {   
        if (IsEmpty())
            return -1;
        else
        {
            Node temp = this.root;
            while (temp.getRight() != null)
                temp = temp.getRight();
            return temp.getData();
        }
    }

    // A function that returns the minimum value in the tree. That value
    // is -1 for an empty tree.
    public int getMin()
    {
        if (IsEmpty())
            return -1;
        else
        {
            Node temp = this.root;
            while (temp.getLeft() != null)
                temp = temp.getLeft();
            return temp.getData();
        }
    }

    // A toString function that returns "NULL" if the tree is empty.
    // Otherwise, it returns the InOrder traversal of the tree.
    public String toString()
    {
        if (IsEmpty())
            return "NULL";
        else
        {
            String result = "";
            return InOrder(this.root, result);
        }
    }

    // A Print function that prints out the InOrder, PreOrder, and
    // PostOrder traversals of the tree (each one preceeded by the word
    // identifying what kind of traversal it is). It also calls the
    // private Print() function which prints out the tree sideways.
    public void Print()
    {
        String str = "";
        System.out.println("InOrder: " + InOrder(this.root, str));
        System.out.println("PreOrder: " + PreOrder(this.root, str));
        System.out.println("PostOrder: " + PostOrder(this.root, str));
        Print(this.root, 0);
    }

    // A Print function that takes a node and an int to recursively print
    // out the tree sideways. The int "lev" determines how far away from
    // the root that particular node will be printed. (Refer to notes for 
    // details of this function).
    private void Print(Node n, int lev)
    {
        if (n != null)
        {
            Print(n.getRight(), lev + 1);
            for (int i = 0; i < lev; i++)
                System.out.print("\t");
            System.out.println(n.getData());
            Print(n.getLeft(), lev + 1);
        }
    }

    // A function that returns if two trees are equal by value.
    public boolean Equals(Tree t)
    {
        return EqualsRecurs(this.root, t.root);
    }

    private boolean EqualsRecurs(Node a, Node b)
    {
        // checking if nodes equal
        if (a == b)
            return true;
        // checking if the branch is different
        if (a == null || b == null)
            return false;
        // recursively checks each node pairs data in trees in Preorder Traversal
        return (a.getData() == b.getData()) && EqualsRecurs(a.getLeft(), b.getLeft())
                && EqualsRecurs(a.getRight(), b.getRight());
    }
}
