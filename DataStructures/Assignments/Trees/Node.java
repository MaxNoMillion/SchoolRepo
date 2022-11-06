// A node class. This is just one component of the Tree class you are
// required to design.
class Node
{
    private int data;
    private Node left;
    private Node right;

    // A constructor that takes the input data as its argument and sets
    // the left and right links to null.
    public Node(int data)
    {
	this.data = data;
	this.left = null;
	this.right = null;
    }

    // A constructor that takes no input, sets the data to 0 and sets
    // the left and right links to null.
    public Node()
    {
	this.data = 0;
	this.left = null;
	this.right = null;
    }

    // Accessors and mutators for the 3 different fields that the node
    // has.
    public void setData(int data)
    {
	this.data = data;
    }

    public void setLeft(Node left)
    {
	this.left = left;
    }

    public void setRight(Node right)
    {
	this.right = right;
    }

    public int getData()
    {
	return this.data;
    }

    public Node getLeft()
    {
	return this.left;
    }

    public Node getRight()
    {
	return this.right;
    }

    // A toString function that allows a node to be printed easily.
    public String toString()
    {
	return "" + this.data;
    }
}

