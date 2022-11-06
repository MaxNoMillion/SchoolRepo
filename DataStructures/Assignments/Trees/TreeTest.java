/* ***************************************************************
 * ---------YOU MAY NOT CHANGE THIS FILE IN ANY WAY---------------
 * ***************************************************************/


import java.util.Random;

public class TreeTest
{
    public static void main(String [] args)
    {
	// Declaring an empty tree a, checking Size(), IsEmpty(),
	// IsFull(), and toString()
	Tree a = new Tree();
	System.out.print("1:  a(" + a.Size() + ",");
	System.out.print((a.IsEmpty() ? "T": "F") + ",");
	System.out.println((a.IsFull() ? "T": "F") + ") =\t" + a);

	// Adding a single node to a
	a.Insert(10);
	System.out.print("2:  a(" + a.Size() + ",");
	System.out.print((a.IsEmpty() ? "T": "F") + ",");
	System.out.println((a.IsFull() ? "T": "F") + ") =\t" + a);
	
	a.Insert(20);
	System.out.print("3:  a(" + a.Size() + ",");
	System.out.print((a.IsEmpty() ? "T": "F") + ",");
	System.out.println((a.IsFull() ? "T": "F") + ") =\t" + a);

	a.Insert(5);
	System.out.print("4:  a(" + a.Size() + ",");
	System.out.print((a.IsEmpty() ? "T": "F") + ",");
	System.out.println((a.IsFull() ? "T": "F") + ") =\t" + a);


	//Adding multiple nodes to a	
	int [] list = {18, 19, 25, 1, 7, 3, 6, 30, 24};
	for (int i = 0; i < list.length; i++)
	    a.Insert(list[i]);
	System.out.print("5:  a(" + a.Size() + ",");
	System.out.print((a.IsEmpty() ? "T": "F") + ",");
	System.out.println((a.IsFull() ? "T": "F") + ") =\t" + a);

	// Using the copy constructor
	Tree b = new Tree(a);
	System.out.print("6:  b(" + b.Size() + ",");
	System.out.print((b.IsEmpty() ? "T": "F") + ",");
	System.out.println((b.IsFull() ? "T": "F") + ") =\t" + b);
	
	// Testing for equality
	System.out.println("\n7:  a = " + a);
	System.out.println("    b = " + b);
	System.out.println("    (a == b) = " + (a.Equals(b) ? "True" : "False"));

	a.Insert(45);
	System.out.println("\n8:  a = " + a);
	System.out.println("    b = " + b);
	System.out.println("    (a == b) = " + (a.Equals(b) ? "True" : "False"));
	
	b.Insert(48);
	System.out.println("\n9:  a = " + a);
	System.out.println("    b = " + b);
	System.out.println("    (a == b) = " + (a.Equals(b) ? "True" : "False") + "\n");

	// Testing unbalanced tree of maximum size.
	Tree c = new Tree();
	for (int i = 0; i < 100; i++)
	    c.Insert(i*i);
	System.out.print("10: c(" + c.Size() + ",");
	System.out.print((c.IsEmpty() ? "T": "F") + ",");
	System.out.println((c.IsFull() ? "T": "F") + ") =\t" + c);

	// Testing random tree of maximum size
	Random r = new Random(5675);
	Tree d = new Tree();
	for (int i = 0; i < 100; i++)
	    d.Insert(r.nextInt(1000)+1);
	System.out.print("11: d(" + d.Size() + ",");
	System.out.print((d.IsEmpty() ? "T": "F") + ",");
	System.out.println((d.IsFull() ? "T": "F") + ") =\t" + d);

	// Testing getMax() and getMin()
	System.out.println("12: c.getMax() = " + c.getMax() + ", c.getMin() = " + c.getMin());
	System.out.println("    d.getMax() = " + d.getMax() + ", d.getMin() = " + d.getMin());
	
	
	
	// Adding same nodes in a different order and testing for
	// equality (even if their inorder traversals are identical)
	int [] list2 = {18, 5, 19, 25, 1, 10, 7, 3, 6, 15, 30, 24};
	Tree e = new Tree(), f = new Tree();
	for (int i = 0; i < list2.length; i++)
	{
	    e.Insert(list2[i]);
	    f.Insert(list2[list2.length - i - 1]);
	}
	System.out.println("\n13: e = " + e);
	System.out.println("    f = " + f);
	System.out.println("    (e == f) = " + (e.Equals(f) ? "True" : "False"));

	// Deleting nodes from a tree
	// Deleting a leaf
	e.Delete(3);
	System.out.print("\n14: e(" + e.Size() + ",");
	System.out.print((e.IsEmpty() ? "T": "F") + ",");
	System.out.println((e.IsFull() ? "T": "F") + ") =\t" + e);

	// Deleting multiple nodes
	int [] toDelete = {30, 15, 3, 6, 7};
	for (int i = 0; i < toDelete.length; i++)
	    e.Delete(toDelete[i]);
	System.out.print("15: e(" + e.Size() + ",");
	System.out.print((e.IsEmpty() ? "T": "F") + ",");
	System.out.println((e.IsFull() ? "T": "F") + ") =\t" + e);

	int [] toDel = {25, 19, 18, 24, 18};
	for (int i = 0; i < toDel.length; i++)
	    e.Delete(toDel[i]);
	System.out.print("16: e(" + e.Size() + ",");
	System.out.print((e.IsEmpty() ? "T": "F") + ",");
	System.out.println((e.IsFull() ? "T": "F") + ") =\t" + e);

	r = new Random(5675);
	for (int i = 0; i < 100; i++)
	{
	    // trying to delete every other random number from the
	    // random tree.
	    int discard = r.nextInt(1000) + 1;
	    int del = r.nextInt(1000) + 1;
	    d.Delete(del);
	}
	System.out.print("17: d(" + d.Size() + ",");
	System.out.print((d.IsEmpty() ? "T": "F") + ",");
	System.out.println((d.IsFull() ? "T": "F") + ") =\t" + d);

	// Trying out all the traversals and tree printing function
	System.out.println("\n18: d:");
	d.Print();
/**/    }
}
