import sys


class AVLTree:
    def __init__(self, root = None):
        self.root = root

    class AVLNode:
        def __init__(self, item, balance = 0, left = None, right = None):
            self.item = item
            self.left = left
            self.right = right
            self.balance = balance

        def getBalance(self):
            return self.balance
        def setBalance(self, balance):
            self.balance = balance
        def __repr__(self):
            return f"AVLNode({repr(self.item)}, balance = {repr(self.balance)}, left = {repr(self.left)}, right = {repr(self.right)})"

        def __iter__(self):
            if self.left != None:
                for elem in self.left:
                    yield elem

            yield self.item

            if self.right != None:
                for elem in self.right:
                    yield elem
                    
        def _getLeaves(self): # used idea from: <https://www.geeksforgeeks.org/tree-traversals-inorder-preorder-and-postorder/>
            # trivial case
            if self == None:
                return
            
            # In Order seaching for leaves
            # If not leaf, then traverse right
            if self.left != None:
                self.left._getLeaves()
            # If leaf, then print
            if self.left == None and self.right == None:
                return print(f"{self.item} ", end = "")
            # If not leaf, then traverse right
            if self.right != None:
                self.right._getLeaves()

            
            
                       
    def insert(self, item):

        def rotateRight(pivot):

            # get pivot's left child node (bad child)
            leftChild = pivot.left
            # bad child's right child becomes pivot's left child
            pivot.left = leftChild.right  
            # pivot becomes right child of bad child 
            leftChild.right = pivot    

            # Resetting Balances
            pivot.balance = 0
            leftChild.balance = 0

            # return bad child
            return leftChild
        
        def rotateLeft(pivot):
            
            # get pivot's right child node (bad child)
            rightChild = pivot.right
            # bad child's left child becomes pivot's right child
            pivot.right = rightChild.left
            # pivot becomes left child of bad child
            rightChild.left = pivot        

            # reseting balances
            pivot.balance = 0
            rightChild.balance = 0

            # return bad child
            return rightChild

        def __insert(root, item):
            # if empty tree, create a node with given item
            if root == None:
                return AVLTree.AVLNode(item)

            # item to be inserted is smaller than root
            # inserting into left subtree with specific rules to handle
            if item < root.item:
                root.left = __insert(root.left, item)

                # handle Case 1 & Case 2 with no rotations
                if root.getBalance() == 0:
                    root.balance += -1

                elif root.getBalance() == 1:
                    self.pivotFound = True
                    root.balance = 0
                
                elif root.getBalance() == -1 and root.left.balance != 0:
                    self.pivotFound = True
                    root.balance += -1
                    

                # check for Case 3 when AVL is unbalanced
                if root.getBalance() == -2:
                    # bad child must be left child, since we are in the left subtree
                    badChild = root.left

                    # Subcase A - Single Rotation
                    if item < badChild.item:
                        root = rotateRight(root)
                        self.pivotFound = False
                    # Subcase B - Double Rotation
                    if item > badChild.item:
                        badGrandChild = badChild.right
                        pivot = root
                        badChild_temp = badChild
                        badChild = rotateLeft(badChild)
                        root = rotateRight(root)

                        # adjusting balances of pivot and bad child based on bad grandchild
                        # if value inserted at badGrandChild
                        # then pivot balance = 0, bad child balance = 0
                        if item == badGrandChild.item:
                            pivot.balance = 0
                            badChild_temp.balance = 0

                        # if inserted value smaller than bad grandchild (left subtree)
                        # then pivot balance = 1, bad child balance = 0
                        if item < badGrandChild.item:
                            pivot.balance = 1
                            badChild_temp.balance = 0
                        
                        # if inserted value larger than bad grandchild (right subtree)
                        # then pivot balance = 0, bad child = -1
                        if item > badGrandChild.item:
                            pivot.balance = 0
                            badChild_temp.balance = -1

            # item to be inserted is larger than root
            # inserting into right subtree with specific rules to handle
            elif item > root.item:
                root.right = __insert(root.right, item)

                # handle Case 1 & Case 2 with no rotations
                if root.getBalance() == 0:
                    root.balance += 1

                elif root.getBalance() == -1:
                    self.pivotFound = True
                    root.balance = 0
                
                elif root.getBalance() == 1 and root.right.balance != 0:
                    self.pivotFound = True
                    root.balance += 1
                    
                # check for Case 3 when AVL is unbalanced
                if root.getBalance() == 2:
                    # bad child must be right child, since we are in the right subtree
                    badChild = root.right

                    # Subcase A - Single Rotation
                    if item > badChild.item:
                        root = rotateLeft(root)
                        self.pivotFound = False
                    # Subcase B - Double Rotation
                    if item < badChild.item:
                        badGrandChild = badChild.left
                        pivot = root
                        badChild_temp = badChild
                        badChild = rotateRight(badChild)
                        root = rotateLeft(root)

                        # adjusting balances of pivot and bad child based on bad grandchild
                        # if value inserted at badGrandChild
                        # then pivot balance = 0, bad child balance = 0
                        if item == badGrandChild.item:
                            pivot.balance = 0
                            badChild_temp.balance = 0
                        
                        # if inserted value smaller than bad grandchild (left subtree)
                        # then pivot balance = 0, bad child balance = 1
                        if item < badGrandChild.item:
                            pivot.balance = 0
                            badChild_temp.balance = 1
                        
                        # if inserted value larger than bad grandchild (right subtree)
                        # then pivot balance = -1, bad child = 0
                        if item > badGrandChild.item:
                            pivot.balance = -1
                            badChild_temp.balance = 0
            
                        
            # check if inserting duplicated value
            else:
                print(f"Insering duplicated value... {item}")
                raise Exception("Duplicate value")

            # once done __inserting return root
            return root
        
        # once done inserting update pivotFound value
        # and assign root with __insert return
        self.pivotFound = False
        self.root = __insert(self.root, item)

    # repr on tree calls repr on root node
    def __repr__(self):
        return f"AVLTree: {repr(self.root)}"

    # iter on tree calls iter on root node
    def __iter__(self):
        return iter(self.root)

    def __lookup(node, item):
        # returns True if value is in tree and False otherwise

        # Base Case
        if node == None:
            return False

        # Checking if current node.item is item being searched for
        if node.item == item:
            return True
        # recursively calling left subtree
        if AVLTree.__lookup(node.left, item):
            return True
        # not located in left, so must be right
        return AVLTree.__lookup(node.right, item)

    def __contains__(self, item):
        # checks if item is in the tree
        # runs __lookup on the tree root
        return AVLTree.__lookup(self.root, item)

    def leaves(self):
        # finds tree leaves
        self.root._getLeaves()  

def main():
    tree = AVLTree()

    # get values from input file
    file = open(sys.argv[1], "r")
    for line in file:
        values = line.split()

    # =  ['10', '3', '18', '2', '4', '13', '40', '39', '12', '38', '14', '11']

    print(f"Values to be inserted: {values}")
    print()
    
    # insert values into the AVL tree
    for v in values:
        tree.insert(int(v))
        print(f"Value {v} is inserted.")
    print()

    # print out the tree
    print(repr(tree))
    print()
    
    # print out tree in-order traversal
    print("In-order traversal: ", end = "")
    for node in tree:
        print(node, end = " ")    
    print()

    # print out tree leaves
    print("\nLeaves: ", end = "")
    tree.leaves()
    print()
    
    # check if given values are in the tree
    print()
    for val in [10, 17, 35, 38, 40]:
        if (val in tree):
            print(f"Value {val} is in tree")
        else:
            print(f"Value {val} is not in tree")  

main()
